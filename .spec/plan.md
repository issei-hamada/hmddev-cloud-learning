# plan

## 目的

AWS も IT も初学者向けの、本当の基礎から勉強出来る学習コンテンツを作成する。
最終的に、AWS クラウドプラクティショナーを、**基礎を理解した上での**合格を目指す。

## 機能

- kiro ベースで実装する
- 自分のペースで md 形式のコンテンツを読める
- kiro と会話しながら、レクチャーしてもらえる
- ユーザは AWS コンソールを見ながら、kiro は AWS CLI で環境を確認しながら、ハンズオンを行う

## エージェント

### ユーザ利用

- teacher
- assistant
- lerning-reviewer

### メンテナー利用

- planner
- writer
- doc-reviewer

## skills

- lesson: ユーザから伝えられたセクションの内容を、ステップバイステップで解説する
- article: 新しい記事を作成する

## hooks

- 学習終了時、結果を保存する

## オンボーディング

- AWS 認証情報設定
- Kiro インストール

## 学習コンテンツ案

> **対象読者**: IT初心者・クラウド未経験者  
> **コンセプト**: アーキテクチャや要件ごとにAWSサービスを分類し、「なぜ必要か → 何が課題か → AWSでどう解決するか」の流れで理解する  
> **対応試験**: AWS Certified Cloud Practitioner (CLF-C02)

---

## 試験概要

| 項目 | 内容 |
|------|------|
| 試験時間 | 90分 |
| 問題数 | 65問（うち採点対象50問、採点対象外15問） |
| 合格スコア | 700 / 1000 |
| 受験料 | 100 USD |
| 問題形式 | 択一選択式、複数選択式 |

### 出題ドメインと配分

| ドメイン | 配分 |
|----------|------|
| 第1分野: クラウドのコンセプト | 24% |
| 第2分野: セキュリティとコンプライアンス | 30% |
| 第3分野: クラウドテクノロジーとサービス | 34% |
| 第4分野: 請求、料金、サポート | 12% |

---

## 本編

---

### 第0章　導入 ― クラウドの基本概念と AWS の全体像

- クラウドとは何か（IaaS / PaaS / SaaS）
- AWS グローバルインフラストラクチャ（リージョン、AZ、エッジロケーション）
- Well-Architected Framework の6つの柱の概要
- 責任共有モデル

**対応サービス**: AWS マネジメントコンソール、AWS CLI、CloudFormation（IaC の導入として）

---

### 第1章　Web アプリケーションのホスティング

**アーキテクチャ**: ユーザーからのHTTPリクエストを受けて処理を返す、最も基本的なWebシステム

**課題**: サーバーの調達・OS管理が大変、アクセス増への対応、グローバル配信

**対応サービス**:

- Amazon EC2（インスタンスタイプ、購入オプション：オンデマンド / リザーブド / スポット / Savings Plans）
- Elastic Load Balancing（負荷分散）
- Auto Scaling（伸縮性）
- Amazon Lightsail（小規模向け簡易ホスティング）
- AWS Elastic Beanstalk（アプリデプロイの自動化）
- Amazon CloudFront（CDN / エッジ配信）

---

### 第2章　サーバーレスアーキテクチャ ― サーバー管理からの解放

**アーキテクチャ**: サーバーを意識せずにコードを実行する、イベント駆動型の処理

**課題**: サーバー管理の運用負荷、アイドル時間のコスト、スケーリングの複雑さ

**対応サービス**:

- AWS Lambda
- Amazon API Gateway
- AWS Fargate
- AWS Step Functions（ワークフローのオーケストレーション）

---

### 第3章　データの永続化 ― ストレージ戦略

**アーキテクチャ**: 用途に応じてオブジェクト / ブロック / ファイルストレージを使い分ける

**課題**: データの種類によって最適な保存方法が異なる、コストとアクセス頻度のトレードオフ、バックアップとライフサイクル管理

**対応サービス**:

- Amazon S3（オブジェクトストレージ、ストレージクラス：Standard / IA / Glacier）
- Amazon EBS（ブロックストレージ）
- Amazon EFS（共有ファイルシステム）
- Amazon FSx
- AWS Storage Gateway（ハイブリッド環境のキャッシュ）
- AWS Backup
- AWS Elastic Disaster Recovery

---

### 第4章　データベース設計 ― RDB から NoSQL まで

**アーキテクチャ**: アプリケーションの要件に応じたデータベース選択（リレーショナル / キーバリュー / ドキュメント / グラフ / インメモリ）

**課題**: セルフマネージド vs マネージド、スケーラビリティ、可用性、データモデルの選定

**対応サービス**:

- Amazon RDS（マネージドRDB）
- Amazon Aurora（高性能RDB）
- Amazon DynamoDB（キーバリュー / NoSQL）
- Amazon ElastiCache（インメモリキャッシュ）
- Amazon DocumentDB（ドキュメントDB）
- Amazon Neptune（グラフDB）
- AWS DMS / AWS SCT（データベース移行）

---

### 第5章　ネットワーク設計 ― 安全なクラウドネットワークの構築

**アーキテクチャ**: パブリック / プライベートサブネットの分離、オンプレミスとの接続、DNS管理

**課題**: セキュリティ境界の設計、オンプレミスとのハイブリッド接続、レイテンシーの最適化

**対応サービス**:

- Amazon VPC（サブネット、インターネットゲートウェイ、NATゲートウェイ）
- セキュリティグループ / ネットワークACL
- Amazon Route 53（DNS）
- AWS Direct Connect（専用線接続）
- AWS VPN（Site-to-Site / Client）
- AWS Transit Gateway
- AWS Global Accelerator
- AWS PrivateLink

---

### 第6章　非同期処理とアプリケーション統合 ― 疎結合アーキテクチャ

**アーキテクチャ**: キューイング、Pub/Sub、イベント駆動で各コンポーネントを疎結合にする

**課題**: 同期処理のボトルネック、障害の連鎖、システム間の依存性

**対応サービス**:

- Amazon SQS（メッセージキュー）
- Amazon SNS（プッシュ通知 / Pub/Sub）
- Amazon EventBridge（イベントバス / イベント駆動）
- AWS Step Functions（ステートマシンによるオーケストレーション）

---

### 第7章　耐障害性と高可用性 ― 止まらないシステムの設計

**アーキテクチャ**: マルチAZ構成、ディザスタリカバリ、自動復旧

**課題**: 単一障害点（SPOF）の排除、障害時の自動フェイルオーバー、RPO / RTO の設計

**対応サービス**:

- マルチAZ配置（EC2、RDS、ELB）
- Auto Scaling
- Amazon S3（イレブンナインの耐久性）
- AWS Elastic Disaster Recovery
- Route 53（DNSフェイルオーバー）
- AWS Backup

---

### 第8章　コンテナ技術 ― マイクロサービスの実行基盤

**アーキテクチャ**: コンテナによるアプリケーションのパッケージングとオーケストレーション

**課題**: 環境差異の解消、デプロイの効率化、コンテナの管理・スケーリング

**対応サービス**:

- Amazon ECS
- Amazon EKS
- AWS Fargate（サーバーレスコンテナ）
- Amazon ECR（コンテナイメージレジストリ）

---

### 第9章　セキュリティとアクセス管理 ― ゼロトラストの考え方

**アーキテクチャ**: 認証・認可、暗号化、脅威検知、コンプライアンスの多層防御

**課題**: 最小権限の実装、不正アクセスの検知、暗号鍵の管理、コンプライアンス対応

**対応サービス**:

- AWS IAM（ユーザー、グループ、ロール、ポリシー）
- AWS IAM Identity Center（SSO）
- Amazon Cognito（アプリユーザー認証）
- AWS KMS（暗号鍵管理）
- AWS CloudHSM
- AWS Secrets Manager
- AWS Certificate Manager
- AWS WAF / AWS Shield（Web攻撃防御 / DDoS防御）
- AWS Firewall Manager
- Amazon GuardDuty（脅威検知）
- Amazon Inspector（脆弱性スキャン）
- Amazon Macie（機密データ検出）
- Amazon Detective
- AWS Security Hub
- AWS Artifact（コンプライアンスレポート）
- AWS Audit Manager
- AWS Directory Service
- AWS RAM（リソース共有）

---

### 第10章　監視・運用と管理 ― 可観測性とガバナンス

**アーキテクチャ**: ログ収集、メトリクス監視、設定管理、組織統制

**課題**: 障害の早期発見、構成ドリフトの検知、マルチアカウント管理

**対応サービス**:

- Amazon CloudWatch（メトリクス、ログ、アラーム）
- AWS CloudTrail（API操作の監査ログ）
- AWS Config（リソース構成の追跡）
- AWS Systems Manager
- AWS Organizations
- AWS Control Tower
- AWS Trusted Advisor
- AWS Health Dashboard
- AWS Service Catalog
- AWS License Manager
- AWS Compute Optimizer
- Service Quotas
- AWS Well-Architected Tool

---

### 第11章　CI/CD とデベロッパーツール ― 開発と運用の自動化

**アーキテクチャ**: コードの変更を自動でビルド・テスト・デプロイするパイプライン

**課題**: 手動デプロイのリスク、リリース頻度の向上、障害時の原因特定

**対応サービス**:

- AWS CodeBuild
- AWS CodePipeline
- AWS X-Ray（分散トレーシング）
- AWS CloudFormation（IaC）
- AWS Amplify / AWS AppSync（フロントエンド / モバイル開発）

---

### 第12章　データ分析基盤 ― ビッグデータの収集・加工・可視化

**アーキテクチャ**: ETLパイプライン、データウェアハウス、リアルタイムストリーミング

**課題**: 大量データの効率的な処理、スキーマ管理、データのリアルタイム処理

**対応サービス**:

- Amazon Kinesis（ストリーミングデータ処理）
- AWS Glue（ETL / データカタログ）
- Amazon Athena（S3上のSQLクエリ）
- Amazon Redshift（データウェアハウス）
- Amazon EMR（Hadoop / Spark）
- Amazon OpenSearch Service
- Amazon QuickSight（BIダッシュボード）

---

### 第13章　AI/ML サービス ― 機械学習をサービスとして使う

**アーキテクチャ**: 事前学習済みAIサービスの活用と、カスタムMLモデルの構築

**課題**: ML人材の不足、学習データの準備、推論環境の運用

**対応サービス**:

- Amazon SageMaker AI（MLモデル構築・学習・デプロイ）
- Amazon Rekognition（画像・動画分析）
- Amazon Comprehend（自然言語処理）
- Amazon Lex（チャットボット）
- Amazon Polly（音声合成）
- Amazon Transcribe（音声→テキスト）
- Amazon Translate（翻訳）
- Amazon Textract（文書解析 / OCR）
- Amazon Kendra（エンタープライズ検索）
- Amazon Q

---

### 第14章　クラウド移行戦略 ― オンプレミスからの移行

**アーキテクチャ**: 7つのR（Rehost, Replatform, Refactor 等）に基づく移行パターン

**課題**: 既存資産の棚卸し、移行計画の策定、大容量データの物理転送

**対応サービス**:

- AWS Cloud Adoption Framework（CAF）
- AWS Migration Hub
- AWS Application Discovery Service
- AWS Application Migration Service
- Migration Evaluator
- AWS Snow Family（Snowcone / Snowball / Snowmobile）
- AWS DMS / AWS SCT（第4章と関連）

---

### 第15章　コスト管理と最適化 ― クラウドの経済性を最大化する

**アーキテクチャ**: コスト可視化、予算管理、購入オプションの最適化

**課題**: 従量課金の予測困難さ、未使用リソースの放置、組織横断のコスト管理

**対応サービス**:

- AWS Cost Explorer
- AWS Budgets
- AWS Cost and Usage Reports
- AWS Marketplace
- AWS Organizations（一括請求）
- AWS Trusted Advisor（コスト最適化チェック）
- AWS Compute Optimizer
- コスト配分タグ

---

### 第16章　その他の頻出サービス ― エンドユーザーコンピューティング / IoT / ビジネスアプリケーション

**アーキテクチャ**: 仮想デスクトップ、IoTデバイス管理、コンタクトセンター

**対応サービス**:

- Amazon WorkSpaces / WorkSpaces Secure Browser
- Amazon AppStream 2.0
- AWS IoT Core
- Amazon Connect
- Amazon SES
- AWS Batch
- AWS Outposts

---

## 付録

---

### 付録A　通信とインターネットの基礎 ― AWS を理解するための前提知識

> 超初心者向け。AWSサービスの理解に必要な最低限のネットワーク知識を、各セクション1〜2ページ程度で解説する。各セクション末尾の「AWSとの接点」で本編の該当章への橋渡しを行う。

---

#### A-1　ネットワーク通信の基本

**「コンピュータ同士が会話する」とはどういうことか**

- 通信とは「データを決まったルールに従って送受信すること」
- プロトコル（通信の約束事）という考え方
- クライアントとサーバーの役割分担

> **AWS との接点**: EC2 は「サーバー」の役割、ブラウザが「クライアント」。この関係がクラウドの出発点。

---

#### A-2　インターネットの仕組み

**世界中のコンピュータがつながる仕組み**

- LAN と WAN ― 小さなネットワークが相互接続して「インターネット」になる
- ルーターの役割 ― ネットワーク同士をつなぐ「交差点の信号機」
- ISP（インターネットサービスプロバイダ）の存在

> **AWS との接点**: AWS リージョンや AZ も、巨大なネットワークの集合体。VPC は「AWS 内に自分専用の LAN を作る」イメージ。

---

#### A-3　IP アドレスとサブネット

**ネットワーク上の「住所」の仕組み**

- IP アドレスとは ― 各機器に割り当てられる一意の識別番号
- パブリック IP とプライベート IP の違い
- CIDR 表記の基本的な読み方（/16、/24 が何を意味するか程度）
- サブネット ― ネットワークを区画分けする考え方

> **AWS との接点**: VPC の CIDR ブロック設定、パブリックサブネット / プライベートサブネットの設計に直結。

---

#### A-4　TCP/IP の基本概念

**データが届くまでの「層」の考え方**

- TCP/IP 4層モデルの概要（ネットワークインターフェース層 → インターネット層 → トランスポート層 → アプリケーション層）
  - 各層の役割を「荷物の配送」に例えて簡潔に
- TCP と UDP の違い ― 信頼性重視 vs 速度重視
- ポート番号 ― 「建物の住所（IP）」の中の「部屋番号」
  - 80（HTTP）、443（HTTPS）、22（SSH）だけ覚えればOK

> **AWS との接点**: セキュリティグループのルール設定（ポート番号の許可 / 拒否）を理解するために必要な知識。

---

#### A-5　DNS ― ドメイン名から IP アドレスを引く仕組み

**なぜ「example.com」と入力するだけでサイトが見られるのか**

- DNS の役割 ― 人間が読める名前を IP アドレスに変換する「電話帳」
- 名前解決の流れ（ブラウザ → リゾルバ → ルートサーバー → 権威サーバー、を簡略化して）
- ドメイン、ホスト名、レコードタイプ（A レコード、CNAME 程度）

> **AWS との接点**: Route 53 はまさにこの DNS を提供するサービス。CloudFront や ELB にドメインを紐づける際に必須。

---

#### A-6　HTTP/HTTPS ― Web の通信プロトコル

**ブラウザと Web サーバーの「会話の作法」**

- HTTP リクエストとレスポンスの基本的な流れ
- URL の構造（スキーム、ホスト、パス）
- HTTPS と SSL/TLS ― 暗号化通信の必要性
- ステートレスという性質

> **AWS との接点**: ELB のリスナー設定（HTTP / HTTPS）、ACM での証明書管理、API Gateway の理解に直結。

---

#### A-7　ファイアウォールとネットワークセキュリティの基礎

**「誰を通すか」を制御する仕組み**

- ファイアウォールの役割 ― 通信の許可 / 拒否を IP とポートで制御
- インバウンド（受信）とアウトバウンド（送信）
- ステートフルとステートレスの違い

> **AWS との接点**: セキュリティグループ（ステートフル）とネットワーク ACL（ステートレス）の違いが、ここを理解していれば一発でわかる。

---

### 付録B　AWS サポートプランの比較

（※ Basic / Developer / Business / Enterprise On-Ramp / Enterprise の各プランの特徴と違いを整理）

---

### 付録C　試験対策のポイント

（※ 学習リソース、模擬試験の活用法、時間配分のコツなどを整理）