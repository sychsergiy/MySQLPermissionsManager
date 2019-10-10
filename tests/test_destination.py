import pytest

from app.target import check_grant_target, Target
from app import grants


def test_check_grant_target():
    result = check_grant_target(
        grants.Grant("ALTER", grants.only_global), Target(global_=True)
    )
    assert result == ""


def test_check_grant_target_not_global():
    result = check_grant_target(
        grants.Grant("ALTER", grants.only_column), Target(global_=True)
    )
    assert result == "ALTER can't be used with global target"
