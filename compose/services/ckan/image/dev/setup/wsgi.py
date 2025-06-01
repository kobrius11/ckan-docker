import sys
from pathlib import Path
from ckan.config.middleware import make_app
from ckan.cli import CKANConfigLoader
from logging.config import fileConfig as loggingFileConfig

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from lib.script_config import ScriptConfig


sc = ScriptConfig()
loggingFileConfig(sc.ckan_ini)
config = CKANConfigLoader(sc.ckan_ini).get_config()
application = make_app(config)