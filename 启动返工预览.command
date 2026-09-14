#!/bin/zsh
set -e
cd -- "${0:A:h}"
app="builds/review/索菲亚广场 · 持枪漫游.app"
if [[ ! -d "$app" ]]; then
  print '尚无本地返工预览。请先运行：python3 scripts/build_demo.py --preview'
  exit 1
fi
print '正在打开本地返工预览。实景 SOP 尚未验收通过。'
open "$app"
