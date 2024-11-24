from . import org
from .crud import router as crud_router
from .roles import router as roles_router
from .members import router as member_router

org.include_router(crud_router)
org.include_router(roles_router)
org.include_router(member_router)
