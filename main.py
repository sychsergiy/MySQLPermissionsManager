from mysql.connector.connection_cext import CMySQLConnection

from app import grants
from app.connector import create_connection
from app.grants import Grant
from app.target import AbstractTarget
from app.query_builder import BaseQueryBuilder, GrantQueryBuilder, \
    RevokeQueryBuilder


def execute_query(connection: CMySQLConnection, query: str):
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()


class Request(object):
    def __init__(self, grant: grants.Grant, target: AbstractTarget,
                 query_builder: BaseQueryBuilder):
        self.grant = grant
        self.target = target
        self.query_builder = query_builder

    def execute(self, user: str):
        self.target.check_grant_level(self.grant)
        query = self.query_builder.build(user)
        connection = create_connection()
        execute_query(connection, query)
        execute_query(connection, "FLUSH PRIVILEGES;")
        connection.close()


def execute_grant_request(grant: Grant, target: AbstractTarget, user: str):
    query_builder = GrantQueryBuilder(grant.action, target)
    request = Request(grant, target, query_builder)
    request.execute(user)


def execute_revoke_request(grant: Grant, target: AbstractTarget, user: str):
    query_builder = RevokeQueryBuilder(grant.action, target)
    request = Request(grant, target, query_builder)
    request.execute(user)


def main():
    create_connection()


if __name__ == "__main__":
    main()
