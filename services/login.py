from requests_oauthlib import OAuth2Session
from decouple import config
import os
from urllib.parse import urlparse, parse_qs
import requests

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class NextCloudOAuth:
    def __init__(self):
        self.client_id = config("NEXTCLOUD_CLIENT_ID")
        self.client_secret = config("NEXTCLOUD_CLIENT_SECRET")
        self.redirect_uri = config("REDIRECT_URI")
        self.scope = ["openid"]
        self.base_url_internal = "http://nextcloud"
        self.base_url_public = "https://nuvem.codegus.space"
        self.session = OAuth2Session(
            self.client_id,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
        )

    def get_authorization(self):
        auth_url = f"{self.base_url_public}/apps/oauth2/authorize"
        full_url, state = self.session.authorization_url(auth_url)
        return full_url, state

    def fetch_token(self, full_callback_url):
        token_url = f"{self.base_url_internal}/index.php/apps/oauth2/api/v1/token"
        parsed = urlparse(full_callback_url)
        code = parse_qs(parsed.query).get("code", [None])[0]
        if not code:
            raise ValueError("Código de autorização não encontrado na URL de callback.")
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(
            token_url,
            data=payload,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()