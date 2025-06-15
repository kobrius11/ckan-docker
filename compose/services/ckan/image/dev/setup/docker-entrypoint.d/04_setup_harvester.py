import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from lib.script_config import ScriptConfig

sc = ScriptConfig()

if __name__ == "__main__":
    
    print("[ENTRYPOINT 04_setup_harverster] Setting up Ckan Harvester plugin variables ..")
    sc.set_ckanvar("ckan.harvest.timeout")
    sc.set_ckanvar("ckan.harvest.mq.type")
    sc.set_ckanvar("ckan.harvest.mq.hostname")
    sc.set_ckanvar("ckan.harvest.mq.port")
    sc.set_ckanvar("ckan.harvest.mq.redis_db")
    # sc.set_ckanvar("ckan.harvest.mq.password")

