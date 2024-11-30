from typing import List, Annotated, Any, Dict, Literal
from fastapi import APIRouter, Depends, Query, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from pymysql.err import IntegrityError, DataError
from src.models import *
from src.shared import *
from src.dependencies import *
from .db import *


project = APIRouter(prefix="/project", tags=[Tags.project])
