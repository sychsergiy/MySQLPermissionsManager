import click

from app.grants import get_available_actions_map
from app.cli_helper import check_action, check_target_type
from app.request import execute_revoke_request, execute_grant_request
from app.target_types import TargetTypeCreator
from app import auth


@click.group()
def cli():
    pass


@cli.command()
@click.argument("username")
@click.argument("password")
def login(username: str, password: str):
    auth.login(username, password)


@cli.command()
def logout():
    auth.logout()


@cli.command()
@click.argument('action')
@click.argument('username')
@click.argument('target_type')
def revoke(action: str, username: str, target_type: str):
    check_action(action)
    grant_ = get_available_actions_map()[action]

    check_target_type(target_type)
    target = TargetTypeCreator().create(target_type)

    execute_revoke_request(grant_, target, username)


@cli.command()
@click.argument('action')
@click.argument('username')
@click.argument('target_type')
def grant(action: str, username: str, target_type: str):
    check_action(action)
    grant_ = get_available_actions_map()[action]

    check_target_type(target_type)
    target = TargetTypeCreator().create(target_type)

    execute_grant_request(grant_, target, username)


if __name__ == "__main__":
    cli()
