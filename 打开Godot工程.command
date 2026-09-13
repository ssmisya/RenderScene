#!/bin/zsh
set -e
PROJECT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$PROJECT_DIR"
if [[ ! -x "$PROJECT_DIR/.tools/godot/Godot.app/Contents/MacOS/Godot" ]]; then
  python3 "$PROJECT_DIR/scripts/setup_godot.py"
fi
"$PROJECT_DIR/.tools/godot/Godot.app/Contents/MacOS/Godot" --editor --path "$PROJECT_DIR/demo"
