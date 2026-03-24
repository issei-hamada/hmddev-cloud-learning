#!/usr/bin/env python3
"""
merge_progress.py
.session_state.json の内容を progress.json へマージする。

Usage:
    python3 merge_progress.py <checkpoint_path> <progress_path>
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"[merge_progress] {path} の読み込みに失敗: {e}", file=sys.stderr)
        sys.exit(0)  # フックはブロックしない


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def merge_lesson(state: dict, progress: dict) -> None:
    """授業セッションの進捗をマージする。"""
    chapter = state.get("chapter")
    if not chapter:
        return

    chapters = progress.setdefault("chapters", {})
    ch = chapters.setdefault(chapter, {
        "status": "not_started",
        "last_section_index": None,
        "understanding_score": None,
        "last_session_file": None,
        "sessions": [],
    })

    # completed 済みのステータスは上書きしない
    if ch.get("status") != "completed":
        ch["status"] = "in_progress"

    idx = state.get("current_section_index")
    if idx is not None:
        ch["last_section_index"] = idx

    # セクション別スコアから総合理解度を算出（最頻値、なければ最悪値）
    scores = state.get("section_scores", {})
    if scores:
        values = list(scores.values())
        for grade in ("C", "B", "A"):
            if grade in values:
                ch["understanding_score"] = grade
                break


def merge_quick_test(state: dict, progress: dict) -> None:
    """Quick Test の結果を quick_tests[] へ追記する。"""
    entry = {
        "date": state.get("last_updated", now_iso()),
        "scope": state.get("scope", ""),
        "total": state.get("total", 0),
        "correct": state.get("correct", 0),
        "score_rate": state.get("score_rate", 0.0),
        "session_file": state.get("session_file", ""),
    }
    progress.setdefault("quick_tests", []).append(entry)


def merge_mpl(state: dict, progress: dict, mpl_key: str) -> None:
    """MPL の結果を progress[mpl_key] へ上書き保存する。"""
    entry = {
        "date": state.get("last_updated", now_iso()),
        "scope": state.get("scope", ""),
        "total": state.get("total", 0),
        "correct": state.get("correct", 0),
        "score_rate": state.get("score_rate", 0.0),
        "domain_scores": state.get("domain_scores", {}),
        "weak_sections": state.get("weak_sections", []),
        "session_file": state.get("session_file", ""),
        "report_file": state.get("report_file", ""),
    }
    progress[mpl_key] = entry


def merge_fpl(state: dict, progress: dict) -> None:
    """FPL の結果を fpl_history[] へ追記する（attempt 番号を自動採番）。"""
    history = progress.setdefault("fpl_history", [])
    attempt = len(history) + 1
    entry = {
        "attempt": attempt,
        "date": state.get("last_updated", now_iso()),
        "total": state.get("total", 0),
        "correct": state.get("correct", 0),
        "score_rate": state.get("score_rate", 0.0),
        "domain_scores": state.get("domain_scores", {}),
        "weak_sections": state.get("weak_sections", []),
        "session_file": state.get("session_file", ""),
        "report_file": state.get("report_file", ""),
    }
    history.append(entry)


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <checkpoint> <progress>", file=sys.stderr)
        sys.exit(1)

    checkpoint_path = Path(sys.argv[1])
    progress_path = Path(sys.argv[2])

    state = load_json(checkpoint_path)
    progress = load_json(progress_path)

    record_type = state.get("type", "")

    if record_type == "lesson":
        merge_lesson(state, progress)
    elif record_type == "quick_test":
        merge_quick_test(state, progress)
    elif record_type in ("mpl1", "mpl2", "mpl3"):
        merge_mpl(state, progress, record_type)
    elif record_type == "fpl":
        merge_fpl(state, progress)
    else:
        print(f"[merge_progress] 未知の type: '{record_type}'。スキップします。", file=sys.stderr)
        sys.exit(0)

    progress["last_updated"] = now_iso()
    save_json(progress_path, progress)


if __name__ == "__main__":
    main()
