from dataclasses import dataclass
from twicas.models.user import User

@dataclass
class Comment():
    id: str
    message: str
    from_user: User
    created: int
