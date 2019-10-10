import typing as t
from app import grants

from app.grants import Grant


class TargetQueryParts(t.NamedTuple):
    database: str = ""
    table: str = ""
    columns: str = ""


class TargetLevelException(Exception):
    pass


class AbstractTarget(object):
    level: grants.Levels = None

    def check_grant_level(self, grant: Grant):
        if not {self.level}.issubset(grant.levels):
            raise TargetLevelException(
                f"{grant.action} can't be used with target.\n"
                f"Target level: {str(self.level)}\n"
                f"Grant levels: {str(grant.levels)}\n"
            )

    def get_query_parts(self) -> TargetQueryParts:
        raise NotImplementedError


class GlobalTarget(AbstractTarget):
    level = grants.Levels.GLOBAL

    def get_query_parts(self) -> TargetQueryParts:
        return TargetQueryParts("*", "*")


class DatabaseTarget(AbstractTarget):
    level = grants.Levels.DATABASE

    def __init__(self, database: str):
        self.database = database

    def get_query_parts(self) -> TargetQueryParts:
        return TargetQueryParts(self.database, "*")


class TableTarget(AbstractTarget):
    level = grants.Levels.TABLE

    def __init__(self, database: str, table: str):
        self.database = database
        self.table = table

    def get_query_parts(self) -> TargetQueryParts:
        return TargetQueryParts(self.database, self.table)


class ColumnsTarget(AbstractTarget):
    level = grants.Levels.COLUMN

    def __init__(self, database: str, table: str, columns: t.List[str]):
        self.database = database
        self.table = table
        self.columns = columns

    def get_query_parts(self):
        columns_part = "({})".format(','.join(self.columns))
        return TargetQueryParts(self.database, self.table, columns_part)


class Target(t.NamedTuple):
    global_: bool = False
    database: str = ""
    table: str = ""
    columns: t.List[str] = None
