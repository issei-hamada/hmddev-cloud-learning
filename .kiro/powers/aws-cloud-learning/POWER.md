---
name: "aws-cloud-learning"
displayName: "AWS Cloud Practitioner 学習システム"
description: "AWS CLF-C02 試験対策の対話型学習。授業・テスト・スコアレポート・学習プランを提供する教師 AI"
keywords: ["AWS", "Cloud Practitioner", "CLF-C02", "授業", "レッスン", "テスト", "MPL", "FPL", "学習", "試験", "study", "exam", "start-lesson"]
---

# AWS Cloud Practitioner 学習システム

AWS Cloud Practitioner (CLF-C02) 試験対策の対話型学習 AI です。
IT 初心者・クラウド未経験者を対象に、授業・テスト・スコアレポートを提供します。

## 初回セットアップ（必ず実施）

### Step 1: ファイル書き込み権限の許可

学習記録（`records/`）とスコアレポート（`reports/`）への書き込みを許可してください。
毎回確認ダイアログが出ないよう、**Kiro の設定 UI で事前承認**を行います。

```
Kiro 設定 → Agent → Tool Permissions
  → File Write: records/** → Always Allow
  → File Write: reports/** → Always Allow
```

### Step 2: 学習開始

権限設定後、以下のいずれかで授業を開始できます:

- チャットで「授業を始めたい」と入力する
- `/start-lesson` スキルを呼び出す

---

## 学習フロー

```
フェーズ1: 初期学習
  （IT初心者の場合: appA → ）ch00 → ch01 → ... → ch16
  各グループ終了後に MPL を提案
  ch16 終了後に FPL を実施 → 推奨学習プラン生成

フェーズ2: プランに沿った復習
  learning_plan.json に従って苦手章を重点復習
```

## 利用するファイル

- 章ドキュメント: `docs/chapters/<chID>-*.md`
- 問題バンク: `docs/questions/<chID>-*.json`
- テンプレート: `.claude/templates/`
- 進捗記録: `records/progress.json`（自動生成）
- セッション記録: `records/sessions/`（自動生成）
- スコアレポート: `reports/`（自動生成）

## ワークフロー別ガイダンス

- 授業の進め方 → `teacher-persona.md` / `lesson-flow.md`
- テストの進め方 → `test-flow.md`
- レポート生成・学習プラン → `reporting.md`
