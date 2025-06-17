import os
import sys
import subprocess
from typing import Union, List
import secrets
from lib.env_parser import EnvParser

class ScriptConfig():
    _instance = None

    def __init__(
            self,
            ckan_ini: str = "",
            env_parser: EnvParser = EnvParser(),
        ):
        if self._isinitialized:
            return
        self.ckan_ini = os.environ.get("CKAN_INI", ckan_ini)
        self.env = env_parser
        self._isinitialized = True

    # singleton pattern
    @classmethod
    def __new__(cls, ckan_ini: str = ""):
        if not cls._instance:
            cls._instance = super(ScriptConfig, cls).__new__(cls)
            cls._instance._isinitialized = False
        elif cls._instance.ckan_ini != ckan_ini:
            raise ValueError(f"{cls._instance.ckan_ini}, newly passed {ckan_ini} has no effect")
        return cls._instance

    def set_ckanvar(self, ckanvar: str, default: Union[str, None] = None) -> None:
        """
        default arg must have __str__ defined 
        """
        print(f"[CONFIG] setting ckanvar {ckanvar}")
        envvar = self.env.convert_ckan_to_envvar(ckanvar)

        value = self.env.get_envvar(envvar, default)
        
        if not value:
            raise ValueError(f"Enviroment var is not set for {envvar}, so default value must be provided")
        
        return subprocess.run(['ckan', 'config-tool', self.ckan_ini, f"{ckanvar}={value}"], check=True)


    def set_session_secrets(self, ckan_env_vars: List[str]) -> None:
        for secret_var in ckan_env_vars:
            self.set_ckanvar(secret_var, secrets.token_urlsafe(64))

    def set_jwt_secrets(self) -> None:
        secret = f"string:{secrets.token_urlsafe(64)}"
        self.set_ckanvar("api_token.jwt.encode.secret", secret)
        self.set_ckanvar("api_token.jwt.decode.secret", secret)
    
    def set_ckan_envvars(self, envvars: List[str]) -> None:
        for var in envvars:
            self.set_ckanvar(var)


    def try_generate_api_token(self, username: str, token_name: str):
            try:
                result = subprocess.run(
                    ["ckan", "-c", self.ckan_ini, "user", "token", "add", username, token_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                    text=True
                )

                token = result.stdout.strip().splitlines()[-1].replace("\t", "")
                print(f"Generated {token_name} token succesfully!")
                return token

            except subprocess.CalledProcessError as e:
                print("Error occurred while generating or setting the API token:")
                print(e.stderr)
                sys.exit(1)

    def try_create_user():
        pass

    def make_user_admin():
        pass