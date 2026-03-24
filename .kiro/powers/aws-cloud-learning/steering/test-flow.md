---
inclusion: auto
name: test-flow
description: テスト（Quick Test・MPL・FPL）を実施するときに使用する
---

# テストの進め方

## Quick Test（最大5問・固定）

「テストしたい」「確認したい」などユーザーオーダー時のみ実施。

```
1. 範囲を確認（全単元 / 特定の章 / 特定のドメイン）
2. 対象の docs/questions/<chXX>.json を読み込む
3. questions 配列からランダムに最大5問選ぶ
4. 1問ずつ出題 → 回答 → 即時フィードバック
5. 全問終了後: 正答率 + 簡単なコメントを口頭で伝える
6. records/sessions/YYYYMMDD_HHmmss_quick_test.md に保存
7. records/.session_state.json に type: "quick_test" で書き込む
```

**1問の出題フォーマット:**
```
問題 X / Y

<問題文>

A. ...
B. ...
C. ...
D. ...
```

**回答後フォーマット:**
```
<正解 or 不正解>
正解: <選択肢>

解説: <explanation の内容>
```

複数選択問題（type: "multi"）は「2つ選んでください」と明示する。

---

## MPL の進め方

### 問題の読み込みと選択

**MPL-1（ch00〜ch04）:**
`docs/questions/` から以下のファイルを読み込み、各章から合計10問を選択する:
- `ch00-introduction.json`: 2問
- `ch01-web-hosting.json`: 2問
- `ch02-serverless.json`: 2問
- `ch03-storage.json`: 2問
- `ch04-database.json`: 2問

**MPL-2（ch05〜ch08）:**
- `ch05-networking.json`: 3問
- `ch06-async.json`: 2問
- `ch07-availability.json`: 3問（ファイル名注意: `ch07-availability.json`）
- `ch08-containers.json`: 2問

**MPL-3（ch09〜ch12）:**
- `ch09-security.json`: 4問（問題数が多いため多めに配分）
- `ch10-monitoring.json`: 2問
- `ch11-cicd.json`: 2問
- `ch12-analytics.json`: 2問

### MPL の実施手順

```
1. 上記の問題ファイルを読み込み、問題をシャッフルして番号を振る
2. 1問ずつ出題 → 回答 → 即時フィードバック（正誤 + 解説）
3. 全問終了後:
   a. 正答率・苦手トピックを口頭でフィードバック
   b. 「次のGroupに向けてのアドバイス」を伝える
4. records/sessions/YYYYMMDD_HHmmss_mpl<N>.md に記録を保存
5. records/.session_state.json に type: "mpl<N>" で書き込む
6. reports/YYYYMMDD_HHmmss_mpl<N>.md にスコアレポートを生成
7. reports/index.md を更新
```

**MPL セッション記録のフォーマット:** `.claude/templates/mpl-session-record.md` を読み込んで参照すること。

---

## FPL の進め方

### 問題の読み込みと選択（30問・本番配分）

`docs/questions/domains.json` を参照してドメインごとの章を特定し、以下の配分で選択する:

| ドメイン | 問題数 | 対象章 |
|---------|--------|--------|
| domain1（クラウドのコンセプト・24%） | 7問 | ch00, ch07, ch14 |
| domain2（セキュリティ・30%） | 9問 | ch09 |
| domain3（テクノロジーとサービス・34%） | 10問 | ch01〜ch06, ch08, ch10〜ch13, ch16 |
| domain4（請求・料金・サポート・12%） | 4問 | ch15 |

各ドメインの対象章から問題数を均等配分して選択する。

### FPL の実施手順

```
1. 各ドメインの問題ファイルを読み込み、配分通りに問題を選択・シャッフル
2. 1問ずつ出題 → 回答 → 即時フィードバック（正誤 + 解説）
3. 全問終了後:
   a. 正答率・ドメイン別得点率を口頭でフィードバック
   b. 苦手分野の詳細まとめ
   c. 「お疲れ様でした！」のメッセージ
4. records/sessions/YYYYMMDD_HHmmss_fpl.md に記録を保存
5. records/.session_state.json に type: "fpl" で書き込む
6. reports/YYYYMMDD_HHmmss_fpl_attempt<N>.md にスコアレポートを生成
7. reports/index.md を更新
8. 推奨学習プランを生成して records/learning_plan.json に保存
```

### session_state.json の書き込みフォーマット（テスト中）

テスト開始時と全問完了時に書き込む。
フォーマットは `.claude/templates/session-state-test.json` を読み込んで参照すること。
