#!/usr/bin/env bash
# .claude/hooks/save_progress.sh
# Stop / SessionEnd フックから呼ばれ、セッション状態を progress.json へ反映する。

set -euo pipefail

CHECKPOINT="$CLAUDE_PROJECT_DIR/records/.session_state.json"
PROGRESS="$CLAUDE_PROJECT_DIR/records/progress.json"
MERGE_SCRIPT="$CLAUDE_PROJECT_DIR/.claude/hooks/merge_progress.py"

# チェックポイントが存在しない場合は何もしない
if [ ! -f "$CHECKPOINT" ]; then
  exit 0
fi

# progress.json が存在しない場合は初期スキーマを作成
if [ ! -f "$PROGRESS" ]; then
  mkdir -p "$(dirname "$PROGRESS")"
  cat > "$PROGRESS" << 'EOF'
{
  "last_updated": "",
  "it_beginner": null,
  "chapters": {},
  "quick_tests": [],
  "mpl1": null,
  "mpl2": null,
  "mpl3": null,
  "fpl_history": []
}
EOF
fi

# Python マージスクリプトを実行
if ! python3 "$MERGE_SCRIPT" "$CHECKPOINT" "$PROGRESS" 2>&1; then
  echo "[save_progress] merge_progress.py の実行に失敗しました。スキップします。" >&2
  exit 0
fi

exit 0
