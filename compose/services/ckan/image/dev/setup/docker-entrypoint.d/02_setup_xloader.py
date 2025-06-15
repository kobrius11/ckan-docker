import os
import sys
import subprocess
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from lib.script_config import ScriptConfig

sc = ScriptConfig()

def setup_xloader():
    is_xloader = "xloader" in sc.env.get_envvar("CKAN__PLUGINS")

    if is_xloader:
        sc.set_ckanvar("ckanext.xloader.ssl_verify")
        sc.set_ckanvar("ckanext.xloader.site_url")
        sc.set_ckanvar("ckanext.xloader.max_content_length")
        sc.set_ckanvar("ckanext.xloader.formats")
        sc.set_ckanvar("ckanext.xloader.job_timeout")
        sc.set_ckanvar("ckanext.xloader.strict_type_guessing")
        sc.set_ckanvar("ckanext.xloader.max_type_guessing_length")
        sc.set_ckanvar("ckanext.xloader.parse_dates_dayfirst")
        sc.set_ckanvar("ckanext.xloader.parse_dates_year_first")
        sc.set_ckanvar("ckanext.xloader.ignore_hash")
        sc.set_ckanvar("ckanext.xloader.max_excerpt_lines")
        sc.set_ckanvar("ckanext.xloader.clean_datastore_tables")
        sc.set_ckanvar("ckanext.xloader.show_badges")
        sc.set_ckanvar("ckanext.xloader.debug_badges")
        sc.set_ckanvar("ckanext.xloader.requires_succesful_report")
        sc.set_ckanvar("ckanext.xloader.enforce_schema")

        #TODO: Fix needed, api_token gets created twice
        API_TOKEN_ENV = sc.env.get_envvar(sc.env.construct_envvar("ckanext.xloader.api_token"))

        if not API_TOKEN_ENV:
            print("Set up ckan.xloader.api_token in the CKAN config file")

            token = sc.try_generate_api_token("sysadmin", "xloader")

            # Write token into config
            sc.set_ckanvar("ckanext.xloader.api_token", token)


if __name__ == "__main__":
    
    print("[ENTRYPOINT 02_setup_xloader] Setting up xloader ...") 
    setup_xloader()