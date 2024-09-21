# Unofficial TwiCasting API

## Usage
```bash
$ pip install git+https://github.com/Dotinkasra/TwiCastingAPI
```

```python
from twicas import TwiCastingAPI
from twicas.models import User, Movie, Comment

tc = TwiCastingAPI(
    "Your ClientID",
    "Your ClientSecret",
    "Your Callback URL"
)
# Fetch user info
user_info = tc.get_user_info("user_id")
print(user_info.name)
```

## Classes
```python
class TwiCastingAPI(
    client_id: str,
    client_secret: str,
    redirect_uri: str
)
```

### Methods
Basically, all methods and models are based on the following official API documentation.
Please refer to the official API document for detailed return value and argument contents.  
**[official API documents](https://apiv2-doc.twitcasting.tv/)**
```python
def get_user_info(self, user_id: str) -> User
```

```python
def get_movie_info(self, movie_id: str) -> Movie
```

```python
def get_movies_by_user(self, user_id: str, offset: int = 0, limit: int = 20, slice_id: str = None) -> list[Movie]
```

```python
def get_current_live(self, user_id: str) -> Movie | None
```

```python
def get_comments(self, movie_id: str, offset: int = 0, limit: int = 10, slice_id: str = None) -> Tuple[int, list[Comment]]
```

## DataClasses
```python
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
```

```python
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
    broadcaster: User
    tags: list[str]
```

```python
@dataclass
class Comment():
    id: str
    message: str
    from_user: User
    created: int
```
## Exceptions
```python
class TwicastingException(Exception):
    def __init__(self, status_code: int, msg: str):
        self.msg = msg
        self.status_code = status_code
        super().__init__(self.status_code, self.msg)

    def __str__(self) -> str:
        return f"{self.status_code}: {self.msg}"


class InvalidTokenException(TwicastingException):
    """Invalid Token (code: 1000)"""


class ValidationError(TwicastingException):
    """Validation Error (code: 1001)"""


class ExecutionCountLimitationException(TwicastingException):
    """Execution Count Limitation (code: 2000)"""


class ApplicationDisabledException(TwicastingException):
    """Application Disabled (code: 2001)"""


class ProtectedException(TwicastingException):
    """Protected (code: 2002)"""


class TooManyCommentsException(TwicastingException):
    """Too Many Comments (code: 2004)"""


class OutOfScopeException(TwicastingException):
    """Out Of Scope (code: 2005)"""


class BadRequestException(TwicastingException):
    """Bad Request (code: 400)"""


class NotFoundException(TwicastingException):
    """Not Found (code: 404)"""


class InternalServerError(TwicastingException):
    """Internal Server Error (code: 500)"""
```