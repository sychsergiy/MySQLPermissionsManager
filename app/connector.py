import sys
from contextlib import contextmanager

from mysql.connector import connect
from mysql.connector.connection_cext import CMySQLConnection
from mysql.connector.errors import ProgrammingError

from app import auth


def create_connection():
    """
    CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
    GRANT ALL PRIVILEGES on *.* to 'admin'@'localhost';
    GRANT GRANT OPTION on *.* to 'admin'@'localhost;
    """
    creds = auth.access()
    try:
        cnx = connect(
            user=creds.username, password=creds.password, host="127.0.0.1"
        )
    except ProgrammingError as e:
        print(e)
        sys.exit(1)
    return cnx


@contextmanager
def connection():
    conn = create_connection()
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def cursor(conn: CMySQLConnection):
    cur = conn.cursor()
    try:
        yield cur
    finally:
        cur.close()
