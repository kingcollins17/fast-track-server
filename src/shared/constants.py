from enum import Enum
from src import *

true = True
false = False
TRUE = True
FALSE = False
null = None


class Tags(Enum):
    accounts_mgt = "Accounts & Management"
    organization = "Organization Management"
    project = "General Project Management Features"
    teams = "Team Management"
    feature = "Project Features"
    tasks = "Task Management"


class Mode(Enum):
    LOCAL = 0
    DEV = 1
    PRODUCTION = 2


# mode
mode = Mode.LOCAL
