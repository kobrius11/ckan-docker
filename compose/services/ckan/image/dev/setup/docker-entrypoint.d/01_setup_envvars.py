import os
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from lib.script_config import ScriptConfig

sc = ScriptConfig()

if __name__ == "__main__":
    
    print(f"[ENTRYPOINT {__file__}] Setting up Enviroment variables ..")
    sc.set_ckanvar("ckan.plugins")
    sc.set_ckanvar("ckan.webassets.path")
    sc.set_ckanvar("ckan.webassets.url")
    sc.set_ckanvar("ckan.cors.origin_allow_all")
