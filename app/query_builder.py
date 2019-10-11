from app.target import AbstractTarget, TargetQueryParts


class BaseQueryBuilder(object):
    def __init__(self, grant_action: str, target: AbstractTarget):
        self.target = target
        self.grant_action = grant_action

    @staticmethod
    def get_db_table_part(query_parts: TargetQueryParts) -> str:
        return f"{query_parts.database}.{query_parts.table}"

    def build(self, user: str) -> str:
        raise NotImplementedError


class GrantQueryBuilder(BaseQueryBuilder):
    def build(self, user: str) -> str:
        query_parts = self.target.get_query_parts()
        target_part = self.get_db_table_part(query_parts)
        query = (
            "GRANT {action} {columns} ON {target} "
            "TO \'{user}\'@\'localhost\'"
                .format(action=self.grant_action, columns=query_parts.columns,
                        target=target_part, user=user
                        ))

        print(f"SQL query: {query}")
        return query


class RevokeQueryBuilder(BaseQueryBuilder):
    def build(self, user: str) -> str:
        query_parts = self.target.get_query_parts()
        target_part = self.get_db_table_part(query_parts)

        query = (
            "REVOKE {action} {columns} ON {target} "
            "FROM \'{user}\'@\'localhost\'"
                .format(
                action=self.grant_action, target=target_part, user=user,
                columns=query_parts.columns
            )
        )
        print(f"SQL query: {query}")
        return query
