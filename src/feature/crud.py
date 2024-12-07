from src.organization import organization
from src.organization.members_db import find_organization_member_db
from src.organization.roles_db import fetch_member_assigned_roles_db
from . import *


@feature.get(
    "/",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": [
                {
                    "project_id": 4,
                    "project_name": "Mobile App",
                    "project_deadline": "2025-12-07T16:18:00",
                    "data": [
                        {
                            "id": 4,
                            "name": "Accounts Managment and Authentication",
                            "description": "User Should be able to Login end to end",
                            "created_at": "2024-12-07T19:12:57",
                            "updated_at": "2024-12-07T19:12:57",
                            "deadline": "2025-11-07T18:11:58",
                            "project_id": 4,
                            "project_name": "Mobile App",
                            "organization_id": 14,
                            "project_deadline": "2025-12-07T16:18:00",
                            "project_created_at": "2024-12-07T17:18:28",
                            "project_updated_at": "2024-12-07T17:18:28",
                        }
                    ],
                },
                {
                    "project_id": 5,
                    "project_name": "Website",
                    "project_deadline": "2024-12-07T18:46:24",
                    "data": [
                        {
                            "id": 5,
                            "name": "Authentication",
                            "description": "Login and Register",
                            "created_at": "2024-12-07T19:47:22",
                            "updated_at": "2024-12-07T19:47:22",
                            "deadline": "2024-12-07T18:46:58",
                            "project_id": 5,
                            "project_name": "Website",
                            "organization_id": 14,
                            "project_deadline": "2024-12-07T18:46:24",
                            "project_created_at": "2024-12-07T19:46:37",
                            "project_updated_at": "2024-12-07T19:46:37",
                        },
                        {
                            "id": 6,
                            "name": "Applications and Inventory",
                            "description": "Login and Register",
                            "created_at": "2024-12-07T19:47:59",
                            "updated_at": "2024-12-07T19:47:59",
                            "deadline": "2024-12-07T18:46:58",
                            "project_id": 5,
                            "project_name": "Website",
                            "organization_id": 14,
                            "project_deadline": "2024-12-07T18:46:24",
                            "project_created_at": "2024-12-07T19:46:37",
                            "project_updated_at": "2024-12-07T19:46:37",
                        },
                    ],
                },
            ],
            "request_at": "2024-12-07T20:15:03.027631",
        },
    ),
)
async def fetch_features(
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    account: Annotated[Dict, Depends(get_current_user)],
    project_id: int | None = None,
    organization_id: int | None = None,
) -> ResponseModel[List[Dict]]:
    try:
        data = await fetch_features_db(
            conn,
            project_id=project_id,
            organization_id=organization_id,
        )
        swaps = {
            "projects.deadline": "project_deadline",
            "projects.created_at": "project_created_at",
            "projects.updated_at": "project_updated_at",
            "projects.id": "project_id",
        }
        data = [swap_keys(value, swaps) for value in data]
        grouped_data = group_list_data(
            data,
            "project_id",
            "project_id",
            "project_name",
            "project_deadline",
        )

        return ResponseModel(data=grouped_data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")


class CreateFeaturePayload(BaseModel):
    name: str
    description: str = ""
    deadline: datetime


@feature.post("/create/{organization_id}/{project_id}")
async def create_new_feature(
    organization_id: int,
    project_id: int,
    data: CreateFeaturePayload,
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    account: Annotated[Dict, Depends(get_current_user)],
) -> ResponseModel:
    try:
        member = await find_organization_member_db(
            conn,
            organization_id,
            account_id=account["id"],
        )
        if member is None:
            raise HTTPException(
                status_code=401, detail="You cannot create features for this project"
            )
        roles = await fetch_member_assigned_roles_db(
            conn,
            member["id"],
            organization_id=organization_id,
        )
        if not role_has_permission(roles, "can_manage_projects"):
            raise HTTPException(
                status_code=401,
                detail="You do not have the required permissions to perform this action",
            )
        feature_id = await create_feature_db(
            conn,
            name=data.name,
            description=data.description,
            deadline=data.deadline,
            project_id=project_id,
        )
        assert feature_id is not None, "feature_id cannot be None"

        return ResponseModel(
            detail=f"New Feature {data.name} added to your Project",
            data={"feature_id": feature_id},
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=404, detail="Please ensure the project is valid"
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")


@feature.delete("/{organization_id}/{feature_id}")
async def delete_feature(
    organization_id: int,
    feature_id: int,
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    account: Annotated[Dict, Depends(get_current_user)],
):
    try:
        member = await find_organization_member_db(
            conn,
            organization_id,
            account_id=account["id"],
        )
        if member is None:
            raise HTTPException(
                status_code=401, detail="You cannot create features for this project"
            )
        roles = await fetch_member_assigned_roles_db(
            conn,
            member["id"],
            organization_id=organization_id,
        )
        if not role_has_permission(roles, "can_manage_projects"):
            raise HTTPException(
                status_code=401,
                detail="You do not have the required permissions to perform this action",
            )
        await delete_feature_db(conn, feature_id)
        return ResponseModel(detail="Feature deleted")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"{type(e)} - {e}")
