import os
import runpy
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, "app")

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

runpy.run_path(os.path.join(APP_DIR, "main.py"), run_name="__main__")
