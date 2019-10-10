from mysql.connector import connect
from mysql.connector.connection_cext import CMySQLConnection
from app import grants
from app.grants import Grant
from app.target import Target, check_grant_target
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
    def __init__(self, grant: grants.Grant, target: Target,
                 query_builder: BaseQueryBuilder):
        self.grant = grant
        self.target = target
        self.query_builder = query_builder

    def execute(self, user: str, connection: CMySQLConnection):
        error_message = check_grant_target(self.grant, self.target)
        if error_message:
            print(error_message)
        else:
            query = self.query_builder.build(user)
            execute_query(connection, query)
            execute_query(connection, "FLUSH PRIVILEGES;")


def execute_grant_request(grant: Grant, target: Target, user: str):
    query_builder = GrantQueryBuilder(grant.action, target)
    request = Request(grant, target, query_builder)
    connection = create_connection()
    request.execute(user, connection)


def execute_revoke_request(grant: Grant, target: Target, user: str):
    query_builder = RevokeQueryBuilder(grant.action, target)
    request = Request(grant, target, query_builder)
    connection = create_connection()
    request.execute(user, connection)


def main():
    pass


if __name__ == "__main__":
    main()
