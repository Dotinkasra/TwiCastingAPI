from dataclasses import dataclass
from twicas.models.user import User

@dataclass
class Movie():
    id: str
    user_id: str
    title: str
    subtitle: str | None
    last_owner_comment: str | None
    category: str | None
    link: str
    is_live: bool
    is_recorded: bool
    comment_count: int
    large_thumbnail: str
    small_thumbnail: str
    country: str
    duration: int
    created: int
    is_collabo: bool
    is_protected: bool
    max_view_count: int
    current_view_count: int
    total_view_count: int
    hls_url: str | None
    broadcaster: User | None
    tags: list[str] | None
