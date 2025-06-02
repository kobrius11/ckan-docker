import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from lib.script_config import ScriptConfig

sc = ScriptConfig()

if __name__ == "__main__":
    
    print("[ENTRYPOINT 02_setup_ckan_auth] Setting up Ckan Auth plugins variables ..")
    sc.set_ckanvar("ckanext.auth.include_frontend_login_token")