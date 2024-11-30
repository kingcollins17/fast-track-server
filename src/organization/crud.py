from fastapi import Response

from src.db import *
from src.dependencies import *
from . import *

router = APIRouter()


@router.get(
    "/me",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": [
                {
                    "id": 1,
                    "organization_name": "KodeHauz",
                    "type": "standard",
                    "member_capacity": 100,
                    "max_teams_per_project": 4,
                    "owner_id": 1,
                    "created_at": "2024-11-24T10:01:18",
                    "updated_at": "2024-11-24T10:01:18",
                },
                {
                    "id": 2,
                    "organization_name": "Zidepeople",
                    "type": "standard",
                    "member_capacity": 100,
                    "max_teams_per_project": 4,
                    "owner_id": 1,
                    "created_at": "2024-11-24T10:03:31",
                    "updated_at": "2024-11-24T10:03:31",
                },
            ],
            "request_at": "2024-11-24T10:16:52.110649",
        },
    ),
)
async def fetch_created_organizations(
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    page: int = 1,
    per_page: int = 100,
) -> ResponseModel[List[Dict]]:
    """Fetch the list of organizations created by caller"""
    try:
        data = await fetch_created_organizations_db(
            conn,
            account_id=account["id"],
            limit=per_page,
            offset=page_offset(page, per_page),
        )
        return ResponseModel(data=data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


@router.get(
    "/part",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": [
                {
                    "member_id": 7,
                    "id": 9,
                    "organization_name": "Snapnet",
                    "type": "standard",
                    "member_capacity": 100,
                    "max_teams_per_project": 4,
                    "owner_id": 1,
                    "created_at": "2024-11-24T14:09:12",
                    "updated_at": "2024-11-24T14:09:12",
                }
            ],
            "request_at": "2024-11-24T17:28:07.008082",
        },
    ),
)
async def fetch_member_organizations(
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    page: int = 1,
    per_page: int = 100,
):
    """Fetch the list of organizations this caller is part of"""
    try:
        data = await fetch_member_organizations_db(
            conn,
            account_id=account["id"],
            limit=per_page,
            offset=page_offset(page, per_page),
        )
        return ResponseModel(data=data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


@router.get(
    "/details/{organization_id}",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": {
                "id": 13,
                "organization_name": "Zidepeople",
                "type": "enterprise",
                "member_capacity": 100,
                "max_teams_per_project": 4,
                "owner_id": 6,
                "created_at": "2024-11-29T14:50:16",
                "updated_at": "2024-11-29T14:50:16",
                "projects": [
                    {
                        "id": 3,
                        "project_name": "Zidepeople Mobile App",
                        "deadline": "2025-11-30T12:18:07",
                        "created_at": "2024-11-30T13:20:34",
                        "updated_at": "2024-11-30T13:20:34",
                        "organization_id": 13,
                    }
                ],
                "members": [
                    {
                        "member_id": 13,
                        "id": 6,
                        "username": "techie99",
                        "email": "techie99@gmail.com",
                        "fullname": "Collins Nnanna",
                        "active": true,
                        "email_verified": true,
                        "fcm_reg_token": null,
                        "created_at": "2024-11-29T14:49:51",
                        "updated_at": "2024-11-29T14:49:51",
                    }
                ],
                "roles": [
                    {
                        "id": 16,
                        "role": "admin",
                        "can_manage_teams": true,
                        "can_manage_projects": true,
                        "can_manage_tasks": true,
                        "can_manage_roles": true,
                        "can_send_invites": true,
                        "created_at": "2024-11-29T14:50:16",
                        "updated_at": "2024-11-29T14:50:16",
                        "organization_id": 13,
                    },
                    {
                        "id": 17,
                        "role": "Intern",
                        "can_manage_teams": false,
                        "can_manage_projects": false,
                        "can_manage_tasks": false,
                        "can_manage_roles": false,
                        "can_send_invites": false,
                        "created_at": "2024-11-29T14:55:18",
                        "updated_at": "2024-11-29T14:55:18",
                        "organization_id": 13,
                    },
                ],
                "teams": [],
            },
            "request_at": "2024-11-30T13:33:58.967507",
        },
    ),
)
async def fetch_organization_details(
    organization_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel:
    """Fetch the details of an organization, including the members and projects"""
    try:
        org = await find_organization_db(conn, organization_id)
        if org is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization does not exist",
            )
        projects = await fetch_projects_db(conn, organization_id)
        org["projects"] = projects

        members = await fetch_organization_members_db(conn, organization_id)
        org["members"] = members
        org["roles"] = await fetch_organization_roles_db(conn, organization_id)
        org["teams"] = []
        return ResponseModel(data=org)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


@router.post(
    "/create",
    responses=example_response(
        status=200,
        example={
            "detail": "You have created a new organization Zidepeople",
            "data": {"organization_id": 13},
            "request_at": "2024-11-29T14:43:44.921923",
        },
    ),
)
async def create_organization(
    name: str,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    type: Literal["default", "standard", "enterprise"] = "standard",
) -> ResponseModel:
    """Create a new organization"""
    try:
        org_id = await create_organization_db(
            conn,
            account["id"],
            name=name,
            org_type=type,
        )
        assert org_id is not None
        return ResponseModel(
            detail=f"You have created a new organization {name}",
            data={"organization_id": org_id},
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


@router.patch("/update/{id}")
async def update_organization_name(
    id: int,
    name: str,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel:
    try:
        await update_organization_db(conn, id, account["id"], name)
        return ResponseModel()
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


@router.delete("/delete/{id}")
async def delete_organization(
    id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel:
    try:
        await delete_organization_db(conn, account["id"], id)
        return ResponseModel(detail="Organization deleted")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )
