import typing as t

from mysql.connector import connect
from mysql.connector.connection_cext import CMySQLConnection
from app import grants
from app.destination import Destination, check_grant_destination
from app.query_builder import BaseQueryBuilder, GrantQueryBuilder, \
    RevokeQueryBuilder


def create_connection(user='admin', password='admin'):
    """
    CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
    GRANT ALL PRIVILEGES on *.* to 'admin'@'localhost';
    GRANT GRANT OPTION on *.* to 'admin'@'localhost;
    """
    cnx = connect(user=user, password=password,
                  host='127.0.0.1')
    # cnx.close()
    return cnx


def execute_query(connection: CMySQLConnection, query: str):
    cursor = connection.cursor()
    result = cursor.execute(query)
    cursor.close()


class Request(object):
    def __init__(self, grant: grants.Grant, destination: Destination,
                 query_builder: BaseQueryBuilder):
        self.grant = grant
        self.destination = destination
        self.query_builder = query_builder

    def execute(self, user: str, connection: CMySQLConnection):
        error_message = check_grant_destination(self.grant, self.destination)
        if error_message:
            print(error_message)
        else:
            query = self.query_builder.build(user)
            execute_query(connection, query)
            execute_query(connection, "FLUSH PRIVILEGES;")


def execute_grant_request(connection):
    query_builder = GrantQueryBuilder(grants.GRANTS[3].action,
                                      Destination(True))
    request = Request(grants.GRANTS[3], Destination(True), query_builder)
    request.execute("test_user", connection)


def execute_revoke_request(connection):
    query_builder = RevokeQueryBuilder(grants.GRANTS[3].action,
                                       Destination(True))
    request = Request(grants.GRANTS[3], Destination(True), query_builder)
    request.execute("test_user", connection)


def main():
    connection = create_connection()
    execute_revoke_request(connection)
    connection.close()


if __name__ == "__main__":
    main()
