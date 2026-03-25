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


def build_html(
    questions: list[dict],
    chapter_filter: list[str] | None,
    domain_filter: str | None,
    weighted: bool,
    seed: int | None,
    domains: dict,
) -> str:
    """模擬試験の HTML を生成する（CSS・JS インライン、1ファイル完結）。"""
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

    # Python の内部フィールド (_chapter, _chapter_title) を除いたデータを埋め込む
    clean_questions = []
    for q in questions:
        cq = {k: v for k, v in q.items() if not k.startswith("_")}
        cq["chapter"] = q.get("_chapter", "")
        cq["chapter_title"] = q.get("_chapter_title", "")
        clean_questions.append(cq)

    questions_json = json.dumps(clean_questions, ensure_ascii=False, indent=2)

    meta_json = json.dumps({
        "title": "AWS Cloud Practitioner 模擬試験",
        "scope": scope_label,
        "count": len(questions),
        "generated": date_str,
        "seed": seed_label,
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AWS Cloud Practitioner 模擬試験</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --aws-orange: #FF9900;
    --aws-dark:   #232F3E;
    --aws-blue:   #146EB4;
    --correct:    #1d8a4a;
    --incorrect:  #c0392b;
    --neutral:    #5a6374;
    --bg:         #f4f6f9;
    --card-bg:    #ffffff;
    --border:     #dde1e7;
    --text:       #1a1a2e;
    --text-sub:   #5a6374;
    --radius:     10px;
    --shadow:     0 2px 12px rgba(0,0,0,.08);
  }}

  body {{
    font-family: "Hiragino Sans", "Meiryo", sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    line-height: 1.7;
  }}

  /* ── Header ── */
  header {{
    background: var(--aws-dark);
    color: #fff;
    padding: 0 24px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
  }}
  header .logo {{ font-size: 1rem; font-weight: 700; letter-spacing: .5px; }}
  header .logo span {{ color: var(--aws-orange); }}
  #timer {{
    font-size: .95rem;
    font-variant-numeric: tabular-nums;
    background: rgba(255,255,255,.1);
    padding: 4px 12px;
    border-radius: 20px;
    display: none;
  }}

  /* ── Layout ── */
  main {{ max-width: 780px; margin: 0 auto; padding: 32px 16px 64px; }}

  .screen {{ display: none; }}
  .screen.active {{ display: block; }}

  /* ── Card ── */
  .card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 32px;
    margin-bottom: 24px;
  }}

  /* ── Welcome ── */
  .welcome-title {{
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--aws-dark);
    margin-bottom: 6px;
  }}
  .welcome-meta {{
    font-size: .9rem;
    color: var(--text-sub);
    margin-bottom: 28px;
    border-left: 3px solid var(--aws-orange);
    padding-left: 12px;
  }}
  .mode-group {{ display: flex; flex-direction: column; gap: 14px; margin-bottom: 28px; }}
  .mode-card {{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 16px 20px;
    border: 2px solid var(--border);
    border-radius: var(--radius);
    cursor: pointer;
    transition: border-color .15s, background .15s;
  }}
  .mode-card:hover {{ border-color: var(--aws-orange); background: #fffbf3; }}
  .mode-card.selected {{ border-color: var(--aws-orange); background: #fffbf3; }}
  .mode-card input[type=radio] {{ margin-top: 3px; accent-color: var(--aws-orange); width: 18px; height: 18px; flex-shrink: 0; }}
  .mode-card .mode-label {{ font-weight: 700; font-size: 1rem; }}
  .mode-card .mode-desc {{ font-size: .87rem; color: var(--text-sub); margin-top: 2px; }}

  /* ── Buttons ── */
  .btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 11px 28px;
    border: none;
    border-radius: 6px;
    font-size: .95rem;
    font-weight: 700;
    cursor: pointer;
    transition: opacity .15s, transform .1s;
  }}
  .btn:active {{ transform: scale(.97); }}
  .btn:disabled {{ opacity: .45; cursor: not-allowed; transform: none; }}
  .btn-primary {{ background: var(--aws-orange); color: #fff; }}
  .btn-primary:hover:not(:disabled) {{ opacity: .88; }}
  .btn-secondary {{ background: var(--aws-dark); color: #fff; }}
  .btn-secondary:hover:not(:disabled) {{ opacity: .82; }}
  .btn-outline {{
    background: transparent;
    color: var(--aws-dark);
    border: 1.5px solid var(--border);
  }}
  .btn-outline:hover {{ border-color: var(--aws-dark); }}
  .btn-danger {{ background: var(--incorrect); color: #fff; }}
  .btn-danger:hover:not(:disabled) {{ opacity: .85; }}
  .btn-sm {{ padding: 7px 16px; font-size: .85rem; }}

  /* ── Progress bar ── */
  .progress-wrap {{
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .progress-bar {{
    flex: 1;
    height: 7px;
    background: var(--border);
    border-radius: 99px;
    overflow: hidden;
  }}
  .progress-fill {{
    height: 100%;
    background: var(--aws-orange);
    border-radius: 99px;
    transition: width .3s ease;
  }}
  .progress-label {{ font-size: .85rem; color: var(--text-sub); white-space: nowrap; }}

  /* ── Question card ── */
  .question-meta {{
    font-size: .8rem;
    color: var(--text-sub);
    margin-bottom: 12px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .meta-tag {{
    background: #eef1f5;
    border-radius: 4px;
    padding: 2px 8px;
  }}
  .multi-badge {{
    display: inline-block;
    background: var(--aws-blue);
    color: #fff;
    font-size: .75rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
    vertical-align: middle;
  }}
  .question-text {{
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 20px;
    line-height: 1.65;
  }}

  /* ── Choices ── */
  .choices {{ display: flex; flex-direction: column; gap: 10px; }}
  .choice-btn {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border: 2px solid var(--border);
    border-radius: 8px;
    background: var(--card-bg);
    cursor: pointer;
    text-align: left;
    font-size: .95rem;
    transition: border-color .15s, background .15s;
    width: 100%;
  }}
  .choice-btn:hover:not(:disabled) {{ border-color: var(--aws-blue); background: #f0f6ff; }}
  .choice-btn .choice-key {{
    font-weight: 700;
    min-width: 22px;
    color: var(--aws-blue);
    flex-shrink: 0;
  }}
  .choice-btn.selected {{ border-color: var(--aws-blue); background: #f0f6ff; }}
  .choice-btn.correct  {{ border-color: var(--correct); background: #edfaf3; }}
  .choice-btn.incorrect {{ border-color: var(--incorrect); background: #fdf0ee; }}
  .choice-btn.revealed  {{ border-color: var(--correct); background: #edfaf3; }}
  .choice-btn:disabled {{ cursor: default; }}
  .choice-icon {{ margin-left: auto; font-size: 1.1rem; flex-shrink: 0; }}

  /* ── Explanation ── */
  .explanation-box {{
    margin-top: 20px;
    padding: 16px 20px;
    background: #f8f9fc;
    border-left: 4px solid var(--aws-orange);
    border-radius: 0 8px 8px 0;
    font-size: .9rem;
    line-height: 1.7;
  }}
  .explanation-box .answer-line {{
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 8px;
    color: var(--aws-dark);
  }}
  .explanation-box .domain-line {{
    margin-top: 10px;
    font-size: .82rem;
    color: var(--text-sub);
  }}

  /* ── Exam mode: answer area ── */
  .exam-action {{
    margin-top: 20px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }}

  /* ── Result ── */
  .result-score-wrap {{
    display: flex;
    align-items: center;
    gap: 32px;
    flex-wrap: wrap;
    margin-bottom: 28px;
  }}
  .score-circle {{
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 6px solid var(--aws-orange);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}
  .score-circle .score-num {{ font-size: 2rem; font-weight: 800; color: var(--aws-dark); }}
  .score-circle .score-denom {{ font-size: .8rem; color: var(--text-sub); }}
  .result-stats {{ display: flex; flex-direction: column; gap: 8px; }}
  .stat-row {{ display: flex; gap: 8px; align-items: center; font-size: .92rem; }}
  .stat-row .stat-label {{ color: var(--text-sub); min-width: 80px; }}
  .stat-row .stat-val {{ font-weight: 700; }}

  /* ── Result list ── */
  .result-list {{ display: flex; flex-direction: column; gap: 12px; margin-top: 8px; }}
  .result-item {{
    border: 1.5px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
  }}
  .result-item-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    cursor: pointer;
    background: #fafbfd;
    user-select: none;
  }}
  .result-item-header:hover {{ background: #f3f5f9; }}
  .result-badge {{
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: .9rem;
    font-weight: 700;
    flex-shrink: 0;
  }}
  .result-badge.ok  {{ background: #edfaf3; color: var(--correct); }}
  .result-badge.ng  {{ background: #fdf0ee; color: var(--incorrect); }}
  .result-item-q {{ font-size: .9rem; flex: 1; }}
  .result-item-body {{ padding: 14px 16px; border-top: 1px solid var(--border); font-size: .88rem; }}
  .result-item-body .choice-row {{ padding: 4px 0; }}
  .result-item-body .choice-row.correct  {{ color: var(--correct); font-weight: 600; }}
  .result-item-body .choice-row.incorrect {{ color: var(--incorrect); }}
  .result-item-body .expl {{ margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border); color: var(--text-sub); line-height: 1.65; }}
  details summary {{ list-style: none; }}
  details summary::-webkit-details-marker {{ display: none; }}

  /* ── History ── */
  .history-table {{ width: 100%; border-collapse: collapse; font-size: .88rem; }}
  .history-table th, .history-table td {{
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
    text-align: left;
  }}
  .history-table th {{ color: var(--text-sub); font-weight: 600; background: #fafbfd; }}
  .history-table tr:last-child td {{ border-bottom: none; }}

  .section-title {{ font-size: 1.05rem; font-weight: 700; margin-bottom: 16px; color: var(--aws-dark); }}
  .divider {{ border: none; border-top: 1px solid var(--border); margin: 28px 0; }}

  .actions-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 8px; }}

  @media (max-width: 520px) {{
    .card {{ padding: 20px 16px; }}
    .result-score-wrap {{ gap: 20px; }}
  }}
</style>
</head>
<body>

<header>
  <div class="logo">AWS <span>Cloud Practitioner</span> 模擬試験</div>
  <div id="timer">⏱ 00:00:00</div>
</header>

<main>

  <!-- ══ Welcome Screen ══ -->
  <div id="screen-welcome" class="screen active">
    <div class="card">
      <div class="welcome-title">AWS Cloud Practitioner 模擬試験</div>
      <div class="welcome-meta" id="welcome-meta"></div>

      <div class="mode-group">
        <label class="mode-card selected" id="label-practice">
          <input type="radio" name="mode" value="practice" checked>
          <div>
            <div class="mode-label">練習モード</div>
            <div class="mode-desc">1問ずつ回答し、すぐに正解・解説を確認できます。理解を深めたいときに。</div>
          </div>
        </label>
        <label class="mode-card" id="label-exam">
          <input type="radio" name="mode" value="exam">
          <div>
            <div class="mode-label">本番モード</div>
            <div class="mode-desc">全問回答後にまとめて採点・解説を表示します。実力を試したいときに。</div>
          </div>
        </label>
      </div>

      <button class="btn btn-primary" id="btn-start">▶ スタート</button>
    </div>

    <div class="card">
      <div class="section-title">過去の受験記録</div>
      <div id="history-container-welcome"></div>
      <hr class="divider">
      <div class="actions-row">
        <button class="btn btn-outline btn-sm btn-danger" id="btn-reset-history">🗑 記録をリセット</button>
      </div>
    </div>
  </div>

  <!-- ══ Exam Screen ══ -->
  <div id="screen-exam" class="screen">
    <div class="progress-wrap">
      <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
      <div class="progress-label" id="progress-label"></div>
    </div>
    <div class="card" id="question-card"></div>
    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:4px;" id="nav-buttons"></div>
  </div>

  <!-- ══ Result Screen ══ -->
  <div id="screen-result" class="screen">
    <div class="card">
      <div class="section-title">試験結果</div>
      <div class="result-score-wrap">
        <div class="score-circle">
          <span class="score-num" id="result-score-num">--</span>
          <span class="score-denom" id="result-score-denom">/ --</span>
        </div>
        <div class="result-stats" id="result-stats"></div>
      </div>
      <div class="actions-row">
        <button class="btn btn-primary" id="btn-retry">↩ もう一度</button>
      </div>
    </div>

    <div class="card">
      <div class="section-title">解答一覧</div>
      <div class="result-list" id="result-list"></div>
    </div>

    <div class="card">
      <div class="section-title">過去の受験記録</div>
      <div id="history-container-result"></div>
      <hr class="divider">
      <div class="actions-row">
        <button class="btn btn-outline btn-sm btn-danger" id="btn-reset-history-result">🗑 記録をリセット</button>
      </div>
    </div>
  </div>

</main>

<script>
// ── データ ──────────────────────────────────────────────────
const QUESTIONS = {questions_json};
const META      = {meta_json};
const LS_KEY    = 'aws_exam_history';
const MAX_HIST  = 50;

// ── 状態 ────────────────────────────────────────────────────
let state = {{
  mode: 'practice',
  current: 0,
  answers: [],       // 各問: string[] (選択済みキー)
  revealed: [],      // 各問: boolean (練習モードで解答済み)
  startTime: null,
  timerInterval: null,
  elapsed: 0,
}};

// ── 初期化 ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {{
  initMeta();
  renderHistoryTable('history-container-welcome');
  bindWelcome();
}});

function initMeta() {{
  const el = document.getElementById('welcome-meta');
  el.textContent =
    `問題数: ${{META.count}}問  /  対象: ${{META.scope}}  /  生成日時: ${{META.generated}}` +
    (META.seed ? `  ${{META.seed}}` : '');
}}

// ── Welcome バインド ─────────────────────────────────────────
function bindWelcome() {{
  document.querySelectorAll('input[name=mode]').forEach(r => {{
    r.addEventListener('change', () => {{
      document.getElementById('label-practice').classList.toggle('selected', r.value === 'practice' ? r.checked : false);
      document.getElementById('label-exam').classList.toggle('selected', r.value === 'exam' ? r.checked : false);
      // 両方リセット後に選択を反映
      document.querySelectorAll('input[name=mode]').forEach(rr => {{
        const lbl = rr.value === 'practice' ? 'label-practice' : 'label-exam';
        document.getElementById(lbl).classList.toggle('selected', rr.checked);
      }});
    }});
  }});

  document.getElementById('btn-start').addEventListener('click', startExam);
  document.getElementById('btn-reset-history').addEventListener('click', resetHistory);
  document.getElementById('btn-reset-history-result').addEventListener('click', resetHistory);
  document.getElementById('btn-retry').addEventListener('click', () => showScreen('welcome'));
}}

// ── 試験開始 ─────────────────────────────────────────────────
function startExam() {{
  state.mode      = document.querySelector('input[name=mode]:checked').value;
  state.current   = 0;
  state.answers   = QUESTIONS.map(() => []);
  state.revealed  = QUESTIONS.map(() => false);
  state.elapsed   = 0;

  showScreen('exam');
  startTimer();
  renderQuestion();
}}

// ── タイマー ─────────────────────────────────────────────────
function startTimer() {{
  state.startTime = Date.now();
  const timerEl = document.getElementById('timer');
  timerEl.style.display = 'block';
  clearInterval(state.timerInterval);
  state.timerInterval = setInterval(() => {{
    state.elapsed = Math.floor((Date.now() - state.startTime) / 1000);
    timerEl.textContent = '⏱ ' + formatTime(state.elapsed);
  }}, 500);
}}

function stopTimer() {{
  clearInterval(state.timerInterval);
  state.timerInterval = null;
  document.getElementById('timer').style.display = 'none';
}}

function formatTime(sec) {{
  const h = String(Math.floor(sec / 3600)).padStart(2, '0');
  const m = String(Math.floor((sec % 3600) / 60)).padStart(2, '0');
  const s = String(sec % 60).padStart(2, '0');
  return `${{h}}:${{m}}:${{s}}`;
}}

// ── 問題レンダリング ──────────────────────────────────────────
function renderQuestion() {{
  const q    = QUESTIONS[state.current];
  const idx  = state.current;
  const isMulti = q.type === 'multi';
  const answered = state.revealed[idx];
  const sel  = state.answers[idx];

  // 進捗バー
  const pct = ((idx) / QUESTIONS.length) * 100;
  document.getElementById('progress-fill').style.width = pct + '%';
  document.getElementById('progress-label').textContent =
    `${{idx + 1}} / ${{QUESTIONS.length}}`;

  // メタ
  const metaParts = [];
  if (q.id)            metaParts.push(`<span class="meta-tag">${{q.id}}</span>`);
  if (q.chapter_title) metaParts.push(`<span class="meta-tag">${{e(q.chapter_title)}}</span>`);
  if (q.domain)        metaParts.push(`<span class="meta-tag">${{e(q.domain)}}</span>`);

  // 選択肢
  const correctKeys = Array.isArray(q.answer) ? q.answer : [q.answer];

  let choicesHtml = '<div class="choices">';
  for (const key of Object.keys(q.choices).sort()) {{
    const isCorrect  = correctKeys.includes(key);
    const isSelected = sel.includes(key);
    let cls = 'choice-btn';
    let icon = '';

    if (answered) {{
      if (isCorrect)  {{ cls += ' revealed'; icon = '<span class="choice-icon">✓</span>'; }}
      if (isSelected && !isCorrect) {{ cls += ' incorrect'; icon = '<span class="choice-icon">✗</span>'; }}
    }} else {{
      if (isSelected) cls += ' selected';
    }}

    const disabledAttr = answered ? 'disabled' : '';
    choicesHtml += `
      <button class="${{cls}}" data-key="${{key}}" ${{disabledAttr}}>
        <span class="choice-key">${{key}}.</span>
        <span>${{e(q.choices[key])}}</span>
        ${{icon}}
      </button>`;
  }}
  choicesHtml += '</div>';

  // 解説（練習モードで回答済み、または本番モードの結果表示時）
  let explanationHtml = '';
  if (answered && state.mode === 'practice') {{
    const ansStr = correctKeys.join('・');
    explanationHtml = `
      <div class="explanation-box">
        <div class="answer-line">正解: ${{ansStr}}</div>
        <div>${{e(q.explanation || '')}}</div>
        ${{q.domain ? `<div class="domain-line">対応ドメイン: ${{e(q.domain)}}</div>` : ''}}
      </div>`;
  }}

  // アクションボタン
  let actionHtml = '';
  if (state.mode === 'practice') {{
    if (!answered) {{
      actionHtml = `<div class="exam-action">
        <button class="btn btn-primary" id="btn-check" ${{sel.length === 0 ? 'disabled' : ''}}>
          ${{isMulti ? '確認する' : '回答する'}}
        </button>
      </div>`;
    }} else {{
      const isLast = idx === QUESTIONS.length - 1;
      actionHtml = `<div class="exam-action">
        ${{isLast
          ? `<button class="btn btn-primary" id="btn-finish">採点・結果を見る</button>`
          : `<button class="btn btn-primary" id="btn-next">次の問題 →</button>`
        }}
      </div>`;
    }}
  }} else {{
    // 本番モード
    const isLast = idx === QUESTIONS.length - 1;
    actionHtml = `<div class="exam-action">
      ${{isLast
        ? `<button class="btn btn-primary" id="btn-finish" ${{sel.length === 0 ? 'disabled' : ''}}>採点・結果を見る</button>`
        : `<button class="btn btn-primary" id="btn-next" ${{sel.length === 0 ? 'disabled' : ''}}>次の問題 →</button>`
      }}
      ${{idx > 0 ? `<button class="btn btn-outline" id="btn-prev">← 前の問題</button>` : ''}}
    </div>`;
  }}

  document.getElementById('question-card').innerHTML = `
    <div class="question-meta">${{metaParts.join('')}}</div>
    <div class="question-text">
      問題 ${{idx + 1}}${{isMulti ? '<span class="multi-badge">2つ選べ</span>' : ''}}
      <br><br>${{e(q.text)}}
    </div>
    ${{choicesHtml}}
    ${{explanationHtml}}
    ${{actionHtml}}
  `;

  // イベント
  document.querySelectorAll('.choice-btn:not(:disabled)').forEach(btn => {{
    btn.addEventListener('click', () => onChoiceClick(btn.dataset.key, isMulti));
  }});
  document.getElementById('btn-check')?.addEventListener('click', revealAnswer);
  document.getElementById('btn-next')?.addEventListener('click', () => {{ state.current++; renderQuestion(); }});
  document.getElementById('btn-prev')?.addEventListener('click', () => {{ state.current--; renderQuestion(); }});
  document.getElementById('btn-finish')?.addEventListener('click', finishExam);
}}

function onChoiceClick(key, isMulti) {{
  const idx = state.current;
  const sel = state.answers[idx];
  if (isMulti) {{
    const pos = sel.indexOf(key);
    if (pos >= 0) sel.splice(pos, 1);
    else sel.push(key);
  }} else {{
    state.answers[idx] = [key];
  }}
  renderQuestion();
}}

function revealAnswer() {{
  state.revealed[state.current] = true;
  renderQuestion();
}}

// ── 試験終了・採点 ────────────────────────────────────────────
function finishExam() {{
  stopTimer();

  // 本番モードでは全問 revealed にして解説を出す
  if (state.mode === 'exam') {{
    state.revealed = state.revealed.map(() => true);
  }}

  let correct = 0;
  QUESTIONS.forEach((q, i) => {{
    const correctKeys = Array.isArray(q.answer) ? [...q.answer].sort() : [q.answer];
    const userKeys    = [...state.answers[i]].sort();
    if (JSON.stringify(correctKeys) === JSON.stringify(userKeys)) correct++;
  }});

  const total   = QUESTIONS.length;
  const pct     = Math.round((correct / total) * 100);
  const elapsed = state.elapsed;

  // LocalStorage に保存
  saveHistory({{ correct, total, pct, elapsed, mode: state.mode, generated: META.generated }});

  showScreen('result');
  renderResult(correct, total, pct, elapsed);
}}

// ── 結果レンダリング ──────────────────────────────────────────
function renderResult(correct, total, pct, elapsed) {{
  document.getElementById('result-score-num').textContent  = correct;
  document.getElementById('result-score-denom').textContent = `/ ${{total}}`;

  document.getElementById('result-stats').innerHTML = `
    <div class="stat-row"><span class="stat-label">正答率</span><span class="stat-val">${{pct}}%</span></div>
    <div class="stat-row"><span class="stat-label">所要時間</span><span class="stat-val">${{formatTime(elapsed)}}</span></div>
    <div class="stat-row"><span class="stat-label">モード</span><span class="stat-val">${{state.mode === 'practice' ? '練習' : '本番'}}</span></div>
    <div class="stat-row"><span class="stat-label">対象</span><span class="stat-val">${{e(META.scope)}}</span></div>
  `;

  const listEl = document.getElementById('result-list');
  listEl.innerHTML = '';
  QUESTIONS.forEach((q, i) => {{
    const correctKeys = Array.isArray(q.answer) ? [...q.answer].sort() : [q.answer];
    const userKeys    = [...state.answers[i]].sort();
    const isOk = JSON.stringify(correctKeys) === JSON.stringify(userKeys);

    let choiceRows = Object.keys(q.choices).sort().map(key => {{
      const isCorrect  = correctKeys.includes(key);
      const isSelected = userKeys.includes(key);
      let cls = 'choice-row';
      let mark = '';
      if (isCorrect)  {{ cls += ' correct';   mark = ' ✓'; }}
      if (isSelected && !isCorrect) {{ cls += ' incorrect'; mark = ' ✗'; }}
      return `<div class="${{cls}}">${{key}}. ${{e(q.choices[key])}}${{mark}}</div>`;
    }}).join('');

    listEl.innerHTML += `
      <div class="result-item">
        <details>
          <summary class="result-item-header">
            <span class="result-badge ${{isOk ? 'ok' : 'ng'}}">${{isOk ? '○' : '✗'}}</span>
            <span class="result-item-q">問題 ${{i + 1}}  ${{e(q.text.slice(0, 60))}}${{q.text.length > 60 ? '…' : ''}}</span>
          </summary>
          <div class="result-item-body">
            ${{choiceRows}}
            <div class="expl">${{e(q.explanation || '')}}</div>
            ${{q.domain ? `<div style="margin-top:6px;font-size:.8rem;color:var(--text-sub)">対応ドメイン: ${{e(q.domain)}}</div>` : ''}}
          </div>
        </details>
      </div>`;
  }});

  renderHistoryTable('history-container-result');
}}

// ── LocalStorage ─────────────────────────────────────────────
function loadHistory() {{
  try {{ return JSON.parse(localStorage.getItem(LS_KEY) || '[]'); }}
  catch {{ return []; }}
}}

function saveHistory(entry) {{
  const hist = loadHistory();
  hist.unshift({{ ...entry, date: new Date().toLocaleString('ja-JP') }});
  if (hist.length > MAX_HIST) hist.splice(MAX_HIST);
  localStorage.setItem(LS_KEY, JSON.stringify(hist));
}}

function resetHistory() {{
  if (!confirm('過去の受験記録をすべて削除しますか？')) return;
  localStorage.removeItem(LS_KEY);
  renderHistoryTable('history-container-welcome');
  renderHistoryTable('history-container-result');
}}

function renderHistoryTable(containerId) {{
  const el   = document.getElementById(containerId);
  if (!el) return;
  const hist = loadHistory();
  if (hist.length === 0) {{
    el.innerHTML = '<p style="color:var(--text-sub);font-size:.9rem;">記録はまだありません。</p>';
    return;
  }}
  let rows = hist.map(h => `
    <tr>
      <td>${{h.date}}</td>
      <td>${{h.correct}} / ${{h.total}}</td>
      <td>${{h.pct}}%</td>
      <td>${{formatTime(h.elapsed)}}</td>
      <td>${{h.mode === 'practice' ? '練習' : '本番'}}</td>
    </tr>`).join('');
  el.innerHTML = `
    <table class="history-table">
      <thead><tr><th>日時</th><th>正解数</th><th>正答率</th><th>時間</th><th>モード</th></tr></thead>
      <tbody>${{rows}}</tbody>
    </table>`;
}}

// ── 画面切替 ─────────────────────────────────────────────────
function showScreen(name) {{
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById('screen-' + name).classList.add('active');
  if (name === 'welcome') {{
    renderHistoryTable('history-container-welcome');
  }}
}}

// ── XSS対策 ─────────────────────────────────────────────────
function e(str) {{
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}}
</script>

</body>
</html>"""


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
        html = build_html(sampled, None, None, True, args.seed, domains)

    # --- --domain ---
    elif args.domain:
        chapter_filter = chapters_for_domain(args.domain, domains)
        questions = load_questions(chapter_filter)
        if not questions:
            print(f"[ERROR] ドメイン {args.domain} に問題が登録されていません。", file=sys.stderr)
            sys.exit(1)
        sampled = sample_questions(questions, args.count, args.seed)
        html = build_html(sampled, None, args.domain, False, args.seed, domains)

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
        html = build_html(sampled, chapter_filter, None, False, args.seed, domains)

    # 出力先ディレクトリ
    output_dir = Path(args.output) if args.output else EXAMS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    # ファイル名: exam_YYYYMMDD_HHmmss_Nq.html
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"exam_{timestamp}_{len(sampled)}q.html"
    output_path = output_dir / filename

    output_path.write_text(html, encoding="utf-8")
    print(f"模擬試験を生成しました: {output_path}")


if __name__ == "__main__":
    main()
