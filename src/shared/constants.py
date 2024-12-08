from enum import Enum
from src import *

true = True
false = False
TRUE = True
FALSE = False
null = None


class Tags(Enum):
    accounts_mgt = "Accounts Management (Sign In, Sign up)"
    organization = "Organization Management"
    project = "Project Management"
    teams = "Team Management"
    feature = "Features Management"
    tasks = "Task Management"


class Mode(Enum):
    LOCAL = 0
    DEV = 1
    PRODUCTION = 2


# mode
mode = Mode.LOCAL
