import sys

import click

from app.grants import Grant
from app.request import execute_revoke_request, execute_grant_request
from app.target import AbstractTarget
from app.target_types import TargetTypes, TargetTypeCreator
from app import grants
from app import auth


def get_available_actions_map():
    return {'_'.join(item.action.lower().split(" ")): item for item in
            grants.GRANTS}


class CommandExecutor(object):
    def check_target_type(self, target_type: str) -> bool:
        target_types = [item.value for item in TargetTypes]
        if target_type not in target_types:
            print(f"Not recognized target type: {target_type}")
            print(f"Available target types: {', '.join(target_types)}")
            return False
        return True

    def check_action(self, action: str) -> bool:
        available_action_map = get_available_actions_map()
        if action not in available_action_map.keys():
            print(f"Not recognized action: {action}")
            actions = ', '.join(available_action_map.keys())
            print(f"Available actions: {actions}")
            return False
        return True

    def execute(self, action: str, target_type: str) -> [AbstractTarget, Grant]:
        if not self.check_action(action):
            sys.exit(1)
        grant_ = get_available_actions_map()[action]

        if not self.check_target_type(target_type):
            sys.exit(1)
        target_type_creator = TargetTypeCreator()
        target = target_type_creator.create(target_type)

        return target, grant_


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
    executor = CommandExecutor()
    target, grant_ = executor.execute(action, target_type)
    execute_revoke_request(grant_, target, username)


@cli.command()
@click.argument('action')
@click.argument('username')
@click.argument('target_type')
def grant(action: str, username: str, target_type: str):
    executor = CommandExecutor()
    target, grant_ = executor.execute(action, target_type)
    execute_grant_request(grant_, target, username)


if __name__ == "__main__":
    cli()
