import click
import logging
from mlops.Experiment import Experiment
from mlops.release.Release import Release
from mlops._version import __version__
logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help'],
                    'show_default': True}


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('no idea')
    ctx.exit()


@click.group('cli', context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.version_option(__version__)
def cli(ctx):
    """
    CLI tool for csc-mlops projects.

    EXAMPLE:
    mlops run scripts/train.py

    """
    pass


@cli.command('run', context_settings=CONTEXT_SETTINGS)
@click.argument('script', type=click.Path(exists=True))
@click.option('-c', '--config', 'config_path', help='Path to config file storing parameters for this run',
              default='config/config.cfg', type=click.Path())
@click.option('-n', '--name', 'run_name', help='MLFlow run name', default=None)
@click.option('-l', '--logging_level', 'logging_level', help='Logging level', default='INFO')
@click.option('-sh', '--shared_memory', 'shared_memory', help='shared_memory docker ag', default='8gb')
@click.option('-r', '--rebuild_docker', 'rebuild_docker', help='Rebuild docker container on run', is_flag=True,
              show_default=True, default=False)
@click.option('--ignore_git_check', is_flag=True, show_default=True, default=False,
              help='TESTING ONLY - ignore git checks, occasionally it might be necessary to ignore the git checks for example, offline testing, do not use this feature if working on tracked models')
def run(script, config_path, run_name, ignore_git_check, shared_memory, logging_level, rebuild_docker):
    """
    Runs python project using csc-mlops framework.

    SCRIPT is the path to the script to run e.g. scripts/train.py
    """

    # create Experiment
    exp = Experiment(script,
                     config_path=config_path,
                     ignore_git_check=ignore_git_check
                     )

    # run Experiment
    exp.run(docker_args={},
            run_name=run_name,
            rebuild_docker=rebuild_docker,
            shared_memory=shared_memory,
            )


@cli.command('release', context_settings=CONTEXT_SETTINGS)
@click.argument('release_target', default=None)
@click.option('-s', '--release_source', 'release_source', help='release_source', default='mlflow')
def release(release_target, release_source):
    """
    Performs actions associated with release

    :return: 
    """
    candidate = Release(release_target, release_source)
    candidate.release()


if __name__ == '__main__':
    cli()
