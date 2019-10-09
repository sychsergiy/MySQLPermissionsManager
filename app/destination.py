import typing as t
from app import grants

from app.grants import Grant


class Destination(t.NamedTuple):
    global_: bool = False
    database: str = ""
    table: str = ""
    columns: t.List[str] = None


def check_grant_destination(
        grant: Grant,
        destination: Destination,
) -> str:
    """
    returns error message if validation fail's, empty string other way
    """
    if destination.global_ and not grants.only_global.issubset(grant.levels):
        return f"{grant.action} can't be used with global destination"

    if destination.database and not grants.only_db.issubset(grant.levels):
        return f"{grant.action} can't be used with database destination"

    if destination.table and not grants.only_table.issubset(grant.levels):
        return f"{grant.action} can't be used with table destination"

    if destination.columns and not grants.only_column.issubset(grant.levels):
        return f"{grant.action} can't be used with columns destination"
    return ""
