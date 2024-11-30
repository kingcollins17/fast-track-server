from . import *

router = APIRouter()


class SignInPayload(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str | None = None
    google_id: str | None = None


@router.post("/sign-in")
async def sign_in(
    data: SignInPayload,
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> ResponseModel[Token]:
    try:
        username = None
        email = None
        if data.username is not None:
            username = data.username.strip()
        if data.email is not None:
            email = data.email.strip()
        account = await fetch_account(conn, username=username, email=email)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not account["active"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is not active",
            )
        if not account["email_verified"]:
            raise HTTPException(
                status_code=status.HTTP_206_PARTIAL_CONTENT,
                detail="Enter the otp sent to your email address",
            )
        if data.google_id is not None:
            pass
        if not verify_password(data.password or "", account["password"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect Password",
            )
        access_token = create_access_token(
            data={
                "id": account["id"],
                "username": account["username"],
                "email": account["email"],
            }
        )
        return ResponseModel(
            data=Token(access_token=access_token, token_type="bearer"),
            detail="Sign in successful",
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


@router.post("/oauth-token")
async def authorize_swagger(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    conn: Annotated[aiomysql.Connection, Depends(db_connection)],
) -> Token:
    account = await fetch_account(conn, username=form_data.username.strip())
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not account["active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="This account is not active"
        )
    if not account["email_verified"]:
        raise HTTPException(
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            detail="Enter the otp sent to your email address",
        )
    if not verify_password(form_data.password, account["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Password",
        )
    access_token = create_access_token(
        data={
            "id": account["id"],
            "username": account["username"],
            "email": account["email"],
        }
    )
    return Token(access_token=access_token, token_type="bearer")
