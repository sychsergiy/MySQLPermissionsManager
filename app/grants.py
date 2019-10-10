import typing as t

from enum import Enum


class Levels(Enum):
    GLOBAL = 0
    DATABASE = 1
    TABLE = 2
    COMMAND = 3
    COLUMN = 4
    ROUTINE = 5


only_global = {Levels.GLOBAL}
only_db = {Levels.DATABASE}
only_table = {Levels.TABLE}
only_column = {Levels.COLUMN}

global_db = only_global | only_db
global_db_routine = global_db | {Levels.ROUTINE}
global_db_table = global_db | only_table
global_db_table_routine = global_db_routine | only_table
global_db_table_column = global_db_table | only_column


class Grant(t.NamedTuple):
    action: str
    levels: t.Set[Levels]


GRANTS = [
    Grant("ALL", set()),
    Grant("ALTER", global_db_table),
    Grant("ALTER ROUTINE", global_db_routine),
    Grant("CREATE", global_db_table),
    Grant("CREATE ROLE", only_global),
    Grant("CREATE ROUTINE", global_db),
    Grant("CREATE TABLESPACE", only_global),
    Grant("CREATE TEMPORARY TABLES", global_db),
    Grant("CREATE USER", only_global),
    Grant("CREATE VIEW", global_db_table),
    Grant("DELETE", global_db_table),
    Grant("DROP", global_db_table),
    Grant("DROP ROLE", only_global),
    Grant("EVENT", global_db),
    Grant("EXECUTE", global_db_routine),
    Grant("FILE", only_global),
    Grant("GRANT OPTION", global_db_table_routine),
    Grant("INDEX", global_db_table),
    Grant("INSERT", global_db_table_column),
    Grant("LOCK TABLE", global_db),
    Grant("PROCESS", only_global),
    Grant("REFERENCES", global_db_table_column),
    Grant("RELOAD", only_global),
    Grant("REPLICATION CLIENT", only_global),
    Grant("REPLICATION SLAVE", only_global),
    Grant("SELECT", global_db_table_column),
    Grant("SHOW DATABASES", only_global),
    Grant("SHOW VIEW", global_db_table),
    Grant("SHUTDOWN", only_global),
    Grant("SUPER", only_global),
    Grant("TRIGGER", global_db_table),
    Grant("UPDATE", global_db_table_column),
    Grant("USAGE", set()),
]
