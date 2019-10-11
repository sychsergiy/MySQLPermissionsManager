import sys

from app.grants import get_available_actions_map
from app.target_types import TargetTypes


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
