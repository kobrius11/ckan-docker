from pathlib import Path
import click
import ckan_docker_cli.src.shell as sh


ROOT = Path.cwd() # /ckan-docker/
COMPOSE_DEV = ROOT / 'compose' / 'docker-compose.dev.yml'
COMPOSE_PROD = ROOT / 'compose' / 'docker-compose.yml'

@click.group()
def cli():
    pass

@cli.command()
@click.option('--env', type=click.Choice(['dev', 'prod']), default='dev', help='Environment (dev or prod)')
@click.option('--full-rebuild', is_flag=True, help='Full rebuild')
@click.argument('args', nargs=-1)
def build(env, full_rebuild, args):
    """Build docker-compose environment."""
    yaml = COMPOSE_DEV if env == 'dev' else COMPOSE_PROD

    if full_rebuild:
        sh.full_rebuild(yaml)
    else:
        sh.docker_compose(yaml, "build", *args)

@cli.command()
@click.option('--env', type=click.Choice(['dev', 'prod']), default='dev', help='Environment (dev or prod)')
@click.option('--full-rebuild', is_flag=True, help='Full rebuild')
@click.argument('args', nargs=-1)
def up(env, full_rebuild, args):
    """Launches docker-compose environment."""
    yaml = COMPOSE_DEV if env == 'dev' else COMPOSE_PROD

    if full_rebuild:
        sh.full_rebuild(yaml)
    else:
        sh.docker_compose(yaml, "up", *args)

@cli.command()
@click.option('--env', type=click.Choice(['dev', 'prod']), default='dev', help='Environment (dev or prod)')
@click.option('--container-name', type=click.STRING, help='Pass the container name to restart')
def restart(env, container_name):
    """Restart the container"""
    yaml = COMPOSE_DEV if env == 'dev' else COMPOSE_PROD
    sh.restart(yaml, container_name)

@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.option('--env', type=click.Choice(['dev', 'prod']), default='dev', help='Environment (dev or prod)')
@click.option('--container-name', type=click.STRING, help='Pass the container name to restart')
@click.pass_context
def bash(ctx, env, container_name):
    """execute bash script inside container"""
    yaml = COMPOSE_DEV if env == 'dev' else COMPOSE_PROD
    args = ctx.args
    if not args:
        args = ["bash"] # enter shell if no args
    sh.bash(yaml, container_name, *args)

# @cli.command()
# @click.option('--env', type=click.Choice(['dev', 'prod']), default='dev', help='Environment (dev or prod)')
# @click.option('--container-name', type=click.STRING, help='Pass the container name to restart')
# @click.argument('args', nargs=-1)
# def ckan(env, container_name, args):
#     """execute ckan script inside container"""
#     yaml = COMPOSE_DEV if env == 'dev' else COMPOSE_PROD
#     sh.ckan(yaml, container_name, *args)

if __name__ == '__main__':
    cli()
