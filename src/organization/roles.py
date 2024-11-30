from . import *
from src import organization

router = APIRouter(prefix="/roles", tags=["Organization Roles"])


class OrgRole(BaseModel):
    role: str
    can_manage_teams: bool = False
    can_manage_projects: bool = False
    can_manage_tasks: bool = False
    can_manage_roles: bool = False
    can_send_invites: bool = False


@router.post("/create/{organization_id}")
async def create_organization_role(
    organization_id: int,
    data: OrgRole,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
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
            can_manage_projects=data.can_manage_projects,
            can_manage_tasks=data.can_manage_tasks,
            can_manage_teams=data.can_manage_teams,
            can_manage_roles=data.can_manage_roles,
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


@router.get(
    "/all/{organization_id}",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": [
                {
                    "id": 16,
                    "role": "admin",
                    "can_manage_teams": True,
                    "can_manage_projects": True,
                    "can_manage_tasks": True,
                    "can_manage_roles": True,
                    "can_send_invites": True,
                    "created_at": "2024-11-29T14:50:16",
                    "updated_at": "2024-11-29T14:50:16",
                    "organization_id": 13,
                }
            ],
            "request_at": "2024-11-29T14:51:56.457965",
        },
    ),
)
async def fetch_organizations_roles(
    organization_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel[List[Dict]]:
    try:
        data = await fetch_organization_roles_db(conn, organization_id)
        return ResponseModel(data=data)
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
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
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
        if member is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account is not part of this organization",
            )
        data = await fetch_member_assigned_roles_db(conn, member["id"], organization_id)
        return ResponseModel(data=data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )


@router.post("/assign/{organization_id}")
async def assign_member_role(
    organization_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    member_id: int,
    role_id: int,
):
    """Assign roles to an organization member"""
    try:
        member = await find_organization_member_db(
            conn,
            organization_id=organization_id,
            member_id=member_id,
        )
        if member is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="You cannot assign roles to a non-member of this Organization",
            )
        role = await find_organization_role_db(conn, role_id)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found",
            )
        elif role["organization_id"] != organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This role does not belong to this organization",
            )

        assigner_membership = await find_organization_member_db(
            conn,
            organization_id=organization_id,
            account_id=account["id"],
        )
        if assigner_membership is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not a member of this Organization",
            )
        # the roles of the person assigning roles to the member
        assigner_roles = await fetch_member_assigned_roles_db(
            conn,
            member_id=assigner_membership["id"],
            organization_id=organization_id,
        )
        if not role_has_permission(assigner_roles, "can_assign_roles"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to assign roles in this Organization",
            )
        await assign_member_role_db(conn, member_id, role_id)
        return ResponseModel(detail="Roles assigned successfully")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )
