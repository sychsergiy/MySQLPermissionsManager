import sys

from mysql.connector import ProgrammingError
from mysql.connector.connection_cext import CMySQLConnection

from app import grants
from app.connector import connection, cursor
from app.query_builder import (
    BaseQueryBuilder,
    GrantQueryBuilder,
    RevokeQueryBuilder,
)
from app.target import AbstractTarget, TargetLevelException


class Request(object):
    def __init__(
        self,
        grant: grants.Grant,
        target: AbstractTarget,
        query_builder: BaseQueryBuilder,
    ):
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

        with connection() as conn:
            execute_query(conn, query)
            execute_query(conn, "FLUSH PRIVILEGES;")


def execute_grant_request(
    grant: grants.Grant, target: AbstractTarget, user: str
):
    query_builder = GrantQueryBuilder(grant.action, target)
    request = Request(grant, target, query_builder)
    print(f"Executing request grant {grant.action} to {user}")
    request.execute(user)


def execute_revoke_request(
    grant: grants.Grant, target: AbstractTarget, user: str
):
    query_builder = RevokeQueryBuilder(grant.action, target)
    request = Request(grant, target, query_builder)
    print(f"Executing request revoke {grant.action} from {user}")
    request.execute(user)


def execute_query(conn: CMySQLConnection, query: str):
    with cursor(conn) as curs:
        try:
            curs.execute(query)
        except ProgrammingError as e:
            print(e)
