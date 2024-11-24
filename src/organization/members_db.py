import aiomysql
from typing import List, Dict, Any


async def fetch_organization_members_db(
    conn: aiomysql.Connection,
    org_id: int,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict]:
    query = "SELECT organization_members.id as member_id, accounts.* FROM organization_members LEFT JOIN accounts ON accounts.id = organization_members.account_id WHERE organization_id = %s LIMIT %s OFFSET %s"
    args = (org_id, limit, offset)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        result = await cursor.fetchall()
        for row in result:
            row["active"] = bool(row["active"])
            row["email_verified"] = bool(row["email_verified"])
            row.pop("password")
        return result


async def find_organization_member_db(
    conn: aiomysql.Connection,
    organization_id: int,
    account_id: int | None = None,
    member_id: int | None = None,
) -> Dict | None:
    assert (
        account_id is not None or member_id is not None
    ), "account_id or member_id must be passed as a filter"
    query = "SELECT * FROM organization_members WHERE {filter}=%s AND organization_id = %s".format(
        filter="id" if member_id else "account_id"
    )
    args = (member_id or account_id, organization_id)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchone()


async def add_organization_member_db(
    conn: aiomysql.Connection,
    org_id: int,
    account_id: int,
):
    query = (
        "INSERT INTO organization_members (account_id, organization_id) VALUES (%s, %s)"
    )
    args = (account_id, org_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()


async def delete_organization_member_db(
    conn: aiomysql.Connection,
    organization_id: int,
    member_id: int,
):
    query = "DELETE FROM organization_members WHERE id = %s AND organization_id = %s"
    args = (member_id, organization_id)
    async with conn.cursor() as cursor:
        await cursor.execute(query, args)
        await conn.commit()
