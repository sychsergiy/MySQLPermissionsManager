from app.destination import Destination


class BaseQueryBuilder(object):
    def __init__(self, grant_action: str, destination: Destination):
        self.destination = destination
        self.grant_action = grant_action

    def _build_destination(self) -> str:
        if self.destination.global_:
            return "*.*"

        if self.destination.database and self.destination.table:
            return f"{self.destination.database}.{self.destination.table}"

        if self.destination.database and not self.destination.table:
            return f"{self.destination.database}.*"

        if not self.destination.database and self.destination.table:
            return f"*.{self.destination.table}"

        raise NotImplementedError("Columns not implemented, or bug builder")

    def build(self, user: str) -> str:
        raise NotImplementedError


class GrantQueryBuilder(BaseQueryBuilder):
    def build(self, user: str) -> str:
        destination_part = self._build_destination()
        query = "GRANT {action} ON {destination} TO \'{user}\'@\'localhost\'".format(
            action=self.grant_action, destination=destination_part, user=user
        )
        return query


class RevokeQueryBuilder(BaseQueryBuilder):
    def build(self, user: str) -> str:
        destination_part = self._build_destination()
        query = "REVOKE {action} ON {destination} FROM \'{user}\'@\'localhost\'".format(
            action=self.grant_action, destination=destination_part, user=user
        )
        return query
