import pytest

from app.destination import check_grant_destination, Destination
from app import grants


def test_check_grant_destination():
    result = check_grant_destination(
        grants.Grant("ALTER", grants.only_global), Destination(global_=True)
    )
    assert result == ""


def test_check_grant_destination_not_global():
    result = check_grant_destination(
        grants.Grant("ALTER", grants.only_column), Destination(global_=True)
    )
    assert result == "ALTER can't be used with global destination"
