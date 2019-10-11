import typing as t
from enum import Enum

from app.target import ColumnsTarget, DatabaseTarget, GlobalTarget, TableTarget


class TargetTypes(Enum):
    GLOBAL = "global"
    DATABASE = "db"
    TABLE = "table"
    COLUMNS = "cols"


class TargetTypeReader(object):
    @staticmethod
    def read_database() -> str:
        return input("Input database name or '*': ")

    @staticmethod
    def read_table() -> str:
        return input("Input table name or '*': ")

    @staticmethod
    def read_columns() -> t.List[str]:
        cols = input("Input columns names with '|' delimiter: ")
        return cols.split("|")


class TargetTypeCreator(object):
    def __init__(self):
        self._reader = TargetTypeReader()

    def create(self, target_type: str):
        if target_type == TargetTypes.GLOBAL.value:
            return self.create_global_target()
        elif target_type == TargetTypes.DATABASE.value:
            return self.create_database_target()
        elif target_type == TargetTypes.TABLE.value:
            return self.create_table_target()
        elif target_type == TargetTypes.COLUMNS.value:
            return self.create_columns_target()
        else:
            raise RuntimeError("Other target types no implemented")

    def create_columns_target(self) -> ColumnsTarget:
        db = self._reader.read_database()
        table = self._reader.read_table()
        cols = self._reader.read_columns()
        return ColumnsTarget(db, table, cols)

    @staticmethod
    def create_global_target():
        return GlobalTarget()

    def create_database_target(self):
        database = self._reader.read_database()
        return DatabaseTarget(database)

    def create_table_target(self):
        database = self._reader.read_database()
        table = self._reader.read_table()
        return TableTarget(database, table)
