from src.organization import organization
from src.organization.members_db import find_organization_member_db
from src.organization.roles_db import fetch_member_assigned_roles_db
from . import *


@feature.get("/{project_id}")
async def fetch_features(
    project_id: int,
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    account: Annotated[Dict, Depends(get_current_user)],
):
    try:
        data = await fetch_features_db(conn, project_id)
        return ResponseModel(data=data)
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
