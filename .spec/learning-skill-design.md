# learning スキル 詳細設計（v5）

## 設計方針の確定

| 項目 | 決定内容 |
|------|---------|
| エントリポイント | `claude --agent teacher`（teacher エージェントを直接起動） |
| `/start-lesson` スキル | 授業開始・再開用スキル（teacher セッション内で使用） |
| テストモード | 対話形式が基本。ファイル生成はユーザーオーダー時のみ |
| テスト記録 | `records/` に保存（学習プラン生成時に参照） |
| 理解度スコア表示 | 記録専用（口語で伝えるのみ、A/B/C は明示しない） |
| 休憩提案 | 5セクション消化 or ディスカッションが長引いた時に提案 |
| 進捗の自動保存 | teacher エージェントのフロントマターに Hooks を定義 |
| IT初心者チェック | 初回起動時に確認 → 初心者なら appA を ch00 の前に挿入 |
| MPL | 3回（ch04・ch08・ch12 完了後） |
| FPL | 1回（ch16 完了後・30問・本番配分） |
| FPL 再受験 | 学習プラン消化後に提案、スコアを progress.json に蓄積 |
| スコアレポート | MPL・FPL 完了後に `reports/` 配下へ Markdown レポートを自動生成 |

---

## テスト種別の全体像

| テスト種別 | トリガー | 問題数 | 出題範囲 | レポート |
|-----------|---------|--------|---------|---------|
| Quick Test | ユーザーオーダー | **最大5問・固定** | 指定章・ドメイン | なし |
| MPL-1 | ch04 完了後に自動提案 | 10問 | ch00〜ch04 | ✓ |
| MPL-2 | ch08 完了後に自動提案 | 10問 | ch05〜ch08 | ✓ |
| MPL-3 | ch12 完了後に自動提案 | 10問 | ch09〜ch12 | ✓ |
| Final Progress Lesson | ch16 完了後に自動提案 | 30問 | ch00〜ch16（本番配分） | ✓ |

---

## 章グループ定義

章の配分はセクション数で均等になるよう設計（各グループ 31〜40 セクション）。

| グループ | 章 | セクション数 | 問題バンク | テーマ |
|---------|---|------------|----------|-------|
| Group A | ch00〜ch04 | 40 | 約127問 | クラウド基礎・コンピューティング・データ |
| Group B | ch05〜ch08 | 31 | 約105問 | ネットワーク・アーキテクチャパターン |
| Group C | ch09〜ch12 | 34 | 約155問 | セキュリティ・運用・開発・分析 |
| Group D | ch13〜ch16 | 31 | 約75問 | AI/ML・移行・コスト・その他 |
| 付録 | appA〜appC | — | — | IT前提知識・サポート・試験対策 |

---

## 学習フローの全体像

```
初回起動
    │
    ▼
「IT初心者ですか？」
    ├── YES → appA（ネットワーク基礎）を先に受講
    └── NO  → ch00 からスタート
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ フェーズ1: 初回学習                                    │
│                                                      │
│  [Group A]  ch00 → ch01 → ch02 → ch03 → ch04        │
│                                    ↓                 │
│                        MPL-1（10問・ch00-ch04）       │
│                                                      │
│  [Group B]  ch05 → ch06 → ch07 → ch08               │
│                                    ↓                 │
│                        MPL-2（10問・ch05-ch08）       │
│                                                      │
│  [Group C]  ch09 → ch10 → ch11 → ch12               │
│                                    ↓                 │
│                        MPL-3（10問・ch09-ch12）       │
│                                                      │
│  [Group D]  ch13 → ch14 → ch15 → ch16               │
│                                    ↓                 │
│                     Final Progress Lesson（30問）     │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ フェーズ2: 推奨学習プラン                               │
│                                                      │
│  FPL結果 + MPL記録 + 授業理解度 → 優先度付き復習プラン  │
│  保存: records/learning_plan.json                    │
│                                                      │
│  プランに従い苦手章を授業 → Quick Test（5問）で定着確認  │
│  全章消化後 → FPL 再受験を提案（スコアを蓄積）          │
└─────────────────────────────────────────────────────┘
```

---

## アーキテクチャ全体図

```
$ claude --agent teacher
        │
        ▼
teacher エージェント（プライマリエージェントとして起動）
  ├── Hooks（フロントマターに定義）
  │     ├── Stop      → save_progress.sh（各ターン応答後・非同期）
  │     └── SessionEnd → save_progress.sh（セッション終了時・同期）
  │
  ├── 起動時の状態判定
  │     ├── learning_plan.json が存在 → フェーズ2モード
  │     └── 存在しない → フェーズ1モード
  │
  ├── フェーズ1
  │     ├── 初回のみ: IT初心者チェック
  │     ├── /start-lesson → 授業フロー（appA 挿入考慮）
  │     ├── ch04/ch08/ch12 完了検知 → MPL 自動提案
  │     ├── ch16 完了検知 → FPL 提案 → 学習プラン生成
  │     └── Quick Test → 最大5問
  │
  └── フェーズ2
        ├── learning_plan.json の次の pending 章を提案
        ├── 復習授業（focus_sections に重点）
        ├── Quick Test（5問）で定着確認
        └── 全章完了後 → FPL 再受験を提案
```

---

## ファイル構成

```
.claude/
  agents/
    teacher.md               # プライマリエージェント定義（Hooks 含む）
  skills/
    start-lesson.md          # 授業開始スキル（/start-lesson で起動）
  hooks/
    save_progress.sh         # 進捗の自動保存スクリプト
    merge_progress.py        # .session_state.json → progress.json マージ

records/
  progress.json              # 全章の進捗トラッカー（授業・テスト共用）
  learning_plan.json         # FPL 後に生成される推奨学習プラン
  .session_state.json        # セッション中の一時状態（Hooks が読み取る）
  sessions/
    YYYYMMDD_HHmmss_appA_lesson.md      # appA 授業記録
    YYYYMMDD_HHmmss_chXX_lesson.md      # 授業セッション記録
    YYYYMMDD_HHmmss_quick_test.md       # Quick Test 記録
    YYYYMMDD_HHmmss_mpl1.md             # MPL-1 記録
    YYYYMMDD_HHmmss_mpl2.md             # MPL-2 記録
    YYYYMMDD_HHmmss_mpl3.md             # MPL-3 記録
    YYYYMMDD_HHmmss_fpl.md              # FPL 記録（複数回分が蓄積）

reports/
  YYYYMMDD_HHmmss_mpl1.md          # MPL-1 スコアレポート
  YYYYMMDD_HHmmss_mpl2.md          # MPL-2 スコアレポート
  YYYYMMDD_HHmmss_mpl3.md          # MPL-3 スコアレポート
  YYYYMMDD_HHmmss_fpl_attempt1.md  # FPL スコアレポート（回数付き）
  YYYYMMDD_HHmmss_fpl_attempt2.md  # FPL 再受験レポート
  index.md                         # 全レポートの一覧（自動更新）

docs/chapters/               # 授業コンテンツ（読み取り専用）
docs/questions/              # 問題バンク（読み取り専用）
tools/generate_exam.py       # テストファイル生成（オーダー時のみ使用）
exams/                       # 生成テストファイルの出力先
```

---

## teacher エージェント仕様（.claude/agents/teacher.md）

### フロントマター

```yaml
---
name: teacher
description: AWS Cloud Practitioner の授業・テストを行う教師エージェント
model: opus
color: blue
memory: project
hooks:
  Stop:
    - hooks:
        - type: command
          command: bash "$CLAUDE_PROJECT_DIR/.claude/hooks/save_progress.sh"
          async: true
          statusMessage: "進捗を保存中..."
  SessionEnd:
    - hooks:
        - type: command
          command: bash "$CLAUDE_PROJECT_DIR/.claude/hooks/save_progress.sh"
---
```

### キャラクター設定

- IT 初心者・クラウド未経験者を相手にする、親しみやすい教師
- 専門用語を使う際は必ず平易な言葉で補足する
- 「わからない」と言いやすい雰囲気を作る
- 正しく答えられなくても否定せず、一緒に考えながら理解を深める

### 起動時の状態判定

```
teacher 起動
    │
    ├── records/learning_plan.json が存在する
    │     → フェーズ2モード
    │       「前回の学習プランが残っています。復習を続けますか？」
    │
    └── 存在しない
          → フェーズ1モード
          │
          ├── progress.json が存在しない（初回）
          │     → IT初心者チェック（下記）
          │
          └── progress.json が存在する（再開）
                → 「授業しますか？テストしますか？」
```

### IT初心者チェック（初回のみ）

```
「AWSの学習を始める前に少し確認させてください。
 ネットワークやサーバーについての基礎知識はありますか？」

    ├── 「あまりない」「初心者」
    │     → progress.json に it_beginner: true を記録
    │       「では最初に、AWSを理解するための
    │        ネットワーク基礎（付録A）から始めましょう！」
    │       → appA-networking-basics.md を授業
    │       → 完了後 ch00 へ
    │
    └── 「ある程度知っている」「スキップしたい」
          → progress.json に it_beginner: false を記録
            → ch00 から開始
```

appB（サポートプラン）・appC（試験対策）は任意受講扱い。
ユーザーから「サポートプランについて学びたい」「試験対策をしたい」と言われたときのみ対応する。

### MPL・FPL の自動提案

章完了後のチェック（各章の授業終了時）:

```
ch04 完了 → 「Group A が終わりました！MPL-1（10問）で確認しませんか？」
ch08 完了 → 「Group B が終わりました！MPL-2（10問）で確認しませんか？」
ch12 完了 → 「Group C が終わりました！MPL-3（10問）で確認しませんか？」
ch16 完了 → 「全章が終わりました！Final Progress Lesson（30問）でまとめましょう！」
```

断った場合は次の章へ。後から「MPLをやりたい」と言われれば対応し `mpl_skipped` を解除する。

---

## start-lesson スキル仕様（.claude/skills/start-lesson.md）

### フロントマター

```yaml
---
name: start-lesson
description: 授業を開始または再開するスキル
---
```

### フェーズによる動作の違い

```
/start-lesson 起動
    │
    ├── フェーズ1
    │     └── 通常の開始点決定フロー
    │           ├── 「続きから」→ progress.json を読んで再開位置を特定
    │           └── 「章を指定する」→ 章の一覧を提示
    │
    └── フェーズ2
          └── learning_plan.json を読み込んで次の pending 章を提案
              「次は ◯◯ の復習をしましょう（理由: △△）」
```

### 開始点の決定（フェーズ1）

```
progress.json を読む
    ├── it_beginner: true で appA が未完了 → appA を提案
    ├── in_progress の章がある → last_section_index + 1 から再開
    ├── in_progress がない → 最後の completed の次の章を提案
    └── progress.json がない（初回）→ IT初心者チェックへ戻る
```

---

## 授業フロー詳細

### 1セクションの進め方

```
1. 予告: 「これから ◯◯ を話します」（1文）
2. 解説: 口語・比喩交じりで説明（ドキュメントをそのまま読まない）
3. .session_state.json に現在のセクション index を書き込む  ← Hook の保存対象
4. 確認質問: 1〜2問（パターン表から選択）
5. ユーザー回答
6. 即時フィードバック（正誤・補足・称賛）
7. .session_state.json に理解度スコアを追記
8. 次のセクションへ
```

### 確認質問パターン

| パターン | 例 |
|---------|---|
| 言語化 | 「EC2 を使ったことがない人に説明するとしたら、どう言いますか？」 |
| 比較 | 「オンデマンドとリザーブドはどう使い分けますか？」 |
| 適用 | 「突然アクセスが10倍になるかもしれない場合、どの機能が役立ちますか？」 |
| 穴埋め | 「CloudFront を使うと _____ が解決できます。何でしょう？」 |
| 想起 | 「今日出てきたサービスを思い出せる範囲で挙げてみてください」 |

フェーズ2の復習授業で `focus_sections` に指定されたセクションは確認質問を **2問**（通常の2倍）にする。

### 休憩提案のトリガー

- 5セクション連続で消化したとき
- 1セクションの質疑がディスカッションに発展し長くなっているとき

### 章末フィードバック

1. **ポジティブ評価**（必ず最初・具体的に）
2. **理解度の自然な言語表現**（A/B/C の記号は使わない）
3. **苦手ポイントへのアドバイス**（あれば）
4. **次のステップ推奨**（MPL 提案があれば合わせて告知）

---

## テストフロー詳細

### Quick Test（最大5問・固定）

```
1. 範囲を確認（全単元 / 特定の章 / 特定のドメイン）
2. docs/questions/ から最大5問をランダム選択
3. 1問ずつ出題 → 回答 → 即時フィードバック
4. 全問終了後: 正答率 + 簡単なコメント
5. sessions/YYYYMMDD_HHmmss_quick_test.md に保存
```

### MPL-1（10問・ch00〜ch04）

```
1. ch00〜ch04 の問題バンクから10問をランダム選択
   （5章から均等配分: 2問 × 5章を基本とし、問題数が少ない章は調整）
2. 1問ずつ出題 → 回答 → 即時フィードバック
3. 全問終了後:
   a. 正答率・苦手トピックを口頭でフィードバック
   b. 「Group B（ネットワーク〜コンテナ）に向けてのアドバイス」
4. sessions/YYYYMMDD_HHmmss_mpl1.md に保存
5. progress.json の mpl1 フィールドを更新
6. reports/YYYYMMDD_HHmmss_mpl1.md にスコアレポートを生成  ← 追加
7. reports/index.md を更新  ← 追加
```

### MPL-2（10問・ch05〜ch08）/ MPL-3（10問・ch09〜ch12）

MPL-1 と同形式。各グループの章から均等配分で出題。

| MPL | 出題範囲 | アドバイスの方向 |
|-----|---------|----------------|
| MPL-1 | ch00〜ch04 | Group B（ネットワーク・アーキテクチャ）に向けて |
| MPL-2 | ch05〜ch08 | Group C（セキュリティ・運用）に向けて |
| MPL-3 | ch09〜ch12 | Group D（AI/ML・移行・コスト）に向けて |

### Final Progress Lesson（FPL・30問）

```
1. ch00〜ch16 の問題バンクから30問を本番配分で選択
   domain1: 7問（24%）、domain2: 9問（30%）、
   domain3: 10問（34%）、domain4: 4問（12%）
2. 1問ずつ出題 → 回答 → 即時フィードバック
3. 全問終了後:
   a. 正答率・ドメイン別得点率を口頭でフィードバック
   b. 苦手分野の詳細まとめ
   c. お疲れ様メッセージ
4. sessions/YYYYMMDD_HHmmss_fpl.md に保存
5. progress.json の fpl_history[] に追記（複数回分を蓄積）
6. reports/YYYYMMDD_HHmmss_fpl_attempt{n}.md にスコアレポートを生成  ← 追加
7. reports/index.md を更新  ← 追加
8. 推奨学習プランを自動生成（下記）
```

**FPL は複数回分のスコアを progress.json に配列で蓄積する。**

### ファイル生成テスト（オーダー時のみ）

```
全単元・20問:         python tools/generate_exam.py -n 20
特定章・10問:         python tools/generate_exam.py -n 10 -c ch01
ドメイン指定・30問:   python tools/generate_exam.py -n 30 -d domain2
本番配分・65問:       python tools/generate_exam.py -n 65 -w
```

---

## スコアレポート設計

MPL・FPL の完了後、teacher エージェントが Write ツールで `reports/` 配下に Markdown レポートを生成する。ユーザーがいつでも見返せる「自己学習の記録」として機能する。

### ファイル命名規則

| テスト | ファイル名 |
|--------|----------|
| MPL-1 | `reports/YYYYMMDD_HHmmss_mpl1.md` |
| MPL-2 | `reports/YYYYMMDD_HHmmss_mpl2.md` |
| MPL-3 | `reports/YYYYMMDD_HHmmss_mpl3.md` |
| FPL（1回目） | `reports/YYYYMMDD_HHmmss_fpl_attempt1.md` |
| FPL（2回目以降） | `reports/YYYYMMDD_HHmmss_fpl_attempt2.md`（連番） |
| レポート一覧 | `reports/index.md`（MPL/FPL のたびに追記） |

---

### スコアバッジ定義（全テスト共通）

正答率に応じて以下のバッジをレポートの冒頭に表示する。

| 正答率 | バッジ | 意味 |
|--------|--------|------|
| 90%以上 | `[EXCELLENT]` | 完璧に近い理解 |
| 70%以上 | `[PASS]` | 試験合格ライン突破 |
| 50%以上 | `[REVIEW]` | 要復習 |
| 50%未満 | `[RETRY]` | 集中的な復習が必要 |

FPL は試験合格ライン（700/1000 = 70%）に直接対応する。

スコアバーはテキストで可視化する（絵文字は使わない）:
```
正答率: 70%  [███████░░░]  7 / 10
```

---

### MPL スコアレポート構成

#### セクション一覧

| # | セクション | 内容 |
|---|-----------|------|
| 1 | ヘッダー | テスト種別・対象範囲・実施日時 |
| 2 | 総合スコア | バッジ・正答率・スコアバー |
| 3 | 章別スコア | 各章の出題数・正答数・正答率（表） |
| 4 | 苦手トピック分析 | 不正解問題のトピック一覧・復習推奨セクション |
| 5 | 問題別詳細 | 全問の正誤・正解・解説（折りたたみ） |
| 6 | 次グループへのアドバイス | 次の Group で注意すべき点 |

#### MPL レポートテンプレート

```markdown
# MPL-1 スコアレポート — Group A（ch00〜ch04）

**実施日時**: 2026-03-23 11:00
**対象範囲**: ch00 クラウド基礎 〜 ch04 データベース設計
**問題数**: 10問

---

## 総合スコア

[PASS] 試験合格ライン突破！

正答率: 80%  [████████░░]  8 / 10

---

## 章別スコア

| 章 | タイトル | 出題数 | 正答数 | 正答率 |
|----|---------|--------|--------|--------|
| ch00 | クラウドの基本概念 | 2 | 2 | 100% |
| ch01 | Webホスティング | 2 | 1 | 50% |
| ch02 | サーバーレス | 2 | 2 | 100% |
| ch03 | ストレージ戦略 | 2 | 2 | 100% |
| ch04 | データベース設計 | 2 | 1 | 50% |

---

## 苦手トピック分析

以下のトピックで不正解がありました。次のグループに進む前に確認しておきましょう。

| トピック | 章 | 対応セクション |
|---------|---|--------------|
| EC2購入オプションの使い分け | ch01 | 1-3. EC2の購入オプション |
| Aurora と RDS の違い | ch04 | 4-2. Amazon Aurora |

**復習推奨セクション**:
- ch01: `1-3. EC2の購入オプション（オンデマンド / リザーブド / Savings Plans）`
- ch04: `4-2. Amazon Aurora ― 高性能RDB`

---

## 問題別詳細

<details>
<summary>問題1（ch01-q05）— 正解 ✓</summary>

**問題**: EC2のオンデマンドインスタンスの特徴として正しいものはどれですか？

**あなたの回答**: A. 使った分だけ秒単位で課金される
**正解**: A

**解説**: オンデマンドインスタンスは...

</details>

<details>
<summary>問題2（ch01-q12）— 不正解 ✗</summary>

**問題**: 1年間の継続利用を前提にコストを削減したい場合、最適な購入オプションはどれですか？

**あなたの回答**: A. オンデマンド
**正解**: B. リザーブドインスタンス

**解説**: リザーブドインスタンスは1年または3年の利用を約束することで...

</details>

<!-- 残りの問題も同形式 -->

---

## Group B に向けてのアドバイス

（teacher エージェントが生成するテキスト）

Group B ではネットワーク設計（ch05）が最初の山場です。
VPC・セキュリティグループ・NACLの使い分けは試験頻出なので、
ch01で学んだセキュリティグループの概念を思い出しながら進めましょう。

---

*このレポートは AWS Cloud Practitioner 学習システムによって自動生成されました。*
```

---

### FPL スコアレポート構成

MPL との差分のみ記載する。

#### MPL から追加されるセクション

| # | セクション | 内容 |
|---|-----------|------|
| 3 | ドメイン別スコア | 4ドメインの出題数・正答数・正答率（試験配点との対比） |
| 7 | 試験合格ライン分析 | 70%ラインとの差・あと何問正解すれば合格水準か |
| 8 | 前回比較 | 2回目以降のみ表示。前回との差分（+/-） |
| 9 | 推奨学習プラン概要 | learning_plan.json の top-3 章を抜粋 |

#### ドメイン別スコアの表示例

```markdown
## ドメイン別スコア

| ドメイン | 配点 | 出題数 | 正答数 | 正答率 | スコアバー |
|---------|------|--------|--------|--------|-----------|
| 第1分野: クラウドのコンセプト | 24% | 7問 | 5問 | 71% | [███████░░░] |
| 第2分野: セキュリティ | 30% | 9問 | 4問 | 44% | [████░░░░░░] |
| 第3分野: テクノロジーとサービス | 34% | 10問 | 7問 | 70% | [███████░░░] |
| 第4分野: 請求・料金・サポート | 12% | 4問 | 3問 | 75% | [████████░░] |
```

#### 試験合格ライン分析の表示例

```markdown
## 試験合格ライン分析

AWS Cloud Practitioner の合格ライン: **700 / 1000（70%）**

あなたの今回の結果: **63%**（19 / 30問正解）

合格ラインまで: あと **2問** 正解が必要です

> セキュリティドメイン（第2分野）の正答率が44%と低く、
> このドメインは試験の30%を占めます。集中的な復習で
> 合格ラインに届く可能性が高いです。
```

#### 前回比較の表示例（2回目以降）

```markdown
## 前回との比較（Attempt 1 → Attempt 2）

| 項目 | 前回 | 今回 | 変化 |
|------|------|------|------|
| 総合 | 63% | 73% | +10% |
| 第1分野 | 71% | 80% | +9% |
| 第2分野 | 44% | 60% | +16% |
| 第3分野 | 70% | 72% | +2% |
| 第4分野 | 75% | 75% | 0% |

> 第2分野（セキュリティ）が大きく改善しています！
> 学習プランの効果が出ています。
```

---

### reports/index.md（自動更新）

MPL・FPL のたびにエントリを追記する。

```markdown
# スコアレポート一覧

## MPL（Middle Progress Lesson）

| テスト | 実施日 | 正答率 | バッジ | レポート |
|--------|--------|--------|--------|---------|
| MPL-1（ch00-ch04） | 2026-03-23 | 80% | [PASS] | [レポートを開く](20260323_110000_mpl1.md) |
| MPL-2（ch05-ch08） | — | — | — | 未実施 |
| MPL-3（ch09-ch12） | — | — | — | 未実施 |

## FPL（Final Progress Lesson）

| 受験回 | 実施日 | 正答率 | バッジ | レポート |
|--------|--------|--------|--------|---------|
| Attempt 1 | 2026-03-24 | 63% | [REVIEW] | [レポートを開く](20260324_140000_fpl_attempt1.md) |
```

---

### レポート生成のタイミング

テスト完了後、teacher エージェントが以下の順序で実行する:

```
テスト全問終了
    │
    ▼
口頭フィードバック（会話内でスコアを伝える）
    │
    ▼
sessions/ にセッション記録を保存
    │
    ▼
reports/ にスコアレポートを生成（Write ツール）
    │
    ▼
reports/index.md を更新（Edit ツール）
    │
    ▼
「レポートを reports/XXXX.md に保存しました」と通知
    │
    ▼（FPL のみ）
推奨学習プランを生成
```

---

## 推奨学習プランの生成（FPL 完了後）

### 生成ロジック

```
入力データ:
  - FPL のドメイン別得点率・問題別正誤
  - MPL-1〜3 の記録（あれば）
  - progress.json の各章 understanding_score
  - 授業セッション記録の理解度メモ

優先度スコア（章ごとに算出）:
  score = (1 - test_accuracy) × 0.6
        + (lesson_score_weight) × 0.4
  ※ lesson_score_weight: A=0, B=0.5, C=1.0

上位章を priority 順に並べて learning_plan.json を生成。
スコアが同点の場合は試験ドメインの配点（domain2=30% など）が高い章を優先。
```

### learning_plan.json のフォーマット

```json
{
  "created_at": "2026-03-24T12:00:00",
  "based_on_fpl": "sessions/20260324_140000_fpl.md",
  "fpl_score_rate": 0.63,
  "plan": [
    {
      "priority": 1,
      "chapter": "ch09",
      "chapter_title": "第9章 セキュリティとアクセス管理",
      "reason": "FPL でセキュリティドメインの正答率が40%",
      "focus_sections": [
        "IAMポリシーの仕組み",
        "KMSとSecrets Managerの使い分け"
      ],
      "status": "pending"
    },
    {
      "priority": 2,
      "chapter": "ch05",
      "chapter_title": "第5章 ネットワーク設計",
      "reason": "授業理解度C、FPL でも複数問不正解",
      "focus_sections": [
        "セキュリティグループとネットワークACLの違い"
      ],
      "status": "pending"
    }
  ],
  "completed_reviews": []
}
```

`status` の値: `pending` / `in_progress` / `completed`

---

## フェーズ2: 推奨プランに従った復習

### 流れ

```
teacher 起動（フェーズ2）
    │
    ▼
learning_plan.json の次の pending 章を提案
「◯◯ の復習をしましょう。理由: △△。特に △△ セクションを重点的に。」
    │
    ▼
/start-lesson → focus_sections を重点にした授業
（focus_sections は確認質問2問）
    │
    ▼
章の授業終了 → Quick Test（5問・その章の問題）で定着確認
    │
    ▼
learning_plan.json の status を completed に更新
    │
    ▼
次の pending 章へ

    ↓ 全章 completed になったら

「お疲れ様でした！学習プランを全て消化しました。
 もう一度 Final Progress Lesson（30問）に挑戦してスコアを確認しますか？」

    └── YES → FPL 再受験（スコアを progress.json に追記）
    └── NO  → 終了
```

---

## Hooks 設計

### save_progress.sh

```bash
#!/usr/bin/env bash
CHECKPOINT="$CLAUDE_PROJECT_DIR/records/.session_state.json"
PROGRESS="$CLAUDE_PROJECT_DIR/records/progress.json"

[ -f "$CHECKPOINT" ] || exit 0

if [ ! -f "$PROGRESS" ]; then
  echo '{"last_updated":"","it_beginner":null,"chapters":{},"quick_tests":[],
        "mpl1":null,"mpl2":null,"mpl3":null,"fpl_history":[]}' > "$PROGRESS"
fi

python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/merge_progress.py" \
  "$CHECKPOINT" "$PROGRESS"
```

### merge_progress.py の処理分岐

| `.session_state.json` の `type` | マージ先 |
|--------------------------------|---------|
| `"lesson"` | `chapters[chapter_id]` の status・last_section_index・section_scores を更新 |
| `"quick_test"` | `quick_tests[]` に追記 |
| `"mpl1"` / `"mpl2"` / `"mpl3"` | `mpl1` / `mpl2` / `mpl3` フィールドを上書き（再受験時は履歴配列に変更を検討） |
| `"fpl"` | `fpl_history[]` に追記（複数回分を蓄積） |

`completed` 済み章は status を上書きしない。

---

## records フォーマット仕様

### progress.json

```json
{
  "last_updated": "2026-03-24T12:00:00",
  "it_beginner": true,
  "chapters": {
    "appA": {
      "status": "completed",
      "last_section_index": 6,
      "understanding_score": "A",
      "sessions": ["sessions/20260320_090000_appA_lesson.md"]
    },
    "ch00": { "status": "completed", ... },
    "ch01": { "status": "in_progress", "last_section_index": 4, ... },
    "ch02": { "status": "not_started", ... }
  },
  "quick_tests": [
    {
      "date": "2026-03-22T11:30:00",
      "scope": "ch01",
      "total": 5, "correct": 4, "score_rate": 0.8,
      "session_file": "sessions/20260322_113000_quick_test.md"
    }
  ],
  "mpl1": {
    "date": "2026-03-23T11:00:00",
    "scope": "ch00-ch04",
    "total": 10, "correct": 8, "score_rate": 0.8,
    "weak_sections": ["CloudFrontの仕組み"],
    "session_file": "sessions/20260323_110000_mpl1.md"
  },
  "mpl2": null,
  "mpl3": null,
  "fpl_history": [
    {
      "attempt": 1,
      "date": "2026-03-24T14:00:00",
      "total": 30, "correct": 19, "score_rate": 0.63,
      "domain_scores": {
        "domain1": 0.70, "domain2": 0.40,
        "domain3": 0.65, "domain4": 0.75
      },
      "weak_sections": ["IAMポリシー", "KMSとSecrets Manager", "VPC設計"],
      "session_file": "sessions/20260324_140000_fpl.md"
    }
  ]
}
```

### セッション記録: sessions/YYYYMMDD_HHmmss_mpl1.md（MPL 共通形式）

```markdown
---
type: mpl1
scope: ch00-ch04
session_date: 2026-03-23T11:00:00
total: 10
correct: 8
score_rate: 0.80
---

## 結果サマリ
正答率: 8 / 10（80%）

## 章別得点

| 章 | 出題数 | 正答数 |
|----|--------|--------|
| ch00 | 2 | 2 |
| ch01 | 2 | 1 |
...

## 苦手トピック
- CloudFrontの仕組み

## Group B に向けてのアドバイス
...
```

### セッション記録: sessions/YYYYMMDD_HHmmss_fpl.md

MPL と同形式（`type: fpl`）。`attempt` フィールドを追加し、再受験回数を明示する。

---

## エラーハンドリング

| 状況 | 対応 |
|------|------|
| `progress.json` が存在しない | IT初心者チェックへ。チェック後に progress.json を初期作成 |
| 章ファイルが見つからない | ユーザーに伝え、別の章を提案 |
| `.session_state.json` が壊れている | `save_progress.sh` がスキップ（`exit 0`）、stderr にログのみ |
| `generate_exam.py` がエラー終了 | エラー内容を伝え、オプション変更で再試行を促す |
| 問題バンクが空 | 「この章の問題はまだ登録されていません」と伝え、別の範囲を提案 |
| MPL/FPL をスキップした | `mpl1_skipped: true` 等を progress.json に記録。後から対応可能 |
| learning_plan.json の全章が completed | FPL 再受験を提案。断られたら学習完了を伝えて終了 |

---

## 未決事項・今後の拡張候補

| 項目 | 内容 |
|------|------|
| appB・appC の受講タイミング | 任意受講だが、FPL 前に「サポートプランを確認しておきますか？」と促すのも手 |
| MPL の再受験 | 後から「MPL-1 をやり直したい」と言われた場合、記録は別エントリとして追記 |
| ハンズオンモード | AWS CLI を使った実機確認（plan.md に記載あり） |
| 理解度グラフ | FPL の複数回スコア推移の可視化 |
