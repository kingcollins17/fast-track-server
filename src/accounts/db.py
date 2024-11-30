from asyncio import Condition
import aiomysql
from typing import List, Dict, Annotated, Any, Union
from src.shared.security import *


async def create_account_db(
    connection: aiomysql.Connection,
    username: str,
    email: str,
    fullname: Union[str, None] = None,
    password: Union[str, None] = None,
    fcm_reg_token: Union[str, None] = None,
) -> int | None:
    password = get_password_hash(password)
    async with connection.cursor() as cursor:
        query = "INSERT INTO accounts (username, email, password, fullname, fcm_reg_token) VALUES (%s, %s, %s, %s, %s)"
        args = (username, email, password, fullname, fcm_reg_token)
        await cursor.execute(query, args)
        await connection.commit()
        return cursor.lastrowid


async def fetch_account_db(
    connection: aiomysql.Connection,
    account_id: int | None = None,
    username: str | None = None,
    email: str | None = None,
) -> Dict | None:
    assert (
        account_id is not None or username is not None or email is not None
    ), "fetch_account must be called with either account_id, username or email"
    query = "SELECT * FROM accounts WHERE {filter}=%s".format(
        filter="id" if account_id else "username" if username else "email",
    )
    args = (account_id or username or email or None,)
    print(query)
    print(args)
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query, args)
        return await cursor.fetchone()
