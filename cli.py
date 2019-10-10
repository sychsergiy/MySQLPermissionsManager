import click

from main import execute_revoke_request, execute_grant_request, \
    create_connection


@click.group()
def cli():
    pass


@cli.command()
def login():
    pass


@cli.command()
def grant():
    execute_grant_request(create_connection())


@cli.command()
def revoke():
    execute_revoke_request(create_connection())


if __name__ == "__main__":
    cli()
