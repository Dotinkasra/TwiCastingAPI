# Unofficial TwiCasting API

## Usage
```bash
$ pip install git+https://github.com/Dotinkasra/TwiCastingAPI
```

```python
from twicas import TwiCastingAPI, TwiCastingUserInfo, TwiCastingMovieInfo

tc = TwiCastingAPI(
    "Your ClientID",
    "Your ClientSecret",
    "Your Callback URL"
)
```

## Class
```python
class TwiCastingAPI(
    client_id: str,
    client_secret: str,
    redirect_uri: str
)
```

```python
@dataclass
class TwiCastingUserInfo():
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
```

```python
@dataclass
class TwiCastingMovieInfo():
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
    broadcaster: TwiCastingUserInfo
    tags: list[str]
```

## Methods
```python
def get_user_info(self, user_id: str) -> TwiCastingUserInfo
```

```python
def get_movie_info(self, movie_id: str) -> TwiCastingMovieInfo
```
