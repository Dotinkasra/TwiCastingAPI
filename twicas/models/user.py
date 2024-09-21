from dataclasses import dataclass

@dataclass
class User():
    id: str
    screen_id: str
    name: str
    image: str
    profile: str
    level: int
    last_movie_id: str|None
    is_live: bool
    supporter_count: int
    supporting_count: int
    created: int
