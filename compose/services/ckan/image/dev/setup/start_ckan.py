from enum import Enum 
from lib.script_runner import ScriptsRunner
from lib.script_config import ScriptConfig
from lib.script_path_resolver import ScriptsPathResolver

class ScriptsDirEnum(Enum):
    ENTRYPOINT_SCRIPTS = "docker-entrypoint.d"
    AFTERINIT_SCRIPTS = "docker-afterinit.d"
    PRERUN_SCRIPTS = "prerun"

sc = ScriptConfig()
spr = ScriptsPathResolver(dir_enum=ScriptsDirEnum)
ss = ScriptsRunner(path_resolver=spr)


if __name__ == "__main__":
    
    print("Looking for Entrypoint scripts ... ")
    ss.find_startup_scripts(ScriptsDirEnum.ENTRYPOINT_SCRIPTS)

    # secrets to set
    ckan_env_secrets = ["beaker.session.secret", "WTF_CSRF_SECRET_KEY", "SECRET_KEY"]
    sc.set_session_secrets(ckan_env_secrets)
    sc.set_jwt_secrets()

    # Run the prerun script to init CKAN and create the default admin user
    print("Running prerun.py script ...")
    ss.find_startup_scripts(ScriptsDirEnum.PRERUN_SCRIPTS)


    print("Looking for Afterinit scripts ... ")
    ss.find_startup_scripts(ScriptsDirEnum.AFTERINIT_SCRIPTS)

    