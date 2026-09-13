# Blender project working directory

The user explicitly moved this project to:

`/Users/songmingyang/Library/Mobile Documents/com~apple~CloudDocs/Desktop/projects/Local tasks/blender`

All future modeling, scripts, renders, exports, logs and other project work must use that directory. Set command workdir to that absolute path, even if the task environment still reports the old workspace.

The main scene is `Harbin_Sophia_Square.blend` at that directory root. Its sibling `scripts`, `assets`, `references`, `renders` and `game` directories are the active supporting files.

Preserve the pre-existing files (including Harbin_Sophia_Blender_Assets_v1.zip and the older GLBs); they are separate prior assets. The original workspace's sophia_scene path is only a compatibility symlink, not a separate working copy.

## Mandatory real-scene QA for future map work

Before changing or expanding this scene, read `docs/实景复原与地图扩展SOP.md`.
The user's requirement is at least 10 recent, distinct, relevant photographs with
per-detail comparison and rework for every identified discrepancy. Keep provenance,
capture dates, coverage gaps and unresolved differences in machine-readable records.
Never claim 100% real-world accuracy from procedural geometry or a passing runtime test.
Run `python3 scripts/validate_references.py --strict` before claiming realism acceptance.
A playable development demo may be delivered with an explicit failed/pending realism gate.
