from fastapi import Response
from . import *


@tasks.get(
    "",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": [
                {
                    "id": 6,
                    "name": "Sign In Endpoints",
                    "description": null,
                    "status": "pending",
                    "requirements": {"PR": "link", "challenges": "text"},
                    "deadline": "2025-12-08T16:53:25",
                    "completed_at": null,
                    "created_at": "2024-12-08T18:14:34",
                    "updated_at": "2024-12-08T18:14:34",
                    "feature_id": 4,
                    "parent_task_id": 3,
                    "assigned_team_id": null,
                    "assigned_account_id": 9,
                    "parent_task_name": "Sign-in and Sign-up",
                    "feature_name": "Accounts Managment and Authentication",
                    "project_id": 4,
                    "project_name": "Mobile App",
                },
                {
                    "id": 4,
                    "name": "Sign In UI Implementation",
                    "description": null,
                    "status": "pending",
                    "requirements": {},
                    "deadline": "2025-12-08T16:53:25",
                    "completed_at": null,
                    "created_at": "2024-12-08T17:56:32",
                    "updated_at": "2024-12-08T17:56:32",
                    "feature_id": 4,
                    "parent_task_id": 3,
                    "assigned_team_id": null,
                    "assigned_account_id": 10,
                    "parent_task_name": "Sign-in and Sign-up",
                    "feature_name": "Accounts Managment and Authentication",
                    "project_id": 4,
                    "project_name": "Mobile App",
                },
                {
                    "id": 3,
                    "name": "Sign-in and Sign-up",
                    "description": null,
                    "status": "pending",
                    "requirements": {},
                    "deadline": "2025-10-08T16:41:33",
                    "completed_at": null,
                    "created_at": "2024-12-08T17:48:42",
                    "updated_at": "2024-12-08T17:48:42",
                    "feature_id": 4,
                    "parent_task_id": null,
                    "assigned_team_id": 5,
                    "assigned_account_id": null,
                    "parent_task_name": null,
                    "feature_name": "Accounts Managment and Authentication",
                    "project_id": 4,
                    "project_name": "Mobile App",
                },
            ],
            "request_at": "2024-12-08T18:17:13.587034",
        },
    ),
)
async def fetch_tasks(
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    organization_id: int | None = None,
    feature_id: int | None = None,
    project_id: int | None = None,
    page: int = 1,
    per_page: int = 200,
) -> ResponseModel:
    try:
        data = await fetch_tasks_db(
            conn,
            organization_id=organization_id,
            project_id=project_id,
            feature_id=feature_id,
            limit=per_page,
            offset=page_offset(page, per_page),
        )

        return ResponseModel(data=data)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")


class AssignTaskPayload(BaseModel):
    name: str
    deadline: datetime
    description: str | None = None
    feature_id: int
    parent_task_id: int | None = None
    assigned_team_id: int | None = None
    assigned_account_id: int | None = None
    requirements: Dict[str, Literal["link", "photo", "text"]] = {}


@tasks.post("/{organization_id}")
async def assign_task(
    organization_id: int,
    data: AssignTaskPayload,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel[Dict[str, int]]:
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
        if not role_has_permission(roles, "can_manage_tasks"):
            raise HTTPException(
                status_code=401,
                detail="You do not have the neccessary permissions to perform this action",
            )
        task_id = await create_task_db(
            conn,
            name=data.name,
            description=data.description,
            deadline=data.deadline,
            feature_id=data.feature_id,
            parent_task_id=data.parent_task_id,
            team_id=data.assigned_team_id,
            account_id=data.assigned_account_id,
            **data.requirements,
        )
        assert task_id is not None
        return ResponseModel(detail="Task assigned", data={"task_id": task_id})
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail=f"Assignee Team or Account does not exist"
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")


@tasks.delete("/{organization_id}/{task_id}")
async def delete_task(
    organization_id: int,
    task_id: int,
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
        if not role_has_permission(roles, "can_manage_tasks"):
            raise HTTPException(
                status_code=401,
                detail="You do not have the neccessary permissions to perform this action",
            )
        await delete_task_db(conn, task_id)
        return ResponseModel(detail="Task deleted")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")
