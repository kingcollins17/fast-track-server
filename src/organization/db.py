import aiomysql
from typing import List, Any, Dict, Tuple

# import other db access modules


async def create_organization_db(
    conn: aiomysql.Connection,
    owner_id: int,
    name: str,
    org_type: str = "default",
):
    query = "INSERT INTO organizations (organization_name, type, owner_id) VALUES (%s, %s, %s)"
    args = (name, org_type, owner_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()


async def find_organization_db(
    conn: aiomysql.Connection,
    org_id: int,
) -> Dict | None:
    query = "SELECT * FROM organizations WHERE id = %s"
    args = (org_id,)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchone()


async def fetch_member_organizations_db(
    conn: aiomysql.Connection,
    account_id: int,
    limit=100,
    offset=0,
):
    query = "SELECT organization_members.id as member_id, organizations.* FROM organization_members LEFT JOIN organizations ON organization_members.organization_id = organizations.id WHERE organization_members.account_id = %s LIMIT %s OFFSET %s"
    args = (account_id, limit, offset)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchall()


async def fetch_created_organizations_db(
    conn: aiomysql.Connection,
    account_id: int,
    limit: int = 100,
    offset: int = 0,
):
    query = "SELECT * FROM organizations WHERE owner_id = %s LIMIT %s OFFSET %s"
    args = (account_id, limit, offset)
    print(query)
    print(args)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchall()


async def update_organization_db(
    conn: aiomysql.Connection,
    org_id: int,
    owner_id: int,
    name: str,
):
    query = "UPDATE organizations SET organization_name = %s WHERE id = %s AND owner_id = %s"
    args = (name, org_id, owner_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()


async def delete_organization_db(
    conn: aiomysql.Connection,
    owner_id: int,
    organization_id: int,
):
    query = "DELETE FROM organizations WHERE owner_id = %s AND id = %s"
    args = (owner_id, organization_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
