# hmddev-cloud-learning

AWS Cloud Practitioner (CLF-C02) の学習ドキュメント・問題バンク・対話型学習システムのリポジトリです。

> ※ 本コンテンツは AWS の公式試験問題を参照していません。学習サポートとしてご利用ください。

---

## クイックスタート

### Claude Code

```bash
# teacher エージェントを起動
claude --agent teacher
```

起動後、「授業を始めて」と話しかけると学習がスタートします。

授業を再開・次の章へ進むときはスキルを呼び出します。

```
/start-lesson
```

### Kiro IDE

エージェントパネルから **teacher** を選択して起動します。

起動後の操作は Claude Code と同じです（「授業を始めて」、`/start-lesson`）。

### Kiro CLI

```bash
# teacher エージェントを起動
kiro --agent teacher
```

起動後の操作は Claude Code と同じです。

---

## 学習の進め方

### フェーズ 1 — 初期学習

```
（IT初心者の場合）appA → ch00 → ch01 → ... → ch16
```

各グループが終わると中間テスト（MPL）を提案します。ch16 修了後に最終テスト（FPL）を実施し、推奨学習プランが生成されます。

| グループ | 対象章 | テスト |
|---------|--------|--------|
| Group A | ch00〜ch04 | ch04 修了後 → MPL-1（10問） |
| Group B | ch05〜ch08 | ch08 修了後 → MPL-2（10問） |
| Group C | ch09〜ch12 | ch12 修了後 → MPL-3（10問） |
| Group D | ch13〜ch16 | ch16 修了後 → FPL（30問） |

### フェーズ 2 — 推奨プランによる復習

FPL 結果をもとに苦手章を優先した復習プランが `records/learning_plan.json` に保存されます。`/start-lesson` で自動的にフェーズ 2 の授業が始まります。

### 授業中にできること

| 操作 | 説明 |
|------|------|
| `/start-lesson` | 進捗に応じた次の授業を開始・再開 |
| 「テストして」 | その場で Quick Test（5問）を実施 |
| 「〇〇について教えて」 | 任意の AWS サービスを質問 |
| 「MPL やって」 | グループ中間テストを実施 |
| 「FPL やって」 | 最終テストを実施 |

---

## 模擬試験の生成

問題バンクから HTML 形式の模擬試験ファイルを生成します。ブラウザで開くだけで使えます。

```bash
# 全単元から 20 問（デフォルト）
python tools/generate_exam.py

# 問題数を指定
python tools/generate_exam.py --count 30

# 特定の単元のみ
python tools/generate_exam.py --chapters ch09,ch10

# ドメインで絞り込み
python tools/generate_exam.py --domain domain2

# 試験の配点比率（24:30:34:12）で自動配分
python tools/generate_exam.py --count 65 --weighted

# シード指定（同じ出題を再現したいとき）
python tools/generate_exam.py --count 20 --seed 42
```

生成ファイルは `exams/exam_YYYYMMDD_HHmmss_Nq.html` に保存されます（gitignore 対象）。

### 試験モード

| モード | 説明 |
|--------|------|
| 練習モード | 1問ずつ回答し、すぐに正解・解説を確認 |
| 本番モード | 全問回答後にまとめて採点・解説を表示 |

受験記録はブラウザの LocalStorage に自動保存されます。

### オプション一覧

`--chapters` / `--domain` / `--weighted` は排他です。

| オプション | 省略形 | デフォルト | 説明 |
|-----------|--------|-----------|------|
| `--count` | `-n` | `20` | 出力する問題数 |
| `--chapters` | `-c` | 全単元 | 対象単元（カンマ区切り） |
| `--domain` | `-d` | | 対象ドメイン ID（`domain1`〜`domain4`） |
| `--weighted` | `-w` | | 配点比率に合わせて全ドメインから自動配分 |
| `--output` | `-o` | `exams/` | 出力先ディレクトリ |
| `--seed` | | なし | 乱数シード（再現用） |

### ドメイン一覧

| ドメイン ID | ドメイン名 | 配点 | 対応単元 |
|-----------|-----------|------|---------|
| `domain1` | クラウドのコンセプト | 24% | ch00, ch07, ch14 |
| `domain2` | セキュリティとコンプライアンス | 30% | ch09 |
| `domain3` | クラウドテクノロジーとサービス | 34% | ch01〜ch06, ch08, ch10〜ch13, ch16, appA |
| `domain4` | 請求、料金、サポート | 12% | ch15, appB |

---

## ディレクトリ構成

```
hmddev-cloud-learning/
├── docs/
│   ├── chapters/               # 章ごとの学習ドキュメント（ch00〜ch16, appA〜appC）
│   └── questions/              # 問題バンク（章ごとの JSON + domains.json）
├── tools/
│   └── generate_exam.py        # 模擬試験生成ツール
├── exams/                      # 生成された模擬試験（gitignore 対象）
├── records/                    # 学習記録・進捗（gitignore 対象）
├── reports/                    # スコアレポート（gitignore 対象）
├── .claude/                    # Claude Code 用設定
│   ├── agents/                 # エージェント定義（teacher など）
│   ├── skills/start-lesson/    # /start-lesson スキル
│   └── hooks/                  # 進捗自動保存フック
└── .kiro/                      # Kiro IDE / Kiro CLI 用設定
    ├── agents/teacher.json     # teacher エージェント定義
    ├── skills/start-lesson/    # /start-lesson スキル
    ├── hooks/                  # 進捗自動保存フック
    └── steering/               # 常時コンテキスト（プロジェクト概要・章マップ）
```

### 学習記録ファイル

| ファイル | 説明 |
|---------|------|
| `records/progress.json` | 章ごとの完了状態・理解度スコア |
| `records/learning_plan.json` | FPL 後に生成される推奨学習プラン |
| `records/sessions/` | 授業・テストのセッション記録 |
| `reports/index.md` | MPL・FPL スコア一覧 |

---

## 問題の追加方法

`docs/questions/<単元ID>-*.json` の `questions` 配列に追記します。

**択一選択（`type: "single"`）**

```json
{
  "id": "ch01-001",
  "type": "single",
  "domain": "第3分野: クラウドテクノロジーとサービス",
  "text": "問題文",
  "choices": { "A": "...", "B": "...", "C": "...", "D": "..." },
  "answer": "B",
  "explanation": "解説文"
}
```

**複数選択（`type: "multi"`）** — 5択から2つ選ぶ形式

```json
{
  "id": "ch09-010",
  "type": "multi",
  "domain": "第2分野: セキュリティとコンプライアンス",
  "text": "〜を2つ選んでください。",
  "choices": { "A": "...", "B": "...", "C": "...", "D": "...", "E": "..." },
  "answer": ["A", "C"],
  "explanation": "解説文"
}
```
