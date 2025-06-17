import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from lib.script_config import ScriptConfig

sc = ScriptConfig()

if __name__ == "__main__":
    is_scheming = "scheming_datasets scheming_groups scheming_organizations" in sc.env.get_envvar("CKAN__PLUGINS")
    
    if is_scheming:
        print(f"[ENTRYPOINT {__file__}] Setting up Ckan scheming plugin variables ..")
        sc.set_ckanvar("scheming.dataset_schemas", "ckanext.scheming:ckan_dataset.yaml")
        sc.set_ckanvar("scheming.group_schemas", "ckanext.scheming:group_with_bookface.json")
        sc.set_ckanvar("scheming.organization_schemas", "ckanext.scheming:org_with_dept_id.json")
        sc.set_ckanvar("scheming.presets", "ckanext.scheming:presets.json")
        sc.set_ckanvar("scheming.dataset_fallback", "false")
