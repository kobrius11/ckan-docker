import os
from  typing import Union

class EnvParser():
    def __init__(self, use_envvars: bool = True):
        self.use_envvars = use_envvars

    @staticmethod
    def replace_dunderscores(envvar: str) -> str:
        return envvar.replace("__", ".")

    @staticmethod
    def replace_dots(ckanvar: str) -> str:
        return ckanvar.replace(".", "__")

    @staticmethod
    def is_native(envvar: str) -> bool:
        return envvar.startswith("CKAN___")

    @classmethod
    def construct_ckanvar(cls, envvar: str) -> str:
        """
        From enviroment variable constructs a CKAN instance variable

        Args:
            :envvar: enviroment variable to convert
         
        example:
            - CKAN__SITE_ID => ckan.site_id
            - CKANEXT__S3FILESTORE__AWS_BUCKET_NAME => ckanext.s3filestore.aws_bucket_name
        """
        assert not cls.is_native(envvar), f"This variable should not be set with envvars in the first place, please check {envvar}"
 
        return cls.replace_dunderscores(envvar).lower()

    @classmethod
    def construct_envvar(cls, ckanvar: str) -> str:
        """
        From CKAN instance variable constructs a enviroment variable

        Args:
            :ckanvar: CKAN instance variable to convert
         
        example:
            - ckan.site_id => CKAN__SITE_ID
            - ckanext.s3filestore.aws_bucket_name => CKANEXT__S3FILESTORE__AWS_BUCKET_NAME
        """
        assert not cls.is_native(ckanvar), f"This variable should not be set with envvars in the first place, please check {ckanvar}"
 
        return cls.replace_dots(ckanvar).upper()


    @staticmethod
    def is_envvar(envvar: str) -> bool:
        """
        Check if Environment variable exists
        """
        return envvar in os.environ

    def convert_env_to_ckanvar(self, envvar: str) -> str:
        """
        BEAKER_SESSION_SECRET => beaker.session.secret
        """
        if self.use_envvars:
            return self.construct_ckanvar(envvar)
        return envvar.replace('_', '.').lower()

    def convert_ckan_to_envvar(self, ckanvar: str) -> str:
        """
        beaker.session.secret => BEAKER_SESSION_SECRET
        """
        if self.use_envvars:
            return self.construct_envvar(ckanvar)
        return ckanvar.replace('.', '_').upper()

    # TODO: Consider adding checks for placeholder strings eg: CHANGE_ME, NONE, NOTSET ...
    def get_envvar(self, envvar: str, default: Union[str, None] = None):
        return os.environ.get(envvar, default)
