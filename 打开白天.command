#!/bin/zsh
set -e
PROJECT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$PROJECT_DIR"
BLENDER_APP="/Applications/Blender.app/Contents/MacOS/Blender"
exec "$BLENDER_APP" "$PROJECT_DIR/Harbin_Sophia_Square.blend" --python "$PROJECT_DIR/scripts/select_lighting.py" -- --mode day
