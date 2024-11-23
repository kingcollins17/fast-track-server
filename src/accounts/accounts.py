from . import *
from .sign_in import router as sign_in_router
from .sign_up import router as sign_up_router

accounts.include_router(sign_in_router)
accounts.include_router(sign_up_router)
