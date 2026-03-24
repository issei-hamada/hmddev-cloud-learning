---
inclusion: auto
name: reporting
description: スコアレポートを生成するとき、学習プランを作成するとき、フェーズ2の復習を進めるときに使用する
---

# スコアレポート・学習プラン・フェーズ2

## スコアレポートの生成

MPL・FPL 完了後、`reports/` 配下にレポートを生成する。

### スコアバッジ

| 正答率 | バッジ |
|--------|--------|
| 90%以上 | `[EXCELLENT]` |
| 70%以上 | `[PASS]` |
| 50%以上 | `[REVIEW]` |
| 50%未満 | `[RETRY]` |

スコアバー（10マス）: 正答率を `█` と `░` で表現する。例: 70% → `[███████░░░]`

### MPL レポートのテンプレート

`.claude/templates/mpl-report.md` を読み込んで参照すること。

### FPL レポートの追加セクション

MPL テンプレートに加えて、`.claude/templates/fpl-report-extras.md` を読み込んで参照すること。

### reports/index.md の更新

MPL・FPL のレポート生成後、`reports/index.md` を更新する。

---

## 推奨学習プランの生成（FPL 完了後）

FPL 完了後に `records/progress.json` と各 MPL 記録・授業セッション記録を元に優先度を算出し、`records/learning_plan.json` を生成する。

### 優先度スコアの算出

各章について以下を計算する:

```
priority_score = (1 - test_accuracy) × 0.6 + lesson_score_weight × 0.4

test_accuracy: FPL でその章の問題の正答率（ドメインスコアで代替）
lesson_score_weight: A=0.0, B=0.5, C=1.0
```

スコアが同点の場合、ドメイン配点（domain2=30% が最高）が高い章を優先する。

### learning_plan.json のフォーマット

`.claude/templates/learning-plan.json` を読み込んで参照すること。

生成後「学習プランを `records/learning_plan.json` に保存しました。次回 `/start-lesson` で復習を開始できます。」と伝える。

---

## フェーズ2: 推奨プランに従った復習

`records/learning_plan.json` が存在するとき、以下のフローで動作する。

```
1. learning_plan.json を読み込む
2. status が "pending" の最初の章を提案する
   「次は ◯◯ の復習をしましょう。理由: △△。特に △△ セクションを重点的に。」
3. /start-lesson でその章を授業（focus_sections のセクションは確認質問2問）
4. 章の授業終了後、Quick Test（5問・その章の問題）で定着確認
5. learning_plan.json の対象章の status を "completed" に更新
6. completed_reviews に章IDを追記
7. 次の pending 章へ
```

全章が completed になったら:
「学習プランを全て消化しました！もう一度 Final Progress Lesson（30問）に挑戦してスコアを確認しますか？」

---

## ファイル操作のルール（テスト・レポート・プラン）

| 操作 | タイミング |
|------|----------|
| 問題バンクを読む | テスト開始時 |
| `.session_state.json` を書く | テスト開始時・全問完了時 |
| `progress.json` を更新 | テスト完了時 |
| セッション記録を保存 | テスト完了時 |
| スコアレポートを生成 | MPL・FPL 完了時 |
| `reports/index.md` を更新 | スコアレポート生成後 |
| `learning_plan.json` を生成 | FPL 完了後 |
| `learning_plan.json` を更新 | 復習章完了時 |

---

## エラーハンドリング

- **章ファイルが見つからない**: ユーザーに伝え、別の章を提案する
- **問題バンクが空**: 「この章の問題はまだ登録されていません」と伝え、別の範囲を提案する
- **progress.json が壊れている**: バックアップとして `.bak` を作成してから再初期化し、ユーザーに伝える
- **MPL/FPL をスキップした**: `progress.json` に `mpl1_skipped: true` 等を記録。後から「MPLをやりたい」と言われれば対応する
