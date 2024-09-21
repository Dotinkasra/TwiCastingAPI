from twicas.models.user import User
from twicas.models.movie import Movie
from twicas.oauth import TwiCastingOAuth

import requests

class TwiCastingAPI:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self._twicasting_oauth = TwiCastingOAuth(client_id, client_secret, redirect_uri)
        self._token = self._twicasting_oauth.load_token() if self._twicasting_oauth.exists_token() else self._do_oauth()
        self._request_header = {
            "Accept": "application/json",
            "X-Api-Version": "2.0",
            "Authorization": f"Bearer {self._token.access_token}"
        }

    def _do_oauth(self):
        endpoint = self._twicasting_oauth.fetch_authorize_endpoint_url()
        print(endpoint)
        code = input("上記リンクを開きCODE入力")
        return self._twicasting_oauth.fetch_authorize_token(code)
    
    def get_user_info(self, user_id: str) -> User:
        url = f"https://apiv2.twitcasting.tv/users/{user_id}"
        response = requests.get(url, headers=self._request_header).json()

        return User(**response["user"])
    
    def get_movie_info(self, movie_id: str) -> Movie:
        url = f"https://apiv2.twitcasting.tv/movies/{movie_id}"
        response = requests.get(url, headers=self._request_header).json()

        return Movie(
            tags=response["tags"],
            broadcaster=User(**response["broadcaster"]),
            **response["movie"]
        )
    
    def get_movies_by_user(self, user_id: str, offset: int = 0, limit: int = 20, slice_id: str = None) -> list[Movie]:
        url = f"https://apiv2.twitcasting.tv/users/{user_id}/movies"
        response = requests.get(url, headers=self._request_header, params={"offset":offset, "limit": limit, "slice_id": slice_id}).json()

        return [Movie(
            broadcaster=None,
            tags=None,
            **movie
        ) for movie in response["movies"]]
    
    def get_current_live(self, user_id: str) -> Movie | None:
        url = f"https://apiv2.twitcasting.tv/users/{user_id}/current_live"
        response = requests.get(url, headers=self._request_header).json()

        if response["live"] is None:
            return None

        return Movie(
            tags=response["tags"],
            broadcaster=User(**response["broadcaster"]),
            **response["movie"]
        )
