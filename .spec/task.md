# 並列執筆タスク一覧

- 作成日: 2026-03-16
- 総タスク数: 20（本編17 + 付録3）
- ドキュメント構成: draft.md に基づく

---

## 並列実行グループ

### グループ1（依存なし・即時開始可能）

- T00, T-appA, T-appB, T-appC

### グループ2（T00完了後に開始可能）

- T01〜T16（T00の基礎概念を参照するため）

### 注意事項

- `related_chapters` に記載のタスクは「参照」関係であり、厳密な依存ではない
- writer エージェントは関連タスクが完了していなくても執筆を開始できる
- 重複サービスは各タスクの `special_notes` の指示に従う
- draw.io ファイルは `docs/images/` 配下に配置し、命名規則は `[chapter-id]-[description].drawio.png` とする

---

## タスク一覧

---

### タスク: T00 ― 第0章 導入

- **task_id:** T00
- **output_path:** `docs/chapters/ch00-introduction.md`
- **scope:** 第0章 導入 ― クラウドの基本概念とAWSの全体像（セクション 0-1〜0-5）
- **related_chapters:** [T01, T09, T-appA]
- **special_notes:**
  - 本書全体の前提となる章。クラウドの定義、AWSの全体像、責任共有モデルなどを扱う
  - CloudFormation は導入レベルの紹介のみ。詳細は T11 で扱う
  - AZ/リージョンの概念は T01, T07 でも繰り返し参照される基礎知識
  - 責任共有モデルは T09 で深掘りするため、本章では全体像にとどめる
- **図解推奨:**
  - クラウドサービスモデルの階層図（IaaS/PaaS/SaaS vs オンプレミス）
  - AWSグローバルインフラストラクチャの構成図
  - 責任共有モデルの境界図
- **draw.io ファイル:**
  - `ch00-cloud-service-models.drawio.png`
  - `ch00-global-infrastructure.drawio.png`
  - `ch00-shared-responsibility.drawio.png`
- **estimated_sections:** 5

---

### タスク: T01 ― 第1章 Webアプリケーションのホスティング

- **task_id:** T01
- **output_path:** `docs/chapters/ch01-web-hosting.md`
- **scope:** 第1章 Webアプリケーションのホスティング（セクション 1-1〜1-7）
- **related_chapters:** [T00, T02, T03, T05, T07, T15]
- **special_notes:**
  - Elastic Beanstalk は本章で扱い、T11 では触れない
  - EC2 購入オプションは本章で詳細に扱い、T15 ではコスト最適化の文脈で参照する
  - EBS の基本はストレージとして T03 でも扱うが、EC2 との関連は本章で説明
- **図解推奨:**
  - オンプレミス vs クラウドのWebサーバー比較図
  - EC2購入オプションの比較チャート
  - ELB + Auto Scaling + CloudFront の全体アーキテクチャ図
- **draw.io ファイル:**
  - `ch01-onprem-vs-cloud.drawio.png`
  - `ch01-ec2-pricing.drawio.png`
  - `ch01-web-architecture.drawio.png`
- **estimated_sections:** 7

---

### タスク: T02 ― 第2章 サーバーレスアーキテクチャ

- **task_id:** T02
- **output_path:** `docs/chapters/ch02-serverless.md`
- **scope:** 第2章 サーバーレスアーキテクチャ（セクション 2-1〜2-5）
- **related_chapters:** [T01, T04, T06, T08]
- **special_notes:**
  - Fargate は本章で概要のみ紹介。責任範囲・起動タイプの詳細は T08 で扱う
  - Step Functions は本章で概要のみ紹介。ステートマシン・ワークフロー設計パターンの詳細は T06 で扱う
  - Lambda + DynamoDB の組み合わせは本章で触れ、DynamoDB の詳細は T04 に委ねる
- **図解推奨:**
  - EC2 vs Lambda の責任範囲比較図
  - サーバーレスWebアプリケーションのアーキテクチャ図
  - Step Functions ワークフロー図（概要のみ）
- **draw.io ファイル:**
  - `ch02-ec2-vs-lambda.drawio.png`
  - `ch02-serverless-webapp.drawio.png`
  - `ch02-step-functions-overview.drawio.png`
- **estimated_sections:** 5

---

### タスク: T03 ― 第3章 ストレージ戦略

- **task_id:** T03
- **output_path:** `docs/chapters/ch03-storage.md`
- **scope:** 第3章 ストレージ戦略（セクション 3-1〜3-7）
- **related_chapters:** [T01, T04, T07, T14, T15]
- **special_notes:**
  - EBS は T01（EC2との関連）でも登場するが、本章でブロックストレージとしての体系的な説明を行う
  - S3 はストレージの主役として本章で詳説。T07（耐久性）、T12（データレイク）、T14（移行先）でも参照される
  - Storage Gateway は T14（移行）でも登場するが、本章でハイブリッドストレージとして説明
- **図解推奨:**
  - ストレージ3種類（ブロック/ファイル/オブジェクト）の比較図
  - S3ストレージクラスのコスト・アクセス頻度マトリクス
  - EBS / EFS / S3 の使い分けフローチャート
- **draw.io ファイル:**
  - `ch03-storage-types.drawio.png`
  - `ch03-s3-storage-classes.drawio.png`
  - `ch03-storage-selection.drawio.png`
- **estimated_sections:** 7

---

### タスク: T04 ― 第4章 データベース設計

- **task_id:** T04
- **output_path:** `docs/chapters/ch04-database.md`
- **scope:** 第4章 データベース設計（セクション 4-1〜4-6）
- **related_chapters:** [T01, T02, T03, T07, T14]
- **special_notes:**
  - DMS/SCT は移行ツールだが、データベース文脈として本章で詳説。T14 でも移行戦略の一環として参照される
  - DynamoDB は T02（Lambda連携）でも触れるが、本章で NoSQL としての体系的な説明を行う
  - RDS マルチAZ は T07（高可用性）でも参照される重要概念
- **図解推奨:**
  - データベースの種類と対応サービスのマッピング図
  - RDSマルチAZ vs リードレプリカの構成図
  - DMS移行パターンのフロー図
- **draw.io ファイル:**
  - `ch04-db-types.drawio.png`
  - `ch04-rds-multiaz-vs-readreplica.drawio.png`
  - `ch04-dms-migration.drawio.png`
- **estimated_sections:** 6

---

### タスク: T05 ― 第5章 ネットワーク設計

- **task_id:** T05
- **output_path:** `docs/chapters/ch05-networking.md`
- **scope:** 第5章 ネットワーク設計（セクション 5-1〜5-6）
- **related_chapters:** [T-appA, T01, T07, T09, T14]
- **special_notes:**
  - 付録A（T-appA）のネットワーク基礎知識を前提とするため、冒頭で付録Aへの参照リンクを設ける
  - セキュリティグループ / NACL は T09（セキュリティ）でもセキュリティ観点から参照される
  - Direct Connect / VPN は T14（移行）、T16（ハイブリッド→Outposts）でも関連
- **図解推奨:**
  - VPCの全体構成図
  - セキュリティグループ vs NACL の適用レイヤー図
  - ハイブリッド接続の比較図（Direct Connect vs VPN）
- **draw.io ファイル:**
  - `ch05-vpc-overview.drawio.png`
  - `ch05-sg-vs-nacl.drawio.png`
  - `ch05-hybrid-connectivity.drawio.png`
- **estimated_sections:** 6

---

### タスク: T06 ― 第6章 非同期処理とアプリケーション統合

- **task_id:** T06
- **output_path:** `docs/chapters/ch06-async.md`
- **scope:** 第6章 非同期処理とアプリケーション統合（セクション 6-1〜6-5）
- **related_chapters:** [T02, T07, T08]
- **special_notes:**
  - Step Functions は T02 で概要を紹介済み。本章でステートマシン、ワークフロー設計パターンの詳細を扱う
  - SQS / SNS / EventBridge の使い分けは試験頻出。明確な判断基準を提示する
  - 疎結合パターンは T07（耐障害性）の前提知識となる
- **図解推奨:**
  - 密結合 vs 疎結合の比較図
  - SQS / SNS / EventBridge の使い分けフロー図
  - ファンアウトパターンのアーキテクチャ図
- **draw.io ファイル:**
  - `ch06-coupling-comparison.drawio.png`
  - `ch06-messaging-selection.drawio.png`
  - `ch06-fanout-pattern.drawio.png`
- **estimated_sections:** 5

---

### タスク: T07 ― 第7章 耐障害性と高可用性

- **task_id:** T07
- **output_path:** `docs/chapters/ch07-resilience.md`
- **scope:** 第7章 耐障害性と高可用性（セクション 7-1〜7-7）
- **related_chapters:** [T00, T01, T03, T04, T05, T06]
- **special_notes:**
  - 本章は多くの先行章のサービスを横断的にまとめる統合章
  - EC2/ELB/Auto Scaling（T01）、S3耐久性（T03）、RDSマルチAZ（T04）、Route53（T05）、疎結合（T06）を前提とする
  - DR戦略の4パターン（Backup & Restore / Pilot Light / Warm Standby / Multi-Site Active-Active）は試験頻出
  - RPO / RTO の概念は初学者にとって混同しやすいため、丁寧な図解が必要
- **図解推奨:**
  - マルチAZ構成のアーキテクチャ図
  - DR戦略の4パターン比較図
  - RPO / RTO の概念図
- **draw.io ファイル:**
  - `ch07-multiaz-architecture.drawio.png`
  - `ch07-dr-strategies.drawio.png`
  - `ch07-rpo-rto.drawio.png`
- **estimated_sections:** 7

---

### タスク: T08 ― 第8章 コンテナ技術

- **task_id:** T08
- **output_path:** `docs/chapters/ch08-containers.md`
- **scope:** 第8章 コンテナ技術（セクション 8-1〜8-5）
- **related_chapters:** [T01, T02, T11]
- **special_notes:**
  - Fargate は T02 で概要を紹介済み。本章で責任範囲・起動タイプ（EC2起動タイプ vs Fargate起動タイプ）の詳細を扱う
  - ECS vs EKS の使い分けは試験で問われるポイント
  - ECR（コンテナレジストリ）も本章で扱う
  - コンテナデプロイフローは T11（CI/CD）と関連
- **図解推奨:**
  - VM vs コンテナの構造比較図
  - ECS/EKS + Fargate のサービス関係図
  - コンテナデプロイのフロー図
- **draw.io ファイル:**
  - `ch08-vm-vs-container.drawio.png`
  - `ch08-ecs-eks-fargate.drawio.png`
  - `ch08-container-deploy.drawio.png`
- **estimated_sections:** 5

---

### タスク: T09 ― 第9章 セキュリティとアクセス管理

- **task_id:** T09
- **output_path:** `docs/chapters/ch09-security.md`
- **scope:** 第9章 セキュリティとアクセス管理（セクション 9-1〜9-8）
- **related_chapters:** [T00, T05, T10]
- **special_notes:**
  - 責任共有モデルは T00 で全体像を紹介済み。本章でサービスごとの責任分界点を深掘りする
  - セキュリティグループ / NACL は T05 でネットワーク文脈から説明済み。本章ではセキュリティ観点で補足する（重複扱いOK）
  - CloudTrail / Config は T10 で運用文脈から詳説するが、本章でもセキュリティ監査の観点で触れる（重複扱いOK）
  - Shield Standard は「全アカウントに自動無料適用」が試験頻出ポイント
  - IAM のポリシー評価ロジック（明示的Deny > 明示的Allow > デフォルトDeny）は試験頻出
- **図解推奨:**
  - IAM の概念関係図（ユーザー/グループ/ロール/ポリシー）
  - 多層防御のレイヤー図
  - セキュリティサービスの全体マップ
- **draw.io ファイル:**
  - `ch09-iam-relationships.drawio.png`
  - `ch09-defense-in-depth.drawio.png`
  - `ch09-security-services-map.drawio.png`
- **estimated_sections:** 8

---

### タスク: T10 ― 第10章 監視・運用と管理

- **task_id:** T10
- **output_path:** `docs/chapters/ch10-monitoring.md`
- **scope:** 第10章 監視・運用と管理（セクション 10-1〜10-8）
- **related_chapters:** [T09, T15, T-appB]
- **special_notes:**
  - CloudTrail / Config は T09（セキュリティ）でも触れるが、本章で運用・監視の観点から体系的に説明する
  - Trusted Advisor は T-appB（サポートプラン）と密接に関連。フルアクセスにはビジネスサポート以上が必要
  - Compute Optimizer は T15（コスト最適化）でも参照される
  - Organizations の SCP（サービスコントロールポリシー）は T09 のセキュリティ文脈とも関連
- **図解推奨:**
  - CloudWatch / CloudTrail / Config の役割比較図
  - Organizations の階層構造図
  - Trusted Advisor の5カテゴリ図
- **draw.io ファイル:**
  - `ch10-cloudwatch-cloudtrail-config.drawio.png`
  - `ch10-organizations-hierarchy.drawio.png`
  - `ch10-trusted-advisor.drawio.png`
- **estimated_sections:** 8

---

### タスク: T11 ― 第11章 CI/CDとデベロッパーツール

- **task_id:** T11
- **output_path:** `docs/chapters/ch11-cicd.md`
- **scope:** 第11章 CI/CDとデベロッパーツール（セクション 11-1〜11-5）
- **related_chapters:** [T00, T08, T10]
- **special_notes:**
  - CloudFormation は T00 で導入レベルの紹介済み。本章でテンプレート構造、スタック、変更セット、CDKとの関係を詳説する
  - Elastic Beanstalk は T01 で扱うため、本章では触れない
  - CodeCommit / CodeBuild / CodeDeploy / CodePipeline のパイプライン構成が試験頻出
- **図解推奨:**
  - CI/CDパイプラインのフロー図
  - CloudFormation の動作概念図
- **draw.io ファイル:**
  - `ch11-cicd-pipeline.drawio.png`
  - `ch11-cloudformation-flow.drawio.png`
- **estimated_sections:** 5

---

### タスク: T12 ― 第12章 データ分析基盤

- **task_id:** T12
- **output_path:** `docs/chapters/ch12-analytics.md`
- **scope:** 第12章 データ分析基盤（セクション 12-1〜12-5）
- **related_chapters:** [T03, T02, T13]
- **special_notes:**
  - S3 をデータレイクとして活用するパターンは T03 と関連。本章ではデータ分析パイプラインの文脈で説明
  - Kinesis は T02（Lambda連携）でも触れる可能性があるが、本章でストリーミング処理として詳説
  - Athena / Redshift / QuickSight / Glue の使い分けが試験ポイント
- **図解推奨:**
  - データ分析パイプラインの全体図
  - データレイク vs データウェアハウスの比較図
- **draw.io ファイル:**
  - `ch12-analytics-pipeline.drawio.png`
  - `ch12-datalake-vs-dw.drawio.png`
- **estimated_sections:** 5

---

### タスク: T13 ― 第13章 AI/MLサービス

- **task_id:** T13
- **output_path:** `docs/chapters/ch13-ai-ml.md`
- **scope:** 第13章 AI/MLサービス（セクション 13-1〜13-7）
- **related_chapters:** [T02, T12, T03]
- **special_notes:**
  - AIサービス層（Rekognition, Comprehend, Polly, Transcribe, Translate, Lex等）と MLプラットフォーム層（SageMaker）の2層構造で整理
  - Amazon Q / Bedrock / CodeWhisperer など生成AI関連サービスも含める（CLF-C02で出題範囲に追加）
  - Lambda + AIサービスの組み合わせは T02 と関連
  - S3 を学習データ保管先として使うパターンは T03 と関連
- **図解推奨:**
  - AI/MLサービスの2層構造図
  - AIサービスのユースケースマッピング
- **draw.io ファイル:**
  - `ch13-ai-ml-layers.drawio.png`
  - `ch13-ai-services-map.drawio.png`
- **estimated_sections:** 7

---

### タスク: T14 ― 第14章 クラウド移行戦略

- **task_id:** T14
- **output_path:** `docs/chapters/ch14-migration.md`
- **scope:** 第14章 クラウド移行戦略（セクション 14-1〜14-5）
- **related_chapters:** [T00, T04, T03, T15]
- **special_notes:**
  - 7つのR（Relocate, Rehost, Replatform, Repurchase, Refactor, Retire, Retain）は試験頻出
  - DMS/SCT は T04 で詳説済み。本章では移行戦略のツールとして参照する
  - Storage Gateway / Snow Family は T03 とも関連するが、本章では大量データ移行の文脈で説明
  - Migration Hub / Application Discovery Service なども移行ツールとして扱う
- **図解推奨:**
  - 7つのRの比較チャート
  - Snow Family のデータ量対応図
  - 移行プロセスのフロー図
- **draw.io ファイル:**
  - `ch14-seven-rs.drawio.png`
  - `ch14-snow-family.drawio.png`
  - `ch14-migration-flow.drawio.png`
- **estimated_sections:** 5

---

### タスク: T15 ― 第15章 コスト管理と最適化

- **task_id:** T15
- **output_path:** `docs/chapters/ch15-cost.md`
- **scope:** 第15章 コスト管理と最適化（セクション 15-1〜15-5）
- **related_chapters:** [T01, T03, T10, T-appB]
- **special_notes:**
  - EC2 購入オプション（オンデマンド/リザーブド/Savings Plans/スポット）は T01 で詳説済み。本章ではコスト最適化の観点から横断的に整理
  - S3 ストレージクラスのコスト比較は T03 と関連
  - Trusted Advisor / Compute Optimizer は T10 と重複。本章ではコスト最適化推奨ツールとして参照
  - サポートプランの料金は T-appB で扱う
  - AWS 料金の3要素（コンピューティング/ストレージ/データ転送OUT）は試験頻出
- **図解推奨:**
  - AWS料金の3要素の図
  - コスト管理ツールの使い分けフロー図
  - 購入オプションのコスト比較グラフ
- **draw.io ファイル:**
  - `ch15-pricing-factors.drawio.png`
  - `ch15-cost-tools.drawio.png`
  - `ch15-purchase-options.drawio.png`
- **estimated_sections:** 5

---

### タスク: T16 ― 第16章 その他の頻出サービス

- **task_id:** T16
- **output_path:** `docs/chapters/ch16-misc.md`
- **scope:** 第16章 その他の頻出サービス（セクション 16-1〜16-4）
- **related_chapters:** [T01, T05, T14]
- **special_notes:**
  - 他章に収まらないが試験に出るサービスを集約（WorkSpaces, AppStream 2.0, Outposts, Local Zones, Wavelength 等）
  - WorkSpaces vs EC2 の違いは T01 と対比して説明
  - Outposts はハイブリッド接続（T05 の Direct Connect/VPN）および移行戦略（T14）と関連
  - 各サービスの説明は簡潔にし、試験での問われ方にフォーカスする
- **図解推奨:**
  - サービスカテゴリマップ
- **draw.io ファイル:**
  - `ch16-services-map.drawio.png`
- **estimated_sections:** 4

---

### タスク: T-appA ― 付録A 通信とインターネットの基礎

- **task_id:** T-appA
- **output_path:** `docs/chapters/appA-networking-basics.md`
- **scope:** 付録A 通信とインターネットの基礎（セクション A-1〜A-7）
- **related_chapters:** [T05, T09]
- **special_notes:**
  - 試験には直接出題されない前提知識だが、第5章（VPC）や第9章（ファイアウォール）の理解に必須
  - 各セクション末尾に「AWSとの接点」ボックスを設け、本編との橋渡しを行う
  - 章末確認問題は設けない。代わりに各セクション末に理解度チェック2〜3問を配置
  - IT初学者向けのため、日常語での比喩を多用する（例: IPアドレス=住所、ポート=部屋番号）
  - グループ1として即時開始可能（他章に依存しない独立コンテンツ）
- **図解推奨:**
  - ネットワーク通信の全体像
  - TCP/IP 4層モデルの図
  - DNS名前解決のフロー図
- **draw.io ファイル:**
  - `appA-network-overview.drawio.png`
  - `appA-tcp-ip-layers.drawio.png`
  - `appA-dns-resolution.drawio.png`
- **estimated_sections:** 7

---

### タスク: T-appB ― 付録B AWSサポートプランの比較

- **task_id:** T-appB
- **output_path:** `docs/chapters/appB-support-plans.md`
- **scope:** 付録B AWSサポートプランの比較（セクション B-1〜B-4）
- **related_chapters:** [T10, T15]
- **special_notes:**
  - Basic / Developer / Business / Enterprise On-Ramp / Enterprise の5プランを比較表で整理
  - TAM（テクニカルアカウントマネージャー）は Enterprise On-Ramp 以上で提供される点が試験頻出
  - Trusted Advisor のフルアクセスはビジネスサポート以上が必要（T10 と連携）
  - レスポンスタイム、料金体系、利用可能なサポートチャネルを明確に比較
  - グループ1として即時開始可能（他章に依存しない独立コンテンツ）
- **図解推奨:**
  - サポートプラン比較表
- **draw.io ファイル:**
  - `appB-support-plans.drawio.png`
- **estimated_sections:** 4

---

### タスク: T-appC ― 付録C 試験対策のポイント

- **task_id:** T-appC
- **output_path:** `docs/chapters/appC-exam-tips.md`
- **scope:** 付録C 試験対策のポイント（セクション C-1〜C-5）
- **related_chapters:** [全タスク]
- **special_notes:**
  - 全ドメイン横断の総まとめ章。各章の試験頻出ポイントを集約する
  - 章末確認問題は設けない。総合模擬問題20問を別セクションとして提供推奨
  - 学習スケジュールのモデル例（2週間/1ヶ月/2ヶ月）を提示
  - ドメイン別の配点と学習優先度を明示
  - グループ1として即時開始可能だが、他タスク完了後に最終調整を推奨
- **図解推奨:**
  - ドメイン別学習優先度チャート
  - 学習スケジュールのモデル例（2週間/1ヶ月/2ヶ月）
- **draw.io ファイル:**
  - `appC-domain-priorities.drawio.png`
  - `appC-study-schedule.drawio.png`
- **estimated_sections:** 5
