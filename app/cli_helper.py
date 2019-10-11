import sys

from mysql.connector import ProgrammingError

from app.grants import get_available_actions_map
from app.target_types import TargetTypes
from app.connector import cursor, connection


def check_action(action: str):
    available_action_map = get_available_actions_map()
    if action not in available_action_map.keys():
        print(f"Not recognized action: {action}")
        actions = ', '.join(available_action_map.keys())
        print(f"Available actions: {actions}")
        sys.exit(1)


def check_target_type(target_type: str):
    target_types = [item.value for item in TargetTypes]
    if target_type not in target_types:
        print(f"Not recognized target type: {target_type}")
        print(f"Available target types: {', '.join(target_types)}")
        sys.exit(1)


def fetch_grants(user: str) -> list:
    with connection() as conn:
        with cursor(conn) as cur:
            query = f"SHOW GRANTS FOR '{user}'@'localhost'"
            try:
                cur.execute(query)
                items = cur.fetchall()
                return items
            except ProgrammingError as e:
                print(e)
                return []
