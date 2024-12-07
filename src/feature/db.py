import aiomysql
from typing import List, Any, Dict, Tuple
from datetime import datetime


async def create_feature_db(
    conn: aiomysql.Connection,
    name: str,
    deadline: datetime,
    project_id: int,
    description: str = "",
) -> int | None:
    query = "INSERT INTO features (name, description, deadline, project_id) VALUES (%s, %s, %s, %s)"
    args = (name, description, deadline, project_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
        return cursor.lastrowid


async def fetch_features_db(
    conn: aiomysql.Connection,
    organization_id: int | None = None,
    project_id: int | None = None,
    limit: int = 200,
    offset: int = 0,
) -> List[Dict]:
    assert (
        organization_id is not None or project_id is not None
    ), "Must be called with at least 1 Argument"
    query = "SELECT * FROM features LEFT JOIN projects ON features.project_id=projects.id WHERE {column}=%s".format(
        column="projects.organization_id"
        if organization_id is not None
        else "features.project_id"
    )
    args = (organization_id or project_id,)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchall()


async def update_feature_db(
    conn: aiomysql.Connection,
    name: str | None = None,
    description: str | None = None,
    deadline: datetime | None = None,
):
    assert (
        name is not None or description is not None or deadline is not None
    ), "All arguments cannot be None at the same time"
    query = (
        "UPDATE features SET name={arg1}, description={arg2} deadline={arg3}".format(
            arg1="%s" if name is not None else "name",
            arg2="%s" if description is not None else "description",
            arg3="%s" if deadline is not None else "deadline",
        )
    )
    args = []
    if name is not None:
        args.append(name)

    if description is not None:
        args.append(description)

    if deadline is not None:
        args.append(deadline)

    async with conn.cursor() as cursor:
        await cursor.execute(query, tuple(args))
        await conn.commit()


async def delete_feature_db(
    conn: aiomysql.Connection,
    feature_id: int,
):
    query = "DELETE FROM features WHERE id = %s"
    args = (feature_id,)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
