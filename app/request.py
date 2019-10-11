import sys

from mysql.connector import ProgrammingError
from mysql.connector.connection_cext import CMySQLConnection

from app import grants
from app.connector import create_connection
from app.target import AbstractTarget, TargetLevelException
from app.query_builder import (
    BaseQueryBuilder,
    GrantQueryBuilder,
    RevokeQueryBuilder,
)


class Request(object):
    def __init__(self, grant: grants.Grant, target: AbstractTarget,
                 query_builder: BaseQueryBuilder):
        self.grant = grant
        self.target = target
        self.query_builder = query_builder

    def _check_target_grant_level(self):
        try:
            self.target.check_grant_level(self.grant)
        except TargetLevelException as e:
            print(e)
            sys.exit(1)

    def execute(self, user: str):
        self._check_target_grant_level()

        query = self.query_builder.build(user)
        connection = create_connection()
        execute_query(connection, query)
        execute_query(connection, "FLUSH PRIVILEGES;")
        connection.close()


def execute_grant_request(grant: grants.Grant, target: AbstractTarget,
                          user: str):
    query_builder = GrantQueryBuilder(grant.action, target)
    request = Request(grant, target, query_builder)
    print(f"Executing request grant {grant.action} to {user}")
    request.execute(user)


def execute_revoke_request(grant: grants.Grant, target: AbstractTarget,
                           user: str):
    query_builder = RevokeQueryBuilder(grant.action, target)
    request = Request(grant, target, query_builder)
    print(f"Executing request revoke {grant.action} from {user}")
    request.execute(user)


def execute_query(connection: CMySQLConnection, query: str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except ProgrammingError as e:
        print(e)
    cursor.close()
