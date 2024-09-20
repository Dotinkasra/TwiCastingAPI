from dataclasses import dataclass

@dataclass
class TwiCastingAccessToken():
    expires_in: int
    access_token: str
    oken_type: str = "Bearer"