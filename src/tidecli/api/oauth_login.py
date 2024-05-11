"""
Provide oauth login for CLI app.

Authentication is saved to keyring.
"""

authors = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
license = "MIT"
date = "11.5.2024"

import base64
import hashlib
import http.server
import secrets
import urllib.parse
import webbrowser
from dataclasses import dataclass

import click
import requests

from tidecli.tide_config import (
    CLIENT_ID,
    REDIRECT_URI,
    SCOPE,
    BASE_URL,
    AUTH_ENDPOINT,
    TOKEN_ENDPOINT,
    PROFILE_ENDPOINT,
    PORT,
)
from tidecli.utils.handle_token import save_token


def create_s256_code_challenge(code_verifier: str) -> str:
    """
    Create the code challenge for the OAuth2 authentication (PKCE).

    :param code_verifier: Random string generated for the code verifier
    :return: The code challenge hash
    """
    data = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


@dataclass
class OAuthAuthenticator:
    """Class for OAuth2 authenticating."""

    def auth(self) -> bool:
        """Authenticate the user for the TIM API."""
        # Generating a random string for the code verifier
        code_verifier = secrets.token_urlsafe(48)
        # Generating the code challenge hash
        code_challenge = create_s256_code_challenge(code_verifier)

        auth_params = {
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPE,
            "response_type": "code",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

        # URL where the user is directed for authentication
        auth_url_with_params = (
            f"{BASE_URL}{AUTH_ENDPOINT}?{urllib.parse.urlencode(auth_params)}"
        )

        login_successful = False

        class Handler(http.server.BaseHTTPRequestHandler):
            """
            Temporary server to handle the callback.

            This class is used to handle the callback
            from the authentication server.
            """

            def do_GET(self) -> None:

                # To access the variables from the outer function
                nonlocal login_successful

                url = urllib.parse.urlparse(self.path)
                query = urllib.parse.parse_qs(url.query)

                # Handles the case where the user denied the
                # authorization / closed the browser
                if "error" in query:
                    self.send_error(403, "Authorization denied by user")
                    return

                # Temporary code, which is used to obtain the API key
                code_query = query.get("code")
                if code_query is None:
                    self.send_error(403, "API key not found in the response.")
                    return

                code = code_query[0]

                token_params = {
                    "client_id": CLIENT_ID,
                    "redirect_uri": REDIRECT_URI,
                    "grant_type": "authorization_code",
                    "code": code,
                    "code_verifier": code_verifier,
                }

                response = requests.post(
                    url=f"{BASE_URL}{TOKEN_ENDPOINT}",
                    data=token_params,
                )

                # If the response is successful, the API key is saved,
                # else an error message is printed
                if response.status_code == 200:
                    access_token = response.json().get("access_token")
                else:
                    self.send_error(
                        response.status_code, f"Error message: {response.text}"
                    )
                    return

                # Get the user profile to save token for right user
                try:
                    res = requests.get(
                        f"{BASE_URL}{PROFILE_ENDPOINT}",
                        headers={"Authorization": f"Bearer {access_token}"},
                    )
                except requests.exceptions.RequestException as e:
                    raise click.ClickException(f"Error: {e}")

                save_token(
                    token=access_token, username=res.json().get("username")
                )

                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    "Login successful! You can now close the browser.".encode(
                        "utf-8"
                    )
                )
                login_successful = True

        # Start temporary server to handle the callback
        server = http.server.HTTPServer(("localhost", PORT), Handler)

        # Open the TIM login page
        webbrowser.open(auth_url_with_params)

        # Wait for the user to sign in or deny the authorization
        server.handle_request()

        return login_successful


def authenticate() -> bool:
    """Authenticate the user for the TIM API."""
    auth = OAuthAuthenticator()
    return auth.auth()
