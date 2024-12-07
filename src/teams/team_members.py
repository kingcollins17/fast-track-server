from . import *


@teams.get(
    "/all-members/{organization_id}",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": [
                {
                    "team_name": "POD 1",
                    "team_id": 5,
                    "organization_name": "Zidepeople",
                    "data": [
                        {
                            "account_id": 9,
                            "username": "jondoe",
                            "fullname": "Jon Doe",
                            "email": "jondoe@gmail.com",
                            "team_id": 5,
                            "team_name": "POD 1",
                            "organization_name": "Zidepeople",
                        },
                        {
                            "account_id": 10,
                            "username": "janedoe",
                            "fullname": "Jane Doe",
                            "email": "janedoe@gmail.com",
                            "team_id": 5,
                            "team_name": "POD 1",
                            "organization_name": "Zidepeople",
                        },
                    ],
                },
                {
                    "team_name": "POD 4",
                    "team_id": 6,
                    "organization_name": "Zidepeople",
                    "data": [
                        {
                            "account_id": 9,
                            "username": "jondoe",
                            "fullname": "Jon Doe",
                            "email": "jondoe@gmail.com",
                            "team_id": 6,
                            "team_name": "POD 4",
                            "organization_name": "Zidepeople",
                        },
                        {
                            "account_id": 10,
                            "username": "janedoe",
                            "fullname": "Jane Doe",
                            "email": "janedoe@gmail.com",
                            "team_id": 6,
                            "team_name": "POD 4",
                            "organization_name": "Zidepeople",
                        },
                    ],
                },
            ],
            "request_at": "2024-12-07T19:27:36.118022",
        },
    ),
)
async def fetch_all_organizations_team_members(
    organization_id: int,
    conn: Annotated[aiomysql.Connection, Depends(connection)],
    account: Annotated[Dict, Depends(get_current_user)],
    page: int = 1,
    per_page: int = 200,
):
    try:
        data = await fetch_team_members_db(
            conn,
            organization_id=organization_id,
        )
        return ResponseModel(
            data=group_list_data(
                data,
                "team_id",  # the grouping key
                "team_name",  # additional label keys
                "team_id",
                "organization_name",
            )
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )


@teams.get("/members/{team_id}")
async def fetch_team_members(
    team_id: int,
    conn: Annotated[aiomysql.Connection, Depends(connection)],
    account: Annotated[Dict, Depends(get_current_user)],
    page: int = 1,
    per_page: int = 200,
) -> ResponseModel:
    try:
        data = await fetch_team_members_db(
            conn,
            team_id=team_id,
            limit=per_page,
            offset=page_offset(page, per_page),
        )
        return ResponseModel(data=data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )


@teams.post("/assign/{organization_id}/{team_id}")
async def assign_team_member(
    organization_id: int,
    team_id: int,
    member_id: Annotated[
        int, Query(description="The account_id of the user you wish to add to a Team")
    ],
    conn: Annotated[aiomysql.Connection, Depends(connection)],
    account: Annotated[Dict, Depends(get_current_user)],
) -> ResponseModel:
    try:
        member = await find_organization_member_db(conn, organization_id, account["id"])
        if member is None:
            raise HTTPException(
                status_code=401,
                detail="You are not allowed to assign team members in this Organization",
            )
        team_member = await find_organization_member_db(
            conn, organization_id, account_id=member_id
        )
        if team_member is None:
            raise HTTPException(
                status_code=401,
                detail="The person you wish to assign is not part of this Organization",
            )
        roles = await fetch_member_assigned_roles_db(
            conn, member["id"], organization_id=organization_id
        )
        if not role_has_permission(roles, "can_manage_teams"):
            raise HTTPException(
                status_code=401,
                detail="You do not have the required permissions for this action",
            )
        res = await create_team_member_db(conn, member_id, team_id)
        return ResponseModel(
            detail="Member assigned to team", data={"team_member_id": res}
        )
    except IntegrityError:
        raise HTTPException(
            status_code=404,
            detail="Either Team does not exist or This account is already part of this Team",
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )


@teams.delete("/delete/{organization_id}/{team_member_id}")
async def kick_from_team(
    organization_id: int,
    team_member_id: int,
    conn: Annotated[aiomysql.Connection, Depends(connection)],
    account: Annotated[Dict, Depends(get_current_user)],
):
    try:
        member = await find_organization_member_db(conn, organization_id, account["id"])
        if member is None:
            raise HTTPException(
                status_code=401,
                detail="You are not allowed to remove team members in this Organization",
            )
        roles = await fetch_member_assigned_roles_db(
            conn, member["id"], organization_id=organization_id
        )
        if not role_has_permission(roles, "can_manage_teams"):
            raise HTTPException(
                status_code=401,
                detail="You do not have the required permissions for this action",
            )
        await delete_team_member_db(conn, team_member_id)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )
