import aiomysql
import json
from typing import List, Any, Tuple, Dict
from datetime import datetime


async def create_task_db(
    conn: aiomysql.Connection,
    name: str,
    deadline: datetime,
    feature_id: int,
    description: str | None = None,
    parent_task_id: int | None = None,
    team_id: int | None = None,
    account_id: int | None = None,
    **requirements,
):
    """values of requirements should be a valid requirements type (link, picture)"""
    assert (
        team_id is not None or account_id is not None
    ), "Task must be assigned to a Team or Individual at creation"
    if len(requirements.keys()) == 0:
        requirements = {}
    else:
        requirements = {k: v for k, v in requirements.items()}
    query = "INSERT INTO tasks (name, deadline, description, requirements, feature_id, parent_task_id, assigned_team_id, assigned_account_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    args = (
        name,
        deadline,
        description,
        json.dumps(requirements),
        feature_id,
        parent_task_id,
        team_id,
        account_id,
    )
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
        return cursor.lastrowid


async def fetch_tasks_db(
    conn: aiomysql.Connection,
    feature_id: int | None = None,
    project_id: int | None = None,
    organization_id: int | None = None,
    limit: int = 200,
    offset: int = 0,
) -> List[Dict]:
    assert (
        organization_id is not None or feature_id is not None
    ), "Must be called with either organization_id or feature_id"
    query = "SELECT tasks.*, parent_tasks.name as parent_task_name, features.name as feature_name, projects.id as project_id, projects.project_name FROM tasks LEFT JOIN features ON tasks.feature_id=features.id LEFT JOIN projects ON features.project_id=projects.id LEFT JOIN organizations ON projects.organization_id=organizations.id LEFT JOIN tasks as parent_tasks ON tasks.parent_task_id=parent_tasks.id WHERE {column}= %s ORDER BY tasks.created_at DESC LIMIT %s OFFSET %s".format(
        column="organizations.id"
        if organization_id is not None
        else "projects.id"
        if project_id is not None
        else "tasks.feature_id"
    )
    args = (organization_id or project_id or feature_id, limit, offset)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        result = await cursor.fetchall()
        for data in result:
            req = "requirements"
            data[req] = json.loads(data[req])
        return result


async def delete_task_db(conn: aiomysql.Connection, task_id: int):
    query = "DELETE FROM tasks WHERE id = %s"
    args = (task_id,)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
