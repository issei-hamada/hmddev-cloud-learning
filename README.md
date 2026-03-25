# hmddev-cloud-learning

AWS Cloud Practitioner (CLF-C02) の学習ドキュメント・問題バンク・対話型学習システムのリポジトリです。

> ※ 注意事項: 本コンテンツは AWS の公式試験問題を参照している訳ではありません。あくまで学習のサポートとして利用して下さい。

---

## 対話型学習システム（teacher エージェント）

Claude Code の `--agent teacher` オプションで起動する対話型学習エージェントです。

```bash
claude --agent teacher
```

### できること

| 機能 | 説明 |
|------|------|
| **対話型授業** | 章ごとにセクション単位で授業。確認質問・フィードバックつき |
| **Quick Test** | 最大5問の即席テスト（任意のタイミングで実施） |
| **MPL（中間テスト）** | グループ終了後に10問（MPL-1〜3） |
| **FPL（最終テスト）** | ch16 修了後に30問・本番試験配分 |
| **スコアレポート** | MPL・FPL 完了後に `reports/` へ自動生成 |
| **推奨学習プラン** | FPL 結果を元に苦手章を優先した復習プランを生成 |

### 学習フロー

```
フェーズ1: 初期学習
  （IT初心者の場合: appA → ）ch00 → ch01 → ... → ch16
  各グループ終了後に MPL を提案
  ch16 終了後に FPL を実施 → 推奨学習プラン生成

フェーズ2: プランに沿った復習
  learning_plan.json に従って苦手章を重点復習
  → 再び FPL でスコア確認
```

### 章グループと MPL タイミング

| グループ | 対象章 | MPL |
|---------|--------|-----|
| Group A | ch00〜ch04 | ch04 終了後 → MPL-1 |
| Group B | ch05〜ch08 | ch08 終了後 → MPL-2 |
| Group C | ch09〜ch12 | ch12 終了後 → MPL-3 |
| Group D | ch13〜ch16 | ch16 終了後 → FPL |

### `/start-lesson` スキル

`--agent teacher` 起動中に入力すると、進捗状況に応じた次の授業を開始します。

```
/start-lesson
```

### 生成されるファイル（gitignore 対象）

```
records/
├── progress.json           # 全体の進捗（章ごとの完了状態・理解度）
├── learning_plan.json      # FPL 後に生成される推奨学習プラン
├── .session_state.json     # セッション中の一時状態（hooks が参照）
└── sessions/               # 授業・テストのセッション記録（Markdown）

reports/
├── index.md                # MPL・FPL スコア一覧
└── YYYYMMDD_HHmmss_*.md    # 個別スコアレポート
```

---

## ディレクトリ構成

```
hmddev-cloud-learning/
├── docs/
│   ├── chapters/               # 章ごとの学習ドキュメント
│   │   ├── ch00-introduction.md
│   │   └── ...（ch00〜ch16, appA〜appC）
│   └── questions/              # 問題バンク
│       ├── domains.json        # ドメイン定義・配点・章マッピング
│       ├── ch00-introduction.json
│       └── ...                 # 章ごとの JSON ファイル
├── tools/
│   └── generate_exam.py        # 模擬試験生成ツール（CLI）
├── exams/                      # 生成された模擬試験（gitignore 対象）
├── records/                    # 学習記録（gitignore 対象）
├── reports/                    # スコアレポート（gitignore 対象）
└── .claude/
    ├── agents/
    │   └── teacher.md          # teacher エージェント定義
    ├── skills/
    │   └── start-lesson.md     # /start-lesson スキル
    ├── hooks/
    │   ├── save_progress.sh    # Stop/SessionEnd フック（進捗自動保存）
    │   └── merge_progress.py   # session_state → progress.json マージ処理
    └── templates/              # フォーマットテンプレート（エージェントが参照）
```

---

## 模擬試験の生成（CLI ツール）

`generate_exam.py` で問題バンクから試験ファイルを生成できます。

```bash
# 全単元から20問（デフォルト）
python tools/generate_exam.py

# 問題数を指定
python tools/generate_exam.py --count 30

# 特定の単元のみ出題
python tools/generate_exam.py --chapters ch09,ch10

# ドメインで絞り込み（domain1〜domain4）
python tools/generate_exam.py --domain domain2

# 試験の配点比率（24:30:34:12）に合わせて自動配分
python tools/generate_exam.py --count 50 --weighted

# シード指定（同じ出題内容を再現したいとき）
python tools/generate_exam.py --count 20 --seed 42
```

生成されたファイルは `exams/exam_YYYYMMDD_HHmmss_Nq.md` に保存されます（gitignore 対象）。

### オプション一覧

`--chapters` / `--domain` / `--weighted` は同時指定不可（排他）です。

| オプション | 省略形 | デフォルト | 説明 |
|-----------|--------|-----------|------|
| `--count` | `-n` | `20` | 出力する問題数 |
| `--chapters` | `-c` | 全単元 | 対象単元（カンマ区切り） |
| `--domain` | `-d` | | 対象ドメインID（`domain1`〜`domain4`） |
| `--weighted` | `-w` | | 配点比率に合わせて全ドメインから自動配分 |
| `--output` | `-o` | `exams/` | 出力先ディレクトリ |
| `--seed` | | なし | 乱数シード（再現用） |

### ドメイン一覧

| ドメインID | ドメイン名 | 配点 | 対応単元 |
|-----------|-----------|------|---------|
| `domain1` | クラウドのコンセプト | 24% | ch00, ch07, ch14 |
| `domain2` | セキュリティとコンプライアンス | 30% | ch09 |
| `domain3` | クラウドテクノロジーとサービス | 34% | ch01〜ch06, ch08, ch10〜ch13, ch16, appA |
| `domain4` | 請求、料金、サポート | 12% | ch15, appB |

---

## 問題の追加方法

`docs/questions/<単元ID>-*.json` の `questions` 配列に追記します。

**択一選択問題（`type: "single"`）**

```json
{
  "id": "ch01-001",
  "type": "single",
  "domain": "第3分野: クラウドテクノロジーとサービス",
  "text": "問題文をここに書く",
  "choices": {
    "A": "選択肢A",
    "B": "選択肢B",
    "C": "選択肢C",
    "D": "選択肢D"
  },
  "answer": "B",
  "explanation": "解説文をここに書く"
}
```

**複数選択問題（`type: "multi"`）**
5択から2つ選ぶ形式。`answer` を配列にし、`choices` に E を加えます。

```json
{
  "id": "ch09-010",
  "type": "multi",
  "domain": "第2分野: セキュリティとコンプライアンス",
  "text": "〜を2つ選んでください。",
  "choices": {
    "A": "選択肢A",
    "B": "選択肢B",
    "C": "選択肢C",
    "D": "選択肢D",
    "E": "選択肢E"
  },
  "answer": ["A", "C"],
  "explanation": "解説文をここに書く"
}
```

> `type` を省略した場合は `"single"` として扱われます。
