"""Compatibility entry for the current v2 renderer. Accepts --mode day/night/both."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name("render_v2.py")),run_name="__main__")
