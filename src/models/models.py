from typing import List, Dict, Any, Tuple, Generic, TypeVar
import pydantic
from datetime import datetime

T = TypeVar("T")


class ResponseModel(pydantic.BaseModel, Generic[T]):
    detail: str = "Request successful"
    data: T | None = None
    request_at: datetime = datetime.now()


class Account(pydantic.BaseModel):
    id: int
    username: str
    email: str


class Organization(pydantic.BaseModel):
    id: int
    name: str
    member_capacity: int = 100
    total_no_of_members: int


class IssueTask(pydantic.BaseModel):
    id: int
    task_name: str
    assignee_id: int


class ProjectFeatureIssue(pydantic.BaseModel):
    id: int
    tasks: List[IssueTask]
    max_no_of_tasks: int
    progress: float


class ProjectFeature(pydantic.BaseModel):
    id: int
    feature: str
    description: str
    no_of_issues: int
    max_no_of_isssues: int
    progress: float


class Project(pydantic.BaseModel):
    id: int
    name: str
    features: List[ProjectFeature]
