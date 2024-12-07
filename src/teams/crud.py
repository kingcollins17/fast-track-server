from . import *


@teams.get(
    "/{organization_id}",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": [
                {
                    "id": 5,
                    "team_name": "POD 1",
                    "created_at": "2024-12-07T17:19:16",
                    "updated_at": "2024-12-07T17:19:16",
                    "organization_id": 14,
                }
            ],
            "request_at": "2024-12-07T17:19:58.275200",
        },
    ),
)
async def fetch_teams(
    organization_id: int,
    conn: Annotated[aiomysql.Connection, Depends(connection)],
    account: Annotated[Dict, Depends(get_current_user)],
):
    try:
        data = await fetch_teams_db(conn, organization_id=organization_id)
        return ResponseModel(data=data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )


@teams.post("/create/{organization_id}/{project_id}")
async def create_team(
    organization_id: int,
    name: str,
    conn: Annotated[aiomysql.Connection, Depends(connection)],
    account: Annotated[Dict, Depends(get_current_user)],
):
    try:
        member = await find_organization_member_db(conn, organization_id, account["id"])
        if member is None:
            raise HTTPException(
                status_code=401,
                detail="You are not allowed to create teams in this Organization",
            )
        roles = await fetch_member_assigned_roles_db(
            conn, member["id"], organization_id=organization_id
        )
        if not role_has_permission(roles, "can_manage_teams"):
            raise HTTPException(
                status_code=401,
                detail="You do not have the required permissions for this action",
            )
        team_id = await create_team_db(conn, name, organization_id)
        return ResponseModel(detail="Created new Team", data={"team_id": team_id})
    except IntegrityError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Please ensure you are creating this team for a valid project",
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )


@teams.delete("/delete/{organization_id}")
async def delete_team(
    organization_id: int,
    team_id: int,
    conn: Annotated[aiomysql.Connection, Depends(connection)],
    account: Annotated[Dict, Depends(get_current_user)],
) -> ResponseModel:
    try:
        member = await find_organization_member_db(conn, organization_id, account["id"])
        if member is None:
            raise HTTPException(
                status_code=401,
                detail="You are not allowed to delete teams in this Organization",
            )
        roles = await fetch_member_assigned_roles_db(
            conn, member["id"], organization_id=organization_id
        )
        if not role_has_permission(roles, "can_manage_teams"):
            raise HTTPException(
                status_code=401,
                detail="You do not have the required permissions for this action",
            )
        await delete_team_db(conn, team_id)
        return ResponseModel(detail="Team deleted")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )
