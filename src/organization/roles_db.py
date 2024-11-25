import aiomysql
from typing import List, Any, Dict, Tuple


async def create_organization_role_db(
    conn: aiomysql.Connection,
    org_id: int,
    role_name: str,
    # role permissions
    can_assign_tasks: bool = False,
    can_review_tasks: bool = False,
    can_create_issue: bool = False,
    can_create_feature: bool = False,
    can_create_teams: bool = False,
    can_assign_to_teams: bool = False,
    can_assign_roles: bool = False,
    can_send_invites: bool = False,
):
    query = "INSERT INTO organization_roles (organization_id, role, can_assign_tasks, can_review_tasks, can_create_issue, can_create_feature, can_create_teams, can_assign_to_teams, can_assign_roles, can_send_invites) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    args = (
        org_id,
        role_name,
        can_assign_tasks,
        can_review_tasks,
        can_create_issue,
        can_create_feature,
        can_create_teams,
        can_assign_to_teams,
        can_assign_roles,
        can_send_invites,
    )
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()


async def fetch_organization_roles_db(conn: aiomysql.Connection, organization_id: int):
    query = "SELECT * FROM organization_roles WHERE organization_id = %s"
    args = (organization_id,)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        result: List[Dict[str, Any]] = await cursor.fetchall()
        for row in result:
            for k, v in row.items():
                if k.startswith("can"):
                    row[k] = bool(v)
        return result


async def fetch_member_assigned_roles_db(
    conn: aiomysql.Connection,
    member_id: int,
    organization_id: int,
):
    query = "SELECT organization_roles.* FROM member_roles LEFT JOIN organization_roles ON organization_roles.id = member_roles.role_id WHERE member_id=%s AND organization_roles.organization_id=%s"
    args = (member_id, organization_id)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        result: List[Dict[str, Any]] = await cursor.fetchall()
        for row in result:
            for key, value in row.items():
                if key.startswith("can"):
                    row[key] = bool(row[key])

        return result


async def find_organization_role_db(
    conn: aiomysql.Connection,
    role_id: int,
):
    query = "SELECT * FROM organization_roles WHERE id =%s"
    args = (role_id,)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchone()


async def assign_member_role_db(
    conn: aiomysql.Connection,
    member_id: int,
    role_id: int,
):
    query = "INSERT INTO member_roles (member_id, role_id) VALUES (%s, %s)"
    args = (member_id, role_id)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        await conn.commit()
