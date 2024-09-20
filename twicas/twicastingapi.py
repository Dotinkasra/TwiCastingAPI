from twicas.models.user import TwiCastingUserInfo
from twicas.models.movie import TwiCastingMovieInfo
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
    
    def get_user_info(self, user_id: str) -> TwiCastingUserInfo:
        url = f"https://apiv2.twitcasting.tv/users/{user_id}"
        response = requests.get(url, headers=self._request_header).json()

        return TwiCastingUserInfo(**response["user"])
    
    def get_movie_info(self, movie_id: str) -> TwiCastingMovieInfo:
        url = f"https://apiv2.twitcasting.tv/movies/{movie_id}"
        response = requests.get(url, headers=self._request_header).json()

        return TwiCastingMovieInfo(
            tags=response["tags"],
            broadcaster=TwiCastingUserInfo(**response["broadcaster"]),
            **response["movie"]
        )