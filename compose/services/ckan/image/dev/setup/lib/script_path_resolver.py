import os
from pathlib import Path
from enum import Enum


class ScriptsPathResolver:
    def __init__(
            self,
            dir_enum: Enum,
            app_dir: str = ""
        ):
        # self.dir_enum = dir_enum
        self.app_dir = os.environ.get("APP_DIR", app_dir)

    def get_dir(self, dir_enum: Enum) -> Path:
        base_dir = Path(self.app_dir)
        return base_dir / dir_enum.value

    # def get_dir(self, dir_enum: Enum) -> Path:
    #     base_dir = Path(self.app_dir)
    #     match dir_enum:
    #         case ScriptsDirEnum.ENTRYPOINT_SCRIPTS:
    #             return base_dir / ScriptsDirEnum.ENTRYPOINT_SCRIPTS
    #         case ScriptsDirEnum.AFTERINIT_SCRIPTS:
    #             return base_dir / ScriptsDirEnum.AFTERINIT_SCRIPTS
    #         case _:
    #             raise ValueError(f"Unknown script dir: {dir_enum}")