import aiomysql
from typing import List, Any, Tuple, Dict


async def fetch_teams_db(
    conn: aiomysql.Connection,
    organization_id: int | None = None,
    project_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
):
    assert (
        organization_id is not None or project_id is not None
    ), "Both arguments cannot be None at the same time"
    filter = ""
    if organization_id is not None:
        filter += "organizations.id=%s"
        if project_id is not None:
            filter += " AND projects.id=%s"
    elif project_id is not None:
        filter += "projects.id=%s"
    query = "SELECT * FROM teams LEFT JOIN projects ON teams.project_id=projects.id LEFT JOIN organizations ON projects.organization_id = organizations.id WHERE {filter} LIMIT %s OFFSET %s".format(
        filter=filter
    )
    args = []
    if organization_id is not None:
        args.append(organization_id)
    if project_id is not None:
        args.append(project_id)

    args = tuple([*args, limit, offset])
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchall()


async def create_team_db(conn: aiomysql.Connection, team_name: str, project_id: int):
    query = "INSERT INTO teams (team_name, project_id) VALUES (%s, %s)"
    args = (team_name, project_id)
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
    team_id: int,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict]:
    query = "SELECT * FROM team_members LEFT JOIN accounts ON team_members.account_id=accounts.id LEFT JOIN teams ON team_members.team_id=teams.id WHERE team_members.team_id=%s LIMIT %s OFFSET %s"
    args = (team_id, limit, offset)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return cursor.fetchall()


async def create_team_member_db(
    conn: aiomysql.Connection,
    account_id: int,
    team_id: int,
):
    query = "INSERT INTO team_members (team_id, account_id) VALUES (%s, %s)"
    args = (team_id, account_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
        return cursor.lastrowid


async def delete_team_member_db(
    conn: aiomysql.Connection,
    team_membership_id: int,
):
    query = "DELETE FROM team_members WHERE id = %s"
    args = (team_membership_id,)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
