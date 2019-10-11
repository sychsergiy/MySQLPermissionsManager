from enum import Enum

from app.target import GlobalTarget, DatabaseTarget, TableTarget


class TargetTypes(Enum):
    GLOBAL = "global"
    DATABASE = "db"
    TABLE = "table"
    # todo: add columns


class TargetTypeReader(object):
    @staticmethod
    def read_database():
        return input("Input database name or '*': ")

    @staticmethod
    def read_table():
        return input("Input table name or '*': ")


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

    # todo: add_columns
