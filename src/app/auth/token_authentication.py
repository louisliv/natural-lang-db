import os
from typing import Optional

from flask.wrappers import Request
from flask import session


class TokenAuthentication:
    def __init__(self, request):
        self.app_token = os.environ.get("APP_TOKEN")
        self.request: Request = request

    def is_authenticated(self) -> bool:
        session_token = session.get("token")
        return session_token and self._is_valid_token(session_token)

    def is_authorised(self) -> bool:
        if not self.request.method == "POST":
            return False

        post_data = self.request.get_json()
        token = post_data.get("token")

        return self._is_valid_token(token)

    def _is_valid_token(self, token: Optional[str]) -> bool:
        if not token:
            return False

        return token == self.app_token
