from app.target import Target


class BaseQueryBuilder(object):
    def __init__(self, grant_action: str, target: Target):
        self.target = target
        self.grant_action = grant_action

    def _build_target(self) -> str:
        if self.target.global_:
            return "*.*"

        if self.target.database and self.target.table:
            return f"{self.target.database}.{self.target.table}"

        if self.target.database and not self.target.table:
            return f"{self.target.database}.*"

        if not self.target.database and self.target.table:
            return f"*.{self.target.table}"

        if self.target.columns:
            raise NotImplementedError("Columns not implemented yet")

        raise Exception("Wrong target")

    def build(self, user: str) -> str:
        raise NotImplementedError


class GrantQueryBuilder(BaseQueryBuilder):
    def build(self, user: str) -> str:
        target_part = self._build_target()
        query = "GRANT {action} ON {target} TO \'{user}\'@\'localhost\'".format(
            action=self.grant_action, target=target_part, user=user
        )
        return query


class RevokeQueryBuilder(BaseQueryBuilder):
    def build(self, user: str) -> str:
        target_part = self._build_target()
        query = "REVOKE {action} ON {target} FROM \'{user}\'@\'localhost\'".format(
            action=self.grant_action, target=target_part, user=user
        )
        return query
