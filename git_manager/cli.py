import click
from .git_manager import GitManager


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        status()


@cli.command()
@click.argument('path', type=click.Path(exists=True))
def add(path):
    gim = GitManager()
    gim.register(path)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
def remove(path):
    gim = GitManager()
    gim.deregister(path)


@cli.command()
def status():
    gim = GitManager()
    gim.status_check()


@cli.command()
def branch():
    gim = GitManager()
    gim.list_branches()


@cli.command()
def pull():
    gim = GitManager()
    gim.pull_all()


if __name__ == '__main__':
    cli()
