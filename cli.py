import sys

import click

from enum import Enum

from app.grants import Grant
from app.target import GlobalTarget, DatabaseTarget, TableTarget, AbstractTarget
from main import execute_revoke_request, execute_grant_request
from app import grants


def get_available_actions_map():
    return {'_'.join(item.action.lower().split(" ")): item for item in
            grants.GRANTS}


class TargetTypeReader(object):
    @staticmethod
    def read_database():
        return input("Input database name or '*': ")

    @staticmethod
    def read_table():
        return input("Input table name or '*': ")


class TargetTypeCreator(object):
    def __init__(self, reader: TargetTypeReader):
        self._reader = reader

    def create(self, target_type: str):
        if target_type == TargetTypes.GLOBAL.value:
            return self.create_global_target()
        elif target_type == TargetTypes.DATABASE.value:
            return self.create_database_target()
        elif target_type == TargetTypes.TABLE:
            return self.create_table_target()

    @staticmethod
    def create_global_target():
        return GlobalTarget()

    def create_database_target(self):
        database = self._reader.read_database()
        return DatabaseTarget(database)

    def create_table_target(self):
        database = self._reader.read_database()
        table = self._reader.read_table()
        return TableTarget(database, table)

    # todo: add_columns


class TargetTypes(Enum):
    GLOBAL = "global"
    DATABASE = "db"
    TABLE = "table"
    # todo: add columns


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
        target_type_creator = TargetTypeCreator(TargetTypeReader())
        target = target_type_creator.create(target_type)

        return target, grant_


@click.group()
def cli():
    pass


@cli.command()
def login():
    pass


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
