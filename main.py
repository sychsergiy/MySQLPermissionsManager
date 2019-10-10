import typing as t

from mysql.connector import connect
from mysql.connector.connection_cext import CMySQLConnection
from app import grants
from app.destination import Destination, check_grant_destination


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


def grant_all(connection: CMySQLConnection, user: str):
    query = "GRANT ALL PRIVILEGES ON *.* TO '{}'@'localhost';".format(user)
    execute_query(connection, query)


def revoke_all(connection: CMySQLConnection, user: str):
    query = "REVOKE ALL PRIVILEGES ON *.* FROM '{}'@'localhost';".format(user)
    execute_query(connection, query)


class GrantRequest(object):
    def __init__(self, grant: grants.Grant, destination: Destination):
        self.grant = grant
        self.destination = destination

    def execute(self, user: str, connection: CMySQLConnection):
        error_message = check_grant_destination(self.grant, self.destination)
        if error_message:
            print(error_message)
        else:
            query = self.build_grant_query(user)
            execute_query(connection, query)

    def build_grant_query(self, user: str) -> str:

        query = "GRANT {} ON *.* TO '{}'@'localhost';".format(
            self.grant.action,
            user
        )
        return query

    def build_revoke_query(self, user: str) -> str:
        query = "REVOKE {} ON *.* FROM '{}'@'localhost';".format(
            self.grant.action,
            user
        )
        return query


def execute_grant_request(connection):
    request = GrantRequest(grants.GRANTS[3], Destination(True))
    request.execute("test_user", connection)


def main():
    connection = create_connection()
    execute_grant_request(connection)
    # revoke_all(connection, 'test_user')
    connection.close()


if __name__ == "__main__":
    main()
