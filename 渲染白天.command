#!/bin/zsh
set -e
PROJECT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$PROJECT_DIR"
BLENDER_APP="/Applications/Blender.app/Contents/MacOS/Blender"
"$BLENDER_APP" -b "$PROJECT_DIR/Harbin_Sophia_Square.blend" --python "$PROJECT_DIR/scripts/render_v2.py" -- --mode day --view hero --width 2400 --samples 192
open "$PROJECT_DIR/renders/v2_2_1"
