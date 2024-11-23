from fastapi import FastAPI
from src.shared import *
from src.accounts.accounts import accounts

app = FastAPI(
    title="FastTrack App",
    root_path="/api/v1",
    openapi_tags=[
        {
            "name": Tags.accounts_mgt,
            "description": "All accounts creation and managment operations",
        },
    ],
)

app.include_router(accounts)
