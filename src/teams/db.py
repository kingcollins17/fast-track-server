import aiomysql
from typing import List, Any, Tuple, Dict


async def fetch_teams_db(
    conn: aiomysql.Connection,
    organization_id: int,
    limit: int = 100,
    offset: int = 0,
):
    query = "SELECT * FROM teams WHERE organization_id=%s ORDER BY created_at DESC LIMIT %s OFFSET %s"
    args = (organization_id, limit, offset)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchall()


async def create_team_db(
    conn: aiomysql.Connection, team_name: str, organization_id: int
):
    query = "INSERT INTO teams (team_name, organization_id) VALUES (%s, %s)"
    args = (team_name, organization_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
        return cursor.lastrowid


async def update_team_db():
    pass


async def delete_team_db(
    conn: aiomysql.Connection,
    team_id: int,
):
    query = "DELETE FROM teams WHERE id = %s"
    args = (team_id,)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()


async def fetch_team_members_db(
    conn: aiomysql.Connection,
    team_id: int | None = None,
    organization_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict]:
    assert (
        team_id is not None or organization_id is not None
    ), "Must be called with at least one argument"
    query = "SELECT accounts.id as account_id, accounts.username, accounts.fullname, accounts.email, teams.id as team_id, teams.team_name FROM team_members LEFT JOIN accounts ON team_members.account_id=accounts.id LEFT JOIN teams ON team_members.team_id=teams.id WHERE team_members.team_id=%s LIMIT %s OFFSET %s"
    args = (team_id, limit, offset)
    if organization_id is not None:
        query = "SELECT accounts.id as account_id, accounts.username, accounts.fullname, accounts.email, teams.id as team_id, teams.team_name, organizations.organization_name FROM team_members LEFT JOIN accounts ON team_members.account_id=accounts.id LEFT JOIN teams ON team_members.team_id=teams.id LEFT JOIN organizations ON teams.organization_id=organizations.id WHERE organizations.id = %s LIMIT %s OFFSET %s"
        args = (organization_id, limit, offset)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchall()


async def create_team_member_db(
    conn: aiomysql.Connection,
    account_id: int,
    team_id: int,
) -> int | None:
    query = "INSERT INTO team_members (team_id, account_id) VALUES (%s, %s)"
    args = (team_id, account_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
        return cursor.lastrowid


async def delete_team_member_db(
    conn: aiomysql.Connection,
    team_member_id: int,
):
    query = "DELETE FROM team_members WHERE id = %s"
    args = (team_member_id,)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
