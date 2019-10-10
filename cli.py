import click

from main import execute_revoke_request, execute_grant_request
from app import grants


def get_available_actions_map():
    return {'_'.join(item.action.lower().split(" ")): item for item in
            grants.GRANTS}


@click.group()
def cli():
    pass


@cli.command()
def login():
    pass


@cli.command()
@click.argument('action')
@click.argument('username')
@click.option('-d', '--target-db')
@click.option('-t', '--target-table')
@click.option('-c', '--target-columns')  # in format col|col|col
def revoke(action: str, username: str, target_db: str,
           target_table: str,
           target_columns: str,
           ):
    available_action_map = get_available_actions_map()
    if action not in available_action_map.keys():
        print(f"Not recognized action: {action}")
        actions = ', '.join(available_action_map.keys())
        print(f"Available actions: {actions}")
        return

    grant_ = available_action_map[action]
    target = create_target(target_db, target_table, target_columns)
    execute_revoke_request(grant_, target, username)


@cli.command()
@click.argument('action')
@click.argument('username')
@click.option('-d', '--target-db')
@click.option('-t', '--target-table')
@click.option('-c', '--target-columns')  # in format col|col|col
def grant(action: str, username: str, target_db: str,
          target_table: str,
          target_columns: str,
          ):
    available_action_map = get_available_actions_map()
    if action not in available_action_map.keys():
        print(f"Not recognized action: {action}")
        actions = ', '.join(available_action_map.keys())
        print(f"Available actions: {actions}")
        return

    grant_ = available_action_map[action]
    target = create_target(target_db, target_table, target_columns)
    execute_grant_request(grant_, target, username)


if __name__ == "__main__":
    cli()
