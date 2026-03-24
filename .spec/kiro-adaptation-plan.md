# Kiro IDE 対応計画書

## 概要

Claude Code 用に構築した学習システム（teacher エージェント・start-lesson スキル・進捗保存フック）を
Kiro IDE で利用可能な形式に変換する。

---

## システム対応マッピング

| Claude Code | Kiro 相当物 | 変換方針 |
|-------------|-------------|---------|
| `.claude/agents/teacher.md` | `.kiro/powers/aws-cloud-learning/` | Power として再構成 |
| `.claude/skills/start-lesson/SKILL.md` | `.kiro/skills/start-lesson/SKILL.md` | ほぼそのままコピー（同一標準） |
| `.claude/hooks/save_progress.sh` | `.kiro/hooks/save-progress.kiro.hook` | Agent Stop フックとして変換 |
| `.claude/hooks/merge_progress.py` | 変更なし（フックから呼び出す） | スクリプト再利用 |
| `.claude/templates/` | 変更なし（Power の steering から参照） | そのまま残す |
| `AGENTS.md` | `.kiro/steering/aws-cloud-learning.md` | Kiro は AGENTS.md を直接サポート（流用可能） |

---

## 変更ファイル一覧

### 新規作成（`.kiro/` 配下）

```
.kiro/
├── steering/
│   └── aws-cloud-learning.md           # 常時読み込みの文脈（既存 AGENTS.md から流用）
├── skills/
│   └── start-lesson/
│       └── SKILL.md                    # そのままコピー（Agent Skills 共通標準）
├── hooks/
│   └── save-progress.kiro.hook         # Agent Stop フック（進捗自動保存）
└── powers/
    └── aws-cloud-learning/
        ├── POWER.md                    # Power の起動条件・オンボーディング
        └── steering/
            ├── teacher-persona.md      # キャラクター・基本原則・起動時動作
            ├── lesson-flow.md          # 授業フロー（セクション進行・休憩提案）
            ├── test-flow.md            # Quick Test / MPL / FPL の実施手順
            └── reporting.md            # スコアレポート・学習プラン生成
```

### 変更なし（Claude Code 用ファイルを共存させる）

```
.claude/                      # Claude Code 用設定をそのまま保持
records/                      # 学習記録（両環境共通・gitignore 対象）
reports/                      # スコアレポート（両環境共通・gitignore 対象）
```

---

## 各ファイルの詳細設計

### 1. `.kiro/powers/aws-cloud-learning/POWER.md`

Power の起動トリガーとなるキーワード・オンボーディング手順を記述する。

```yaml
---
name: "aws-cloud-learning"
displayName: "AWS Cloud Practitioner 学習システム"
description: "AWS CLF-C02 試験対策の対話型学習。授業・テスト・スコアレポート・学習プランを提供する"
keywords: ["AWS", "Cloud Practitioner", "CLF-C02", "授業", "レッスン", "テスト", "MPL", "FPL", "学習", "study", "exam"]
---
```

本文にはオンボーディング手順（初回確認・フェーズ判定）と、steering/ 各ファイルへの参照を記述する。

### 2. `.kiro/powers/aws-cloud-learning/steering/` の分割方針

`teacher.md`（621行）を 4 ファイルに分割してコンテキスト効率を改善する。

| ファイル | 内容 | 元の行範囲（参考） |
|---------|------|------------------|
| `teacher-persona.md` | キャラクター・起動時判定・IT 初心者チェック | L24〜L80 |
| `lesson-flow.md` | 授業進行・セクション・章末処理・MPL/FPL 提案 | L83〜L235 |
| `test-flow.md` | Quick Test / MPL / FPL の実施・問題配分 | L238〜L373 |
| `reporting.md` | スコアレポート生成・学習プラン算出・フェーズ2 | L375〜L621 |

Kiro の steering では `inclusion: auto` を指定して関連タスク時のみ読み込む設計にする。

### 3. `.kiro/skills/start-lesson/SKILL.md`

Claude Code のスキルと Kiro のスキルは**同一の Agent Skills オープン標準**を採用している。
`.claude/skills/start-lesson/SKILL.md` を `.kiro/skills/start-lesson/SKILL.md` にコピーするだけで動作する。
frontmatter の `name` / `description` は変更不要。

### 4. `.kiro/steering/aws-cloud-learning.md`

常時読み込む文脈として既存の `AGENTS.md` を流用する。
Kiro は `AGENTS.md`（ワークスペースルート）を直接サポートしているため、
追加で `.kiro/steering/` に配置する場合は `inclusion: always` を指定する。

### 5. `.kiro/hooks/save-progress.kiro.hook`

`.kiro.hook` ファイルは **JSON 形式**。`when.type` に使えるのは
`fileEdited` / `fileCreated` / `fileDeleted` / `userTriggered` のみ。

Claude Code の `Stop`（ターン完了後）に相当するトリガーは **IDE フックには存在しない**。
代替策として `.session_state.json` の書き込みを `fileEdited` で検知する方式を採用する。

```json
{
  "name": "AWS Learning Progress Saver",
  "description": "session_state.json が更新されたとき progress.json へマージして進捗を保存する",
  "version": "1",
  "when": {
    "type": "fileEdited",
    "patterns": ["records/.session_state.json"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "records/.session_state.json が更新されました。.claude/hooks/save_progress.sh を実行して progress.json へ進捗をマージしてください。"
  }
}
```

> Claude Code では Stop/SessionEnd フックでスクリプトを直接実行していたが、
> Kiro IDE フックの `then.type: askAgent` はエージェント経由の実行になる点に注意。
> スクリプトを直接実行したい場合は Kiro CLI エージェントフック（`stop` ライフサイクル）を検討する。

---

## 対応しない項目（スコープ外）

| 項目 | 理由 |
|------|------|
| `mcp.json` | MCP サーバーは不使用（ドキュメント参照のみ） |
| SessionEnd フック | Kiro IDE フックに同等のトリガーなし（`fileEdited` で `.session_state.json` を監視して代替） |
| `memory: project` | Kiro のメモリ管理は steering で代替 |
| `model: opus` | Kiro のモデル選択は設定画面で行う |
| ファイル書き込みの事前承認 | IDE の CLI エージェント設定（`allowedTools`）は IDE モードで使えない。**ユーザーが Kiro の IDE 設定 UI から `records/` と `reports/` への書き込みを手動で許可する**必要がある。POWER.md のオンボーディングセクションにその手順を記載する。 |

---

## 実装順序

1. `.kiro/skills/start-lesson/SKILL.md` — コピーのみ・即動作確認可能
2. `.kiro/steering/aws-cloud-learning.md` — AGENTS.md を流用して常時文脈を確立
3. `.kiro/powers/aws-cloud-learning/POWER.md` — Power の起動トリガー作成
4. `.kiro/powers/aws-cloud-learning/steering/` — teacher.md を 4 分割して作成
5. `.kiro/hooks/save-progress.kiro.hook` — `.session_state.json` 更新を監視するフック

---

## 留意事項

- `records/` と `reports/` は `.gitignore` 設定済み。Kiro でも同じパスを使用するため変更不要。
- `.claude/` 配下は削除せず共存させる（Claude Code / Kiro の両環境で利用可能）。
- `.kiro.hook` ファイルの正確なスキーマは実装前に Kiro の UI で確認すること。
