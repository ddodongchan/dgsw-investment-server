from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    REPORTER = "REPORTER"

class UserStatus(str, Enum):
    ACTIVATE = "ACTIVATE"
    DEACTIVATE = "DEACTIVATE"