#!/bin/zsh
set -e
PROJECT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$PROJECT_DIR"
APP="$PROJECT_DIR/builds/索菲亚广场 · 持枪漫游.app"
if [[ ! -d "$APP" ]]; then
  mkdir -p "$PROJECT_DIR/builds"
  ditto -x -k "$PROJECT_DIR/SophiaWalk_macOS_v2.2_demo.zip" "$PROJECT_DIR/builds"
fi
mkdir -p "$PROJECT_DIR/logs"
exec "$APP/Contents/MacOS/索菲亚广场 · 持枪漫游" > "$PROJECT_DIR/logs/game_demo.log" 2>&1
