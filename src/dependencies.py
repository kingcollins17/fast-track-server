import aiomysql
from typing import Annotated, List, Any, Dict
from fastapi import Depends
from . import *


async def db_connection() -> aiomysql.Connection:
    return await aiomysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
    )
