from pydantic import EmailStr
from pydantic_core import Url

from src.dependencies import *
from . import *
from src.db import *

router = APIRouter(prefix="/members", tags=["Organization Members Management"])


class InviteResponse(BaseModel):
    invite_link: Url
    invite_type: Literal["public", "private"]
    invitee_email: EmailStr | None = None


def build_invite(host_id: int, invitee_id, as_a):
    return f"{host_id} is inviting {invitee_id} as a {as_a}"


@router.get("/invite")
async def send_organization_invite(
    organization_id: int,
    role_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    invitee_email: Union[EmailStr, None] = None,
) -> ResponseModel[InviteResponse]:
    """The generated invite link may be public or private, if invitee is specified, then it is private
    If not, it is public, if the link is private, then a key is added as a query parameter whose value will be a hash
    to be submitted during invite acceptance by the intended invitee
    """
    try:
        role = await find_organization_role_db(conn, role_id)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found",
            )
        link = "https://fasttrack_web.onrender.com/#/organization/invite"
        params = {}
        if invitee_email is not None:
            assert (
                invitee_email != account["email"]
            ), "You cannot invite yourself to your own organization"
            params["invite_type"] = "private"
            params["invitee_email"] = invitee_email
            key = hash_string(
                build_invite(organization_id, invitee_email, as_a=role_id)
            )
            params["key"] = key

        # start appending query parameters
        else:
            params["invite_type"] = "public"
            key = hash_string(build_invite(organization_id, "any", as_a=role_id))
            params["key"] = key

        params["organization_id"] = organization_id
        params["role_id"] = role_id
        link += "?"
        # append all query params from dictionary
        for k, value in params.items():
            link += f"{k}={value}&"
        return ResponseModel(
            detail="Invite created",
            data=InviteResponse(
                invite_link=Url(link.removesuffix("&")),
                **params,
            ),
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


class AcceptInvitePayload(BaseModel):
    invite_link: Url


@router.post("/accept-invite")
async def accept_organization_invite(
    data: AcceptInvitePayload,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
):
    try:
        params = query_params(str(data.invite_link))
        print(params)
        print(params)
        # print()
        org_id = int(params["organization_id"])
        role_id = int(params["role_id"])
        if not verify_hash(
            build_invite(
                org_id,
                account["email"] if params["invite_type"] == "private" else "any",
                as_a=role_id,
            ),
            params["key"],
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your invite key is invalid",
            )

        member_id = await create_organization_member_db(conn, org_id, account["id"])
        assert member_id is not None, "Member id cannot be None"
        await assign_member_role_db(conn, member_id, role_id)
        return ResponseModel(detail="You are now a member of this organization")
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You are already a member"
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(e)} - {e}",
        )


@router.get(
    "/{organization_id}",
    responses=example_response(
        status=200,
        example={
            "detail": "Request successful",
            "data": [
                {
                    "member_id": 3,
                    "id": 1,
                    "username": "dev99",
                    "email": "dev99@gmail.com",
                    "fullname": None,
                    "active": True,
                    "email_verified": True,
                    "fcm_reg_token": None,
                    "created_at": "2024-11-22T17:11:06",
                    "updated_at": "2024-11-22T17:11:06",
                }
            ],
            "request_at": "2024-11-24T14:23:09.697695",
        },
    ),
)
async def fetch_organization_members(
    organization_id: int,
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    page: int = 1,
    per_page: int = 100,
) -> ResponseModel[List[Dict]]:
    try:
        data = await fetch_organization_members_db(
            conn, organization_id, limit=per_page, offset=page_offset(page, per_page)
        )
        return ResponseModel(data=data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


@router.delete("/remove/{organization_id}/{member_id}")
async def remove_organization_member(
    organization_id: int,
    member_id: int,  # member to kick out
    account: Annotated[Dict, Depends(get_current_user)],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel:
    """Admins and Organization owners can use this kick a member, use with caution"""
    member = await find_organization_member_db(
        conn,
        organization_id,
        account_id=account["id"],
    )
    removing_member = await find_organization_member_db(
        conn,
        organization_id,
        member_id=member_id,
    )
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not part of this Organization",
        )
    if removing_member is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The person you want to remove is not part of this organization",
        )
    roles = await fetch_member_assigned_roles_db(
        conn,
        member["id"],
        organization_id=organization_id,
    )
    if not role_has_permission(roles, "can_manage_teams"):
        raise HTTPException(
            status_code=401,
            detail="You are authorized to remove someone from this Organization",
        )

    await delete_organization_member_db(conn, organization_id, member_id=member["id"])
    return ResponseModel(detail="Member removed")
