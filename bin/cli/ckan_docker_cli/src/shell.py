import os
import sys
import shlex
from pathlib import Path
import subprocess


def docker_compose(yaml: Path, *args):
    subprocess.run(["docker", "compose", "-f", yaml, *args], check=True)

def docker_system(*args):
    subprocess.run(["docker", "system", *args], check=True)

def docker_prune(*args):
    docker_system("prune", *args)

def docker_exec(yaml: Path, container_name: str, *args):
    docker_compose(yaml, "exec", container_name, *args)

def restart(yaml: Path, container_name: str):
    docker_compose(yaml, "restart", container_name)

def full_rebuild(yaml: Path):
    docker_prune("-a", "--volumes", "-f")
    docker_compose(yaml, "build", "--no-cache")
    docker_compose(yaml, "up", "--force-recreate")

def bash(yaml: Path, container_name: str, *args):
    command = shlex.join(args)
    docker_exec(yaml, container_name, "bash", "-c", command)

def ckan(yaml: Path, container_name: str, *args):
    docker_exec(yaml, container_name, "ckan", *args)
