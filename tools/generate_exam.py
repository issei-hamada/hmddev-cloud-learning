#!/usr/bin/env python3
"""
AWS Cloud Practitioner 模擬試験ジェネレーター

使い方:
  python tools/generate_exam.py
  python tools/generate_exam.py --count 30
  python tools/generate_exam.py --chapters ch01,ch02,ch09
  python tools/generate_exam.py --domain domain2
  python tools/generate_exam.py --count 50 --weighted
  python tools/generate_exam.py --count 10 --chapters ch09,ch10 --seed 42
"""

import argparse
import json
import math
import random
import sys
from datetime import datetime
from pathlib import Path

QUESTIONS_DIR = Path(__file__).parent.parent / "docs" / "questions"
EXAMS_DIR = Path(__file__).parent.parent / "exams"
DOMAINS_FILE = QUESTIONS_DIR / "domains.json"

CHAPTER_ORDER = [
    "ch00", "ch01", "ch02", "ch03", "ch04",
    "ch05", "ch06", "ch07", "ch08", "ch09",
    "ch10", "ch11", "ch12", "ch13", "ch14",
    "ch15", "ch16", "appA", "appB", "appC",
]


def load_domains() -> dict:
    """domains.json を読み込む。ファイルがなければ空dictを返す。"""
    if not DOMAINS_FILE.exists():
        return {}
    try:
        return json.loads(DOMAINS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[ERROR] domains.json の読み込みに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)


def chapters_for_domain(domain_id: str, domains: dict) -> list[str]:
    """ドメインIDに対応する章リストを返す。"""
    if domain_id not in domains:
        valid = ", ".join(domains.keys())
        print(f"[ERROR] 不明なドメインID: {domain_id}", file=sys.stderr)
        print(f"  利用可能なドメイン: {valid}", file=sys.stderr)
        sys.exit(1)
    return domains[domain_id]["chapters"]


def load_questions(chapter_filter: list[str] | None) -> list[dict]:
    """問題バンクから問題を読み込む。chapter_filter が None の場合は全章を対象とする。"""
    all_questions = []

    json_files = sorted(
        f for f in QUESTIONS_DIR.glob("*.json") if f.name != "domains.json"
    )
    if not json_files:
        print(f"[ERROR] 問題ファイルが見つかりません: {QUESTIONS_DIR}", file=sys.stderr)
        sys.exit(1)

    for path in json_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"[WARN] {path.name} の読み込みに失敗しました: {e}", file=sys.stderr)
            continue

        chapter = data.get("chapter", "")
        if chapter_filter and chapter not in chapter_filter:
            continue

        for q in data.get("questions", []):
            q["_chapter"] = chapter
            q["_chapter_title"] = data.get("title", "")
            all_questions.append(q)

    return all_questions


def sample_questions(questions: list[dict], count: int, seed: int | None) -> list[dict]:
    """問題をランダムに抽出する。"""
    if seed is not None:
        random.seed(seed)

    if count > len(questions):
        print(
            f"[WARN] 指定された問題数 ({count}) が利用可能な問題数 ({len(questions)}) を超えています。"
            f" 全問題を出題します。",
            file=sys.stderr,
        )
        count = len(questions)

    return random.sample(questions, count)


def sample_weighted(domains: dict, count: int, seed: int | None) -> list[dict]:
    """ドメインの配点比率に応じて問題をランダム抽出する。"""
    if seed is not None:
        random.seed(seed)

    total_weight = sum(d["weight"] for d in domains.values())
    sampled: list[dict] = []

    # 各ドメインの割り当て問題数を計算（小数点以下は切り捨て後、余りを大きい順に補完）
    raw_counts = {
        did: count * d["weight"] / total_weight
        for did, d in domains.items()
    }
    floor_counts = {did: math.floor(v) for did, v in raw_counts.items()}
    remainder = count - sum(floor_counts.values())
    # 小数部が大きい順にドメインへ余りを1ずつ配分
    sorted_by_frac = sorted(
        raw_counts.keys(),
        key=lambda did: raw_counts[did] - floor_counts[did],
        reverse=True,
    )
    for did in sorted_by_frac[:remainder]:
        floor_counts[did] += 1

    for did, domain_info in domains.items():
        n = floor_counts[did]
        if n == 0:
            continue
        domain_questions = load_questions(domain_info["chapters"])
        if not domain_questions:
            print(
                f"[WARN] ドメイン {did}（{domain_info['name']}）に問題が登録されていません。スキップします。",
                file=sys.stderr,
            )
            continue
        if n > len(domain_questions):
            print(
                f"[WARN] ドメイン {did} の割り当て問題数 ({n}) が利用可能な問題数 ({len(domain_questions)}) を超えています。",
                file=sys.stderr,
            )
            n = len(domain_questions)
        sampled.extend(random.sample(domain_questions, n))

    random.shuffle(sampled)
    return sampled


def format_question(index: int, q: dict) -> str:
    """1問分のMarkdownブロックを生成する。"""
    qid = q.get("id", "")
    q_type = q.get("type", "single")
    domain = q.get("domain", "")
    text = q.get("text", "")
    choices = q.get("choices", {})
    answer = q.get("answer", "")
    explanation = q.get("explanation", "")
    chapter_title = q.get("_chapter_title", "")

    is_multi = q_type == "multi"

    lines = []
    lines.append(f"## 問題 {index}" + ("　※2つ選べ" if is_multi else ""))
    lines.append("")

    meta_parts = []
    if qid:
        meta_parts.append(f"**[{qid}]**")
    if chapter_title:
        meta_parts.append(f"単元: {chapter_title}")
    if domain:
        meta_parts.append(f"ドメイン: {domain}")
    if meta_parts:
        lines.append("> " + " / ".join(meta_parts))
        lines.append("")

    lines.append(text)
    lines.append("")

    for key in sorted(choices.keys()):
        lines.append(f"- {key}. {choices[key]}")
    lines.append("")

    # 正解の表示（単一 or 複数）
    if isinstance(answer, list):
        answer_str = "・".join(answer)
    else:
        answer_str = str(answer)

    lines.append("<details>")
    lines.append("<summary>解答・解説を見る</summary>")
    lines.append("")
    lines.append(f"**正解: {answer_str}**")
    if explanation:
        lines.append("")
        lines.append(explanation)
    if domain:
        lines.append("")
        lines.append(f"**対応ドメイン**: {domain}")
    lines.append("")
    lines.append("</details>")
    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def build_markdown(
    questions: list[dict],
    chapter_filter: list[str] | None,
    domain_filter: str | None,
    weighted: bool,
    seed: int | None,
    domains: dict,
) -> str:
    """模擬試験全体のMarkdownを生成する。"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M")

    if weighted:
        scope_label = "全ドメイン（配点比率配分）"
    elif domain_filter:
        scope_label = f"ドメイン: {domains.get(domain_filter, {}).get('name', domain_filter)}"
    elif chapter_filter:
        scope_label = ", ".join(chapter_filter)
    else:
        scope_label = "全単元"

    seed_label = f" / シード: {seed}" if seed is not None else ""

    lines = []
    lines.append("# AWS Cloud Practitioner 模擬試験")
    lines.append("")
    lines.append(
        f"**問題数**: {len(questions)}問 / "
        f"**対象**: {scope_label} / "
        f"**生成日時**: {date_str}"
        f"{seed_label}"
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, q in enumerate(questions, start=1):
        lines.append(format_question(i, q))

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AWS Cloud Practitioner 模擬試験をランダム生成します。"
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=20,
        metavar="N",
        help="出力する問題数 (デフォルト: 20)",
    )

    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument(
        "-c", "--chapters",
        type=str,
        default=None,
        metavar="CHAPTERS",
        help="対象単元をカンマ区切りで指定 (例: ch01,ch02,ch09)。省略時は全単元。",
    )
    filter_group.add_argument(
        "-d", "--domain",
        type=str,
        default=None,
        metavar="DOMAIN_ID",
        help="対象ドメインIDを指定 (例: domain2)。--chapters と同時指定不可。",
    )
    filter_group.add_argument(
        "-w", "--weighted",
        action="store_true",
        help="試験の配点比率（24:30:34:12）に合わせて各ドメインから自動配分する。",
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        metavar="DIR",
        help="出力先ディレクトリ (デフォルト: exams/)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        metavar="SEED",
        help="乱数シード (再現用。省略時はランダム)",
    )
    args = parser.parse_args()

    domains = load_domains()

    # --- --weighted ---
    if args.weighted:
        if not domains:
            print("[ERROR] domains.json が見つからないため --weighted を使用できません。", file=sys.stderr)
            sys.exit(1)
        sampled = sample_weighted(domains, args.count, args.seed)
        if not sampled:
            print("[ERROR] 問題が1問も取得できませんでした。", file=sys.stderr)
            sys.exit(1)
        markdown = build_markdown(sampled, None, None, True, args.seed, domains)

    # --- --domain ---
    elif args.domain:
        chapter_filter = chapters_for_domain(args.domain, domains)
        questions = load_questions(chapter_filter)
        if not questions:
            print(f"[ERROR] ドメイン {args.domain} に問題が登録されていません。", file=sys.stderr)
            sys.exit(1)
        sampled = sample_questions(questions, args.count, args.seed)
        markdown = build_markdown(sampled, None, args.domain, False, args.seed, domains)

    # --- --chapters / 全単元 ---
    else:
        chapter_filter: list[str] | None = None
        if args.chapters:
            chapter_filter = [c.strip() for c in args.chapters.split(",") if c.strip()]
            invalid = [c for c in chapter_filter if c not in CHAPTER_ORDER]
            if invalid:
                print(f"[ERROR] 不明な単元が指定されました: {', '.join(invalid)}", file=sys.stderr)
                print(f"  利用可能な単元: {', '.join(CHAPTER_ORDER)}", file=sys.stderr)
                sys.exit(1)

        questions = load_questions(chapter_filter)
        if not questions:
            label = f"単元 {', '.join(chapter_filter)}" if chapter_filter else "全単元"
            print(f"[ERROR] {label} に問題が登録されていません。", file=sys.stderr)
            sys.exit(1)
        sampled = sample_questions(questions, args.count, args.seed)
        markdown = build_markdown(sampled, chapter_filter, None, False, args.seed, domains)

    # 出力先ディレクトリ
    output_dir = Path(args.output) if args.output else EXAMS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    # ファイル名: exam_YYYYMMDD_HHmmss_Nq.md
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"exam_{timestamp}_{len(sampled)}q.md"
    output_path = output_dir / filename

    output_path.write_text(markdown, encoding="utf-8")
    print(f"模擬試験を生成しました: {output_path}")


if __name__ == "__main__":
    main()
