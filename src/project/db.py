import aiomysql
from typing import Any, List, Dict, Tuple
from datetime import datetime


async def create_project_db(
    conn: aiomysql.Connection,
    project_name: str,
    deadline: datetime,
    organization_id: int,
) -> int | None:
    query = "INSERT INTO projects (project_name, deadline, organization_id) VALUES (%s, %s, %s)"
    args = (project_name, deadline, organization_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
        return cursor.lastrowid


async def update_project_db(
    conn: aiomysql.Connection,
    organization_id: int,
    project_id: int,
    project_name: str | None = None,
    deadline: datetime | None = None,
):
    if project_name is None and deadline is None:
        return
    query = "UPDATE projects SET project_name={n}, deadline={d} WHERE id=%s".format(
        n="%s" if project_name is not None else "project_name",
        d="%s" if deadline is not None else "deadline",
    )
    args = []
    if project_name is not None:
        args.append(project_name)
    if deadline is not None:
        args.append(deadline)

    args.append(project_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, tuple(args))
        await conn.commit()
        return project_id


async def delete_project_db(
    conn: aiomysql.Connection,
    project_id: int,
):
    query = "DELETE FROM projects WHERE id = %s"
    args = (project_id,)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()


async def fetch_projects_db(
    conn: aiomysql.Connection,
    organization_id: int,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    query = "SELECT * FROM projects WHERE organization_id = %s ORDER BY updated_at DESC LIMIT %s OFFSET %s"
    args = (organization_id, limit, offset)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchall()
