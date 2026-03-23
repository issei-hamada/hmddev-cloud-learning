---
name: Chapter document style and structure
description: Established format for learning chapters - heading structure, section numbering, exam tips, quiz format
type: project
---

各章のドキュメントは以下の共通構造に従う:
- タイトル: `# 第N章　タイトル ― サブタイトル`
- メタ情報: 対応試験ドメイン、推定読了時間
- 「この章で学ぶこと」セクション（箇条書きで概要）
- 各セクション: `## N-M. セクション名` + `### このセクションで学ぶこと`
- セクション末尾に `> **試験のポイント**` ブロック
- 章末に「章末確認問題」（details/summaryタグで解答を隠す形式）
- 図の参照は `../images/ファイル名` の相対パス
- 図のプレースホルダは `> **図解:** ファイル名 — 説明` 形式（ch00スタイル）ではなく、直接 `![alt](path)` で挿入（ch02以降のスタイル）

**Why:** ch00の既存フォーマットに合わせつつ、図の挿入方法はMarkdown標準に統一した
**How to apply:** 新しい章を作成する際はこの構造に従う
