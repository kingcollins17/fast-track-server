from enum import Enum
from src import *


class Tags(Enum):
    accounts_mgt = "Accounts & Management"


class Mode(Enum):
    LOCAL = 0
    DEV = 1
    PRODUCTION = 2


# mode
mode = Mode.LOCAL
