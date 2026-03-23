# AGENTS.md

このファイルは、hmddev-cloud-learning プロジェクトにおけるエージェントの動作を定義します。

---

## AWS 試験サポート

### 基本方針

AWS に関する質問を受けたとき、エージェントは以下の手順で回答してください。

1. **ドキュメントを検索する**
   `docs/chapters/` 配下のファイルから、質問に関連するセクションを特定する。

2. **該当箇所を引用する**
   関連するドキュメントのファイル名とセクション名を明示し、内容を引用しながら解説する。

3. **初心者向けに補足する**
   対象読者は IT 初心者・クラウド未経験者。専門用語は噛み砕いて説明し、「なぜ必要か → 何が課題か → AWS でどう解決するか」の流れで解説する。

4. **試験との対応を示す**
   可能であれば、CLF-C02 のどのドメインに関連するかを補足する（例:「第2分野: セキュリティとコンプライアンス」）。

---

### ドキュメントマップ

質問のトピックに応じて、以下のファイルを参照してください。

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

### 回答フォーマット例

```
## [質問に対する回答タイトル]

> 参照: `docs/chapters/ch09-security.md` ― 「AWS IAM」セクション

[引用または要約]

### ポイント解説

[初心者向けの補足説明]

### 試験との関連

- **対応ドメイン**: 第2分野 ― セキュリティとコンプライアンス（30%）
- **よく出る問い方**: [試験でよく問われる観点]
```

---

### 注意事項

- ドキュメントに記載のない情報は、その旨を明示した上で補足してよい。
- ハンズオンを求められた場合は、AWS CLI または AWS マネジメントコンソールの操作手順を案内する。
- 試験問題を解く場合は、まず自力で考えさせてから解説するよう促す。
