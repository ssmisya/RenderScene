"""Validate and render the current scene without resetting or saving camera edits."""
import runpy,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
runpy.run_path(str(R/"scripts/validate_v2.py"),run_name="__main__")
sys.argv=["render_v2.py","--","--mode","both","--view","all","--width","2400","--samples","192"]
runpy.run_path(str(R/"scripts/render_v2.py"),run_name="__main__")
