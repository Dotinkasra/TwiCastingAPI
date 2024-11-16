"""
The MIT License (MIT)

Copyright (c) 2024 Dotinkasra.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from twicas.models.user import User
from twicas.models.movie import Movie
from twicas.models.comment import Comment
from twicas.oauth import TwiCastingOAuth
from twicas.module import TwiCastingModule
from twicas.errors.twicasting_exceptions import TwicastingException

import requests
from typing import Tuple

class TwiCastingAPI:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self._twicasting_oauth = TwiCastingOAuth(client_id, client_secret, redirect_uri)
        self._token = self._twicasting_oauth.load_token() if self._twicasting_oauth.exists_token() else self._do_oauth()

    def _do_oauth(self):
        endpoint = self._twicasting_oauth.fetch_authorize_endpoint_url()
        print(endpoint)
        code = input("上記リンクを開きCODE入力")
        return self._twicasting_oauth.fetch_authorize_token(code)
    
    def reset_token(self):
        self._twicasting_oauth.delete_token()
        try:
            self._token = self._do_oauth()
        except TwicastingException as e:
            print(e)

    def _twicas_get_request(self, url: str, params: dict = None) -> dict:
        header = {
            "Accept": "application/json",
            "X-Api-Version": "2.0",
            "Authorization": f"Bearer {self._token.access_token}"
        }
        response = requests.get(url, headers=header, params=params).json()

        try:
            TwiCastingModule.response_validation(response)
        except TwicastingException as e:
            raise e
        
        return response
    
    def get_user_info(self, user_id: str) -> User:
        url = f"https://apiv2.twitcasting.tv/users/{user_id}"
        response = self._twicas_get_request(url)
        
        return User(**response["user"])
    
    def get_movie_info(self, movie_id: str) -> Movie:
        url = f"https://apiv2.twitcasting.tv/movies/{movie_id}"
        response = self._twicas_get_request(url)

        return Movie(
            tags=response["tags"],
            broadcaster=User(**response["broadcaster"]),
            **response["movie"]
        )
    
    def get_movies_by_user(self, user_id: str, offset: int = 0, limit: int = 20, slice_id: str = None) -> list[Movie]:
        url = f"https://apiv2.twitcasting.tv/users/{user_id}/movies"
        response = self._twicas_get_request(url, params = {"offset":offset, "limit": limit, "slice_id": slice_id})
        
        return [Movie(
            broadcaster=None,
            tags=None,
            **movie
        ) for movie in response["movies"]]
    
    def get_current_live(self, user_id: str) -> Movie | None:
        url = f"https://apiv2.twitcasting.tv/users/{user_id}/current_live"
        response = self._twicas_get_request(url)
        if response["live"] is None:
            return None

        return Movie(
            tags=response["tags"],
            broadcaster=User(**response["broadcaster"]),
            **response["movie"]
        )
    
    def get_comments(self, movie_id: str, offset: int = 0, limit: int = 10, slice_id: str = None) -> Tuple[int, list[Comment]]:
        url = f"https://apiv2.twitcasting.tv/movies/{movie_id}/comments"
        response = self._twicas_get_request(url, params={"offset":offset, "limit": limit, "slice_id": slice_id})
        
        return (
            response["all_count"],
            [Comment(
                id=comment["id"],
                message=comment["message"],
                from_user=User(**comment["from_user"]),
                created=comment["created"],
            ) for comment in response["comments"]]
        )
