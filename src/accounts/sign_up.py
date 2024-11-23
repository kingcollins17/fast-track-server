from . import *

router = APIRouter()


class SignUpPayload(BaseModel):
    email: str
    username: str | None = None
    fullname: str | None = None
    password: str | None = None


@router.post("/sign_up")
async def sign_up(
    data: SignUpPayload,
    conn: Annotated[aiomysql.Connection, Depends(connection)],
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
