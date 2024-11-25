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


@router.get(
    "/all/{organization_id}",
    responses=example_response(
        status=200,
        example={
            "id": 8,
            "role": "admin",
            "can_create_issue": True,
            "can_assign_tasks": True,
            "can_review_tasks": True,
            "can_create_feature": True,
            "can_create_teams": True,
            "can_assign_to_teams": True,
            "can_assign_roles": True,
            "can_send_invites": True,
            "created_at": "2024-11-25T12:50:50",
            "updated_at": "2024-11-25T12:50:50",
            "organization_id": 10,
        },
    ),
)
async def fetch_organizations_roles(
    organization_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(connection)],
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
    conn: Annotated[aiomysql.Connection, Depends(connection)],
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
