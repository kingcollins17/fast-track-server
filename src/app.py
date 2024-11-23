from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from src.shared import *

from src.accounts.accounts import accounts

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]


app = FastAPI(
    title="FastTrack App",
    root_path="/api/v1",
    openapi_tags=[
        {
            "name": Tags.accounts_mgt,
            "description": "All accounts creation and managment operations",
        },
    ],
    middleware=middleware,
)

app.include_router(accounts)
