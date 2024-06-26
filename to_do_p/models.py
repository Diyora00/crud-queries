from enum import Enum
from typing import Optional


class UserRole(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    SUPERADMIN = 'SUPERADMIN'


class UserStatus(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    BLOCKED = 'BLOCKED'


class TodoType(Enum):
    Optional = 'optional'
    Personal = 'personal'
    Shopping = 'shopping'


class User:
    def __init__(self,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 user_id: Optional[int] = None,
                 role: Optional[UserRole] = None,
                 status: Optional[UserStatus] = None,
                 login_try_count: Optional[int] = None
                 ):
        self.username = username
        self.password = password
        self.id = user_id
        self.role = role or UserRole.USER.value
        self.status = status or UserStatus.INACTIVE.value
        self.login_try_count = login_try_count or 0

    def assign(self, li: tuple):
        self.id = li[0]
        self.username = li[1]
        self.password = li[2]
        self.role = li[3]
        self.status = li[4]
        self.login_try_count = li[5]

    def __str__(self):
        return f'{self.role} => {self.username}'


class Todo:
    def __init__(self,
                 title: str,
                 user_id: int,
                 todo_type: Optional[TodoType] = None,
                 ):
        self.title = title
        self.user_id = user_id
        self.todo_type = todo_type or TodoType.Optional.value