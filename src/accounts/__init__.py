from typing import List, Annotated, Any, Dict
from fastapi import APIRouter, Depends, Query, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from src.models import *
from src.shared import *
from .db import *

accounts = APIRouter(prefix="/accounts", tags=[Tags.accounts_mgt])
