from mlops.Experiment import Experiment
import click

CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help'],
                    'show_default': True}


@click.group('cli', context_settings=CONTEXT_SETTINGS)
def cli():
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
@click.option('--ignore_git_check', is_flag=True, show_default=True, default=False,
              help='TESTING ONLY - ignore git checks, occasionally it might be necessary to ignore the git checks for example, offline testing, do not use this feature if working on tracked models')
def run(script, config_path, run_name, ignore_git_check, logging_level):
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
            )


if __name__ == '__main__':
    cli()
