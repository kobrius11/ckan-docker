import os
import subprocess
from pathlib import Path
from lib.script_path_resolver import ScriptsPathResolver


class ScriptsRunner():

    def __init__(self, path_resolver: ScriptsPathResolver, is_test: bool = False):
        self.path_resolver = path_resolver
        self.is_test = is_test

    # Run any startup scripts provided by images extending this one
    def find_startup_scripts(self, scripts_dir) -> None:
        scripts_dir = self.path_resolver.get_dir(scripts_dir)

        assert isinstance(scripts_dir, Path), f"scripts_dir Arg must be of Path instance, Arg passed: {scripts_dir}"
        assert scripts_dir.exists(), f"scripts_dir Arg not Found, Arg passed: {scripts_dir}"

        for entry_path in sorted(scripts_dir.iterdir(), key=lambda e: e.name):
            
            if entry_path.is_file() and entry_path.suffix == '.sh':
                print(f"Running startup script: {entry_path}")
                if self.is_test:
                    entry_path.chmod(777)
                self.run_sh_script(entry_path)
            
            elif entry_path.is_file() and entry_path.suffix == '.py':
                print(f"Running startup script: {entry_path}")
                if self.is_test:
                    entry_path.chmod(777)
                self.run_py_script(entry_path)
            
            else:
                print(f"Skipping: {entry_path}")
            
            if entry_path.is_dir():
                print(f"Entering Dir: {entry_path}")
                self.find_startup_scripts(scripts_dir=entry_path)

    @staticmethod
    def run_sh_script(script_path: Path = Path("")) -> None:
        assert isinstance(script_path, Path), f"script_path Arg must be of Path instance. Please fix {script_path}"
        assert script_path.suffix == '.sh', f"File Must be of .sh extension. Please fix {script_path}"
        # assert os.access(script_path, os.R_OK | os.X_OK), f"Permission denied, cannot access {script_path}"
        
        subprocess.call(['/bin/sh', str(script_path.absolute())])

    @staticmethod
    def run_py_script(script_path: Path = Path("")) -> None:
        assert isinstance(script_path, Path), f"script_path Arg must be of Path instance. Please fix {script_path}"
        assert script_path.suffix == '.py', f"File Must be of .py extension. Please fix {script_path}"
        assert os.access(script_path, os.R_OK), f"Permission denied, cannot access {script_path}"
        
        subprocess.run(['python3', str(script_path.absolute())])