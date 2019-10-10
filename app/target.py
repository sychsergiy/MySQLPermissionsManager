import typing as t
from app import grants

from app.grants import Grant


class Target(t.NamedTuple):
    global_: bool = False
    database: str = ""
    table: str = ""
    columns: t.List[str] = None


def check_grant_target(grant: Grant, target: Target) -> str:
    """
    returns error message if validation fail's, empty string other way
    """
    if target.global_ and not grants.only_global.issubset(grant.levels):
        return f"{grant.action} can't be used with global target"

    if target.database and not grants.only_db.issubset(grant.levels):
        return f"{grant.action} can't be used with database target"

    if target.table and not grants.only_table.issubset(grant.levels):
        return f"{grant.action} can't be used with table target"

    if target.columns and not grants.only_column.issubset(grant.levels):
        return f"{grant.action} can't be used with columns target"
    return ""


def get_available_actions_map():
    return {'_'.join(item.action.lower().split(" ")): item for item in
            grants.GRANTS}


def create_target(target_db: str,
                  target_table: str,
                  target_columns: str):
    if not target_db and not target_table and not target_columns:
        return Target(global_=True)

    if target_columns:
        target_columns_list = target_columns.split('|')
    else:
        target_columns_list = []
    return Target(database=target_db, table=target_table,
                  columns=target_columns_list)
