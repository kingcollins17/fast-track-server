from enum import Enum
from src import *


class Tags(Enum):
    accounts_mgt = "Accounts & Management"
    organization = "Organization Management"
    project = "General Project Management Features"
    teams = "Team Management"


class Mode(Enum):
    LOCAL = 0
    DEV = 1
    PRODUCTION = 2


# mode
mode = Mode.LOCAL
