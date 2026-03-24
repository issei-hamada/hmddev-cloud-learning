# AGENTS.md

このファイルは hmddev-cloud-learning プロジェクトで動作するすべてのエージェントが把握すべき情報を定義します。

---

## プロジェクト概要

AWS Cloud Practitioner (CLF-C02) 試験対策のための学習システムです。
学習ドキュメント・問題バンク・対話型学習エージェント（teacher）で構成されます。

---

## ディレクトリ構成と役割

```
docs/chapters/          章ごとの学習ドキュメント（ch00〜ch16, appA〜appC）
docs/questions/         問題バンク JSON（chapters ごと + domains.json）
tools/generate_exam.py  CLI 模擬試験生成ツール
exams/                  生成された試験ファイル（gitignore）
records/                学習記録・進捗（gitignore）
reports/                スコアレポート（gitignore）
.claude/agents/         エージェント定義
.claude/skills/         スキル定義
.claude/hooks/          Stop/SessionEnd フック
.claude/templates/      各種ファイルフォーマットテンプレート
```

> `records/` と `reports/` は gitignore 対象。ユーザー個人の学習データのため、コミットしない。

---

## teacher エージェント（メイン）

`claude --agent teacher` で直接起動する主エージェント。他のエージェントから subagent として呼び出すことは想定していない。

### フェーズ構成

| フェーズ | 条件 | 動作 |
|---------|------|------|
| **フェーズ1** | `records/learning_plan.json` が存在しない | ch00〜ch16 を順に授業。MPL・FPL を実施 |
| **フェーズ2** | `records/learning_plan.json` が存在する | プランに従って苦手章を復習 |

### 章グループと MPL タイミング

| グループ | 章 | MPL |
|---------|----|-----|
| A | ch00〜ch04 | ch04 完了後 → MPL-1（10問） |
| B | ch05〜ch08 | ch08 完了後 → MPL-2（10問） |
| C | ch09〜ch12 | ch12 完了後 → MPL-3（10問） |
| D | ch13〜ch16 | ch16 完了後 → FPL（30問） |

### 進捗の永続化（hooks）

- **Stop hook（async）**: セッションの各ターン終了後に `save_progress.sh` を実行
- **SessionEnd hook（sync）**: セッション終了時に同スクリプトを実行
- フックは `records/.session_state.json` を読み込み `records/progress.json` へマージする

### .session_state.json の役割

teacher エージェントが各操作後に書き込む一時ファイル。フックがこれを参照して `progress.json` へマージする。
- 授業中: `type: "lesson"` — `.claude/templates/session-state-lesson.json` を参照
- テスト中: `type: "mpl1|mpl2|mpl3|fpl|quick_test"` — `.claude/templates/session-state-test.json` を参照

### テンプレートファイルの参照

teacher エージェントはファイル生成時に必ず `.claude/templates/` のテンプレートを Read ツールで読み込んでからフォーマットを適用すること。

| テンプレート | 用途 |
|------------|------|
| `progress-initial.json` | `records/progress.json` の初期化フォーマット |
| `session-state-lesson.json` | 授業中の `.session_state.json` フォーマット |
| `session-state-test.json` | テスト中の `.session_state.json` フォーマット |
| `lesson-session-record.md` | 授業セッション記録（`records/sessions/`）フォーマット |
| `mpl-session-record.md` | MPL セッション記録フォーマット |
| `mpl-report.md` | MPL スコアレポートフォーマット |
| `fpl-report-extras.md` | FPL レポートの追加セクション（ドメイン別・合格ライン・前回比較） |
| `learning-plan.json` | `records/learning_plan.json` フォーマット |

---

## /start-lesson スキル

`--agent teacher` 起動中に `/start-lesson` を入力すると発動する。
進捗状況（`records/progress.json`）を読み込み、次に学習すべき章を判断して授業を開始する。

---

## 一般的な AWS 質問への回答方針

teacher エージェント以外（通常の Claude Code セッション）で AWS に関する質問を受けた場合:

1. `docs/chapters/` 配下の該当ファイルを Read ツールで読み込む
2. 関連セクションを引用しながら解説する
3. 対象読者は **IT 初心者・クラウド未経験者** — 専門用語は平易な言葉で補足する
4. CLF-C02 の対応ドメインを可能な限り示す

### ドキュメントマップ

| トピック例 | 参照ファイル |
|-----------|-------------|
| クラウドの概念、IaaS/PaaS/SaaS、責任共有モデル、Well-Architected Framework | `docs/chapters/ch00-introduction.md` |
| EC2、ELB、Auto Scaling、CloudFront、Elastic Beanstalk、Lightsail | `docs/chapters/ch01-web-hosting.md` |
| Lambda、API Gateway、Fargate、Step Functions（サーバーレス） | `docs/chapters/ch02-serverless.md` |
| S3、EBS、EFS、FSx、Storage Gateway、Backup（ストレージ） | `docs/chapters/ch03-storage.md` |
| RDS、Aurora、DynamoDB、ElastiCache、DocumentDB、Neptune、DMS（データベース） | `docs/chapters/ch04-database.md` |
| VPC、サブネット、セキュリティグループ、NACL、Route 53、Direct Connect、VPN | `docs/chapters/ch05-networking.md` |
| SQS、SNS、EventBridge、Step Functions（非同期・疎結合） | `docs/chapters/ch06-async.md` |
| マルチAZ、ディザスタリカバリ、RPO/RTO、フェイルオーバー | `docs/chapters/ch07-resilience.md` |
| ECS、EKS、Fargate、ECR（コンテナ） | `docs/chapters/ch08-containers.md` |
| IAM、Cognito、KMS、WAF、Shield、GuardDuty、Inspector、Macie、Security Hub | `docs/chapters/ch09-security.md` |
| CloudWatch、CloudTrail、Config、Systems Manager、Organizations、Trusted Advisor | `docs/chapters/ch10-monitoring.md` |
| CodeBuild、CodePipeline、CloudFormation、X-Ray、Amplify（CI/CD） | `docs/chapters/ch11-cicd.md` |
| Kinesis、Glue、Athena、Redshift、EMR、QuickSight（データ分析） | `docs/chapters/ch12-analytics.md` |
| SageMaker、Rekognition、Comprehend、Lex、Polly、Transcribe、Translate、Amazon Q | `docs/chapters/ch13-ai-ml.md` |
| 移行戦略（7つのR）、CAF、Migration Hub、Snow Family、DMS | `docs/chapters/ch14-migration.md` |
| Cost Explorer、Budgets、Trusted Advisor、Savings Plans（コスト管理） | `docs/chapters/ch15-cost.md` |
| WorkSpaces、IoT Core、Connect、SES、Batch、Outposts | `docs/chapters/ch16-misc.md` |
| TCP/IP、DNS、HTTP/HTTPS、ファイアウォール（ネットワーク基礎） | `docs/chapters/appA-networking-basics.md` |
| サポートプラン（Basic / Developer / Business / Enterprise） | `docs/chapters/appB-support-plans.md` |
| 試験対策のポイント、出題ドメイン、学習リソース | `docs/chapters/appC-exam-tips.md` |

---

## 注意事項

- `records/` と `reports/` はユーザー個人データ。コミットしない（gitignore 設定済み）。
- ドキュメントに記載のない情報は、その旨を明示した上で補足してよい。
- 試験問題を解く場合は、まず自力で考えさせてから解説するよう促す。
