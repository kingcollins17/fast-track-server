from src.db import *
from . import *


class CreateProjectPayload(BaseModel):
    project_name: str
    deadline: datetime


@project.post(
    "/{organization_id}",
    responses=example_response(
        status=200,
        example={
            "detail": "Created new Project Paybigi Mobile Application",
            "data": {"project_id": 1},
            "request_at": "2024-11-29T13:47:02.575410",
        },
    ),
)
async def create_new_project(
    organization_id: int,
    data: CreateProjectPayload,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel:
    try:
        member = await find_organization_member_db(
            conn,
            organization_id,
            account_id=account["id"],
        )
        if member is None:
            raise HTTPException(
                status_code=400, detail="You are not a member of this Organization"
            )

        roles = await fetch_member_assigned_roles_db(
            conn,
            member_id=member["id"],
            organization_id=organization_id,
        )
        if not role_has_permission(roles, "can_manage_projects"):
            raise HTTPException(
                status_code=401,
                detail="You do not have the neccessary permissions to perform this action",
            )

        project_id = await create_project_db(
            conn,
            project_name=data.project_name,
            deadline=data.deadline,
            organization_id=organization_id,
        )

        assert project_id is not None
        return ResponseModel(
            data={"project_id": project_id},
            detail=f"Created new Project {data.project_name}",
        )

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")


@project.get(
    "/{organization_id}",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": [
                {
                    "id": 2,
                    "project_name": "Paybigi Website",
                    "created_at": "2024-11-29T14:01:24",
                    "updated_at": "2024-11-29T14:01:24",
                    "organization_id": 10,
                    "deadline": "2025-01-29T12:45:19",
                },
                {
                    "id": 1,
                    "project_name": "Paybigi Mobile Application",
                    "created_at": "2024-11-29T13:47:07",
                    "updated_at": "2024-11-29T13:47:07",
                    "organization_id": 10,
                    "deadline": "2025-11-29T12:45:19",
                },
            ],
            "request_at": "2024-11-29T14:06:08.366839",
        },
    ),
)
async def fetch_projects(
    organization_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    page: int = 1,
    per_page: int = 100,
) -> ResponseModel:
    try:
        data = await fetch_projects_db(
            conn,
            organization_id=organization_id,
            limit=per_page,
            offset=page_offset(page, per_page),
        )
        return ResponseModel(data=data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")


@project.get(
    "/details/{project_id}",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": {
                "id": 3,
                "project_name": "Zidepeople Mobile App",
                "deadline": "2025-11-30T12:18:07",
                "created_at": "2024-11-30T13:20:34",
                "updated_at": "2024-11-30T13:20:34",
                "organization_id": 13,
                "organizations.id": 13,
                "organization_name": "Zidepeople",
                "type": "enterprise",
                "member_capacity": 100,
                "max_teams_per_project": 4,
                "owner_id": 6,
                "organizations.created_at": "2024-11-29T14:50:16",
                "organizations.updated_at": "2024-11-29T14:50:16",
                "features": [
                    {
                        "id": 2,
                        "name": "Authentication",
                        "description": "",
                        "created_at": "2024-11-30T15:29:56",
                        "updated_at": "2024-11-30T15:29:56",
                        "deadline": "2024-12-30T14:29:30",
                        "project_id": 3,
                        "projects.id": 3,
                        "project_name": "Zidepeople Mobile App",
                        "projects.deadline": "2025-11-30T12:18:07",
                        "projects.created_at": "2024-11-30T13:20:34",
                        "projects.updated_at": "2024-11-30T13:20:34",
                        "organization_id": 13,
                    },
                    {
                        "id": 3,
                        "name": "Job Application",
                        "description": "A zider should be able to apply to Jobs and book Jobs",
                        "created_at": "2024-11-30T15:31:31",
                        "updated_at": "2024-11-30T15:31:31",
                        "deadline": "2024-12-30T14:29:30",
                        "project_id": 3,
                        "projects.id": 3,
                        "project_name": "Zidepeople Mobile App",
                        "projects.deadline": "2025-11-30T12:18:07",
                        "projects.created_at": "2024-11-30T13:20:34",
                        "projects.updated_at": "2024-11-30T13:20:34",
                        "organization_id": 13,
                    },
                ],
                "teams": [
                    {
                        "id": 1,
                        "team_name": "POD 1",
                        "created_at": "2024-11-30T14:15:19",
                        "updated_at": "2024-11-30T14:15:19",
                        "project_id": 3,
                        "projects.id": 3,
                        "project_name": "Zidepeople Mobile App",
                        "deadline": "2025-11-30T12:18:07",
                        "projects.created_at": "2024-11-30T13:20:34",
                        "projects.updated_at": "2024-11-30T13:20:34",
                        "organization_id": 13,
                        "organizations.id": 13,
                        "organization_name": "Zidepeople",
                        "type": "enterprise",
                        "member_capacity": 100,
                        "max_teams_per_project": 4,
                        "owner_id": 6,
                        "organizations.created_at": "2024-11-29T14:50:16",
                        "organizations.updated_at": "2024-11-29T14:50:16",
                    },
                    {
                        "id": 2,
                        "team_name": "POD 4",
                        "created_at": "2024-11-30T14:18:00",
                        "updated_at": "2024-11-30T14:18:00",
                        "project_id": 3,
                        "projects.id": 3,
                        "project_name": "Zidepeople Mobile App",
                        "deadline": "2025-11-30T12:18:07",
                        "projects.created_at": "2024-11-30T13:20:34",
                        "projects.updated_at": "2024-11-30T13:20:34",
                        "organization_id": 13,
                        "organizations.id": 13,
                        "organization_name": "Zidepeople",
                        "type": "enterprise",
                        "member_capacity": 100,
                        "max_teams_per_project": 4,
                        "owner_id": 6,
                        "organizations.created_at": "2024-11-29T14:50:16",
                        "organizations.updated_at": "2024-11-29T14:50:16",
                    },
                ],
            },
            "request_at": "2024-11-30T15:30:48.096197",
        },
    ),
)
async def fetch_project_details(
    project_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
):
    try:
        project = await fetch_project_details_db(conn, project_id)
        if project is not None:
            project["features"] = await fetch_features_db(conn, project_id)
            project["teams"] = await fetch_teams_db(conn, project_id=project_id)

        return ResponseModel(data=project)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")


class UpdateProjectPayload(BaseModel):
    project_name: str | None = None
    deadline: datetime | None = None


@project.put("/{organization_id}")
async def update_project(
    organization_id: int,
    project_id: int,
    data: UpdateProjectPayload,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel:
    try:
        member = await find_organization_member_db(
            conn,
            organization_id=organization_id,
            account_id=account["id"],
        )
        if member is None:
            raise HTTPException(
                status_code=400,
                detail="You are not a member of this Organization",
            )

        roles = await fetch_member_assigned_roles_db(
            conn,
            member["id"],
            organization_id=organization_id,
        )
        if not role_has_permission(roles, "can_manage_projects"):
            raise HTTPException(
                status_code=401,
                detail="You are not authorized to update a Project in this Organization",
            )

        res = await update_project_db(
            conn,
            organization_id=organization_id,
            project_name=data.project_name,
            deadline=data.deadline,
            project_id=project_id,
        )
        return ResponseModel(
            detail="Project updated successfully", data={"project_id": res}
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")


@project.delete("/{organization_id}")
async def delete_project(
    organization_id: int,
    project_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel:
    try:
        await delete_project_db(conn, project_id)
        return ResponseModel(detail="Project deleted")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")
