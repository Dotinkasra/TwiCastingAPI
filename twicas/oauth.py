from twicas.models.access_token import TwiCastingAccessToken
from twicas.errors.twicasting_exceptions import *
from twicas.module import TwiCastingModule

from requests_oauthlib import OAuth2Session
import pickle, requests, pathlib, os

class TwiCastingOAuth:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._session = OAuth2Session(self._client_id)
        self._local_token_path = "./.data/twicasting_token"

    def fetch_authorize_endpoint_url(self) -> str:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        OAUTH_URL = "https://apiv2.twitcasting.tv/oauth2/authorize"

        auth_url, _ = self._session.authorization_url(OAUTH_URL)
        return auth_url

    def fetch_authorize_token(self, code: str) -> TwiCastingAccessToken:
        TOKEN_URL = f"https://apiv2.twitcasting.tv/oauth2/access_token"
        parameters = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "redirect_uri": self._redirect_uri
        }
        response = requests.post(TOKEN_URL, data= parameters).json()
        TwiCastingModule.response_validation(response)

        access_token = TwiCastingAccessToken(expires_in=response["expires_in"], access_token=response["access_token"])
        self.save_token(access_token)
        return access_token

    def save_token(self, token: TwiCastingAccessToken):
        if not os.path.exists(self._local_token_path):
            os.mkdir("./.data")
        with open(self._local_token_path, 'wb') as f:
            pickle.dump(token, f, protocol=5)

    def load_token(self) -> TwiCastingAccessToken:
        with open(self._local_token_path, 'rb') as f:
            return pickle.load(f)
    
    def exists_token(self) -> bool:
        if pathlib.Path(self._local_token_path).is_file():
            return True
        return False
    
    def delete_token(self):
        if self.exists_token():
            os.remove(self._local_token_path)
        
    