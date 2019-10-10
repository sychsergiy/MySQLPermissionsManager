from app.target import AbstractTarget, TargetQueryParts


# todo: add columns target building

class BaseQueryBuilder(object):
    def __init__(self, grant_action: str, target: AbstractTarget):
        self.target = target
        self.grant_action = grant_action

    @staticmethod
    def get_db_table_part(query_parts: TargetQueryParts) -> str:
        return f"{query_parts.database}.{query_parts.table}"

    @staticmethod
    def get_columns_part(query_parts: TargetQueryParts) -> str:
        return "({})".format(','.join(query_parts.columns))

    def build(self, user: str) -> str:
        raise NotImplementedError


class GrantQueryBuilder(BaseQueryBuilder):
    def build(self, user: str) -> str:
        query_parts = self.target.get_query_parts()
        target_part = self.get_db_table_part(query_parts)

        if query_parts.columns:
            raise NotImplementedError("Columns not implemented")
        query = "GRANT {action} ON {target} TO \'{user}\'@\'localhost\'".format(
            action=self.grant_action, target=target_part, user=user
        )
        return query


class RevokeQueryBuilder(BaseQueryBuilder):
    def build(self, user: str) -> str:
        query_parts = self.target.get_query_parts()
        target_part = self.get_db_table_part(query_parts)
        if query_parts.columns:
            raise NotImplementedError("Columns not implemented")
        query = "REVOKE {action} ON {target} FROM \'{user}\'@\'localhost\'".format(
            action=self.grant_action, target=target_part, user=user
        )
        return query
