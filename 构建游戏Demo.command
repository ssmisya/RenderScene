#!/bin/zsh
set -e
PROJECT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$PROJECT_DIR"
python3 scripts/setup_godot.py
python3 scripts/build_demo.py
open "$PROJECT_DIR/builds"
