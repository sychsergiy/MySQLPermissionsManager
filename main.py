import typing as t

from mysql.connector import connect
from mysql.connector.connection_cext import CMySQLConnection


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
    cursor.execute(query)
    cursor.close()


def grant_all(connection: CMySQLConnection, user: str):
    query = "GRANT ALL PRIVILEGES ON *.* TO '{}'@'localhost';".format(user)
    execute_query(connection, query)


def revoke_all(connection: CMySQLConnection, user: str):
    query = "REVOKE ALL PRIVILEGES ON *.* FROM '{}'@'localhost';".format(user)
    execute_query(connection, query)


def execute_grant_request():
    pass


def main():
    connection = create_connection()
    revoke_all(connection, 'test_user')
    connection.close()


if __name__ == "__main__":
    main()
