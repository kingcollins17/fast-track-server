from . import *
from src import organization

router = APIRouter(prefix="/roles", tags=["Organization Roles"])


class OrgRole(BaseModel):
    role: str
    can_assign_tasks: bool = False
    can_review_tasks: bool = False
    can_create_issue: bool = False
    can_create_feature: bool = False
    can_create_teams: bool = False
    can_assign_to_teams: bool = False
    can_assign_roles: bool = False
    can_send_invites: bool = False


@router.post("/create/{organization_id}")
async def create_organization_role(
    organization_id: int,
    data: OrgRole,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(connection)],
):
    try:
        organization = await find_organization_db(conn, organization_id)
        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="We do not have any record of this Organization",
            )
        if organization["owner_id"] != account["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sorry, only owners of this organization can create roles",
            )

        await create_organization_role_db(
            conn,
            organization_id,
            role_name=data.role,
            can_assign_tasks=data.can_assign_tasks,
            can_assign_roles=data.can_assign_roles,
            can_create_feature=data.can_create_issue,
            can_create_issue=data.can_create_issue,
            can_review_tasks=data.can_review_tasks,
            can_create_teams=data.can_create_teams,
            can_assign_to_teams=data.can_assign_to_teams,
            can_send_invites=data.can_send_invites,
        )
        return ResponseModel(
            detail=f"You have added role {data.role} to your organization",
        )

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


@router.get("/all/{organization_id}")
async def fetch_organizations_roles(
    organization_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(connection)],
) -> ResponseModel[List[OrgRole]]:
    try:
        data = await fetch_organization_roles_db(conn, organization_id)
        return ResponseModel(data=[OrgRole(**value) for value in data])
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


@router.get("/assigned/{organization_id}")
async def fetch_assigned_roles(
    organization_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(connection)],
    member_id: int | None = None,
):
    """Your roles in this organization
    If member id is passed, it returns the roles of the member_id otherwise it returns
    the roles assigned to this authorized user
    """

    try:
        member = await find_organization_member_db(
            conn,
            organization_id=organization_id,
            account_id=account["id"],
            member_id=member_id,
        )
        print(member)
        if member is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account is not part of this organization",
            )
        data = await fetch_member_assigned_roles_db(conn, member["id"])
        return ResponseModel(data=data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )
