---
inclusion: always
---

# AWS Cloud Practitioner 学習システム — 常時コンテキスト

## プロジェクト概要

AWS Cloud Practitioner (CLF-C02) 試験対策の対話型学習システム。
学習ドキュメント・問題バンク・対話型 AI 授業で構成される。

## ディレクトリ構成と役割

```
docs/chapters/          章ごとの学習ドキュメント（ch00〜ch16, appA〜appC）
docs/questions/         問題バンク JSON（章ごと + domains.json）
records/                学習記録・進捗（gitignore 対象）
reports/                スコアレポート（gitignore 対象）
.claude/templates/      各種ファイルフォーマットテンプレート
```

> `records/` と `reports/` はユーザー個人データ。コミットしない（gitignore 設定済み）。

## ドメインと章のマッピング

| ドメイン | 配点 | 対象章 |
|---------|------|--------|
| domain1: クラウドのコンセプト | 24% | ch00, ch07, ch14 |
| domain2: セキュリティ | 30% | ch09 |
| domain3: テクノロジーとサービス | 34% | ch01〜ch06, ch08, ch10〜ch13, ch16 |
| domain4: 請求・料金・サポート | 12% | ch15 |

## 章グループと MPL タイミング

| グループ | 章 | テスト |
|---------|----|--------|
| Group A | ch00〜ch04 | ch04 完了後 → MPL-1（10問） |
| Group B | ch05〜ch08 | ch08 完了後 → MPL-2（10問） |
| Group C | ch09〜ch12 | ch12 完了後 → MPL-3（10問） |
| Group D | ch13〜ch16 | ch16 完了後 → FPL（30問） |

## 章ファイルマップ

| 章ID | ファイルパス |
|------|------------|
| appA | `docs/chapters/appA-networking-basics.md` |
| ch00 | `docs/chapters/ch00-introduction.md` |
| ch01 | `docs/chapters/ch01-web-hosting.md` |
| ch02 | `docs/chapters/ch02-serverless.md` |
| ch03 | `docs/chapters/ch03-storage.md` |
| ch04 | `docs/chapters/ch04-database.md` |
| ch05 | `docs/chapters/ch05-networking.md` |
| ch06 | `docs/chapters/ch06-async.md` |
| ch07 | `docs/chapters/ch07-resilience.md` |
| ch08 | `docs/chapters/ch08-containers.md` |
| ch09 | `docs/chapters/ch09-security.md` |
| ch10 | `docs/chapters/ch10-monitoring.md` |
| ch11 | `docs/chapters/ch11-cicd.md` |
| ch12 | `docs/chapters/ch12-analytics.md` |
| ch13 | `docs/chapters/ch13-ai-ml.md` |
| ch14 | `docs/chapters/ch14-migration.md` |
| ch15 | `docs/chapters/ch15-cost.md` |
| ch16 | `docs/chapters/ch16-misc.md` |
| appB | `docs/chapters/appB-support-plans.md` |
| appC | `docs/chapters/appC-exam-tips.md` |

## 一般的な AWS 質問への回答方針

AWS に関する質問を受けた場合:
1. `docs/chapters/` 配下の該当ファイルを読み込む
2. 関連セクションを引用しながら解説する
3. 対象読者は **IT 初心者・クラウド未経験者** — 専門用語は平易な言葉で補足する
4. CLF-C02 の対応ドメインを可能な限り示す
