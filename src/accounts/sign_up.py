from . import *

router = APIRouter()


class SignUpPayload(BaseModel):
    email: str
    username: str | None = None
    fullname: str
    password: str | None = None


@router.post("/sign-up")
async def sign_up(
    data: SignUpPayload,
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel:
    try:
        await create_account_db(
            conn,
            username=data.username or data.email.split("@")[0].strip(),
            email=data.email.strip(),
            password=data.password,
            fullname=data.fullname,
        )
        return ResponseModel(detail="Please check your email for an otp")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


@router.get("/user-account")
async def fetch_account(
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
    account: Annotated[Dict, Depends(get_current_user)],
):
    try:
        data = await fetch_account_db(
            conn,
            account_id=account["id"],
        )
        if data is None:
            raise HTTPException(status_code=404, detail="Account not found")
        data["active"] = bool(data["active"])
        data.pop("email_verified")
        data.pop("fcm_reg_token")
        data.pop("password")
        return ResponseModel(data=data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )
