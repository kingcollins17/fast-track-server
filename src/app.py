from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from src.shared import *

from src.accounts.accounts import accounts
from src.organization.organization import org
from src.project.project import project
from src.teams.teams import teams
from src.feature.feature import feature

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
        {
            "name": Tags.organization,
            "description": "Organization Management Endpoints",
        },
        {
            "name": Tags.project,
            "description": "Projects Mangement endpoints",
        },
        {
            "name": Tags.teams,
            "description": "Team Management Endpoints",
        },
    ],
    middleware=middleware,
)

app.include_router(accounts)
app.include_router(org)
app.include_router(project)
app.include_router(teams)
app.include_router(feature)
