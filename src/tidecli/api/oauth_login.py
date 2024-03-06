import base64
from dataclasses import dataclass
import hashlib
import requests
import webbrowser
import urllib.parse
import secrets
import http.server

import configparser

from tidecli.utils.handle_token import save_token


def create_s256_code_challenge(code_verifier: str):
    data = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


@dataclass
class OAuthAuthenticator:
    """
    Class for OAuth2 authenticating
    """

    # Might need to define path manually TODO: why?
    # config_path = os.path.abspath(os.path.join('..', 'config.ini'))
    config = configparser.ConfigParser()
    config.read("config.ini")

    client_id: str = config["OAuthConfig"][
        "client_id"
    ]  # Application ID (must be the same as in TIM)
    base_url: str = config["OAuthConfig"][
        "base_url"
    ]  # URL to which the user is directed for authentication
    auth_endpoint: str = config["OAuthConfig"][
        "auth_endpoint"
    ]  # Endpoint to which the user is directed for authentication
    token_endpoint: str = config["OAuthConfig"][
        "token_endpoint"
    ]  # Endpoint to obtain the API key
    port: int = int(
        config["OAuthConfig"]["port"]
    )  # Port where the authentication server response is expected. This must be known to TIM.
    scope: str = config["OAuthConfig"]["scope"]  # Scope of the rights the key requests
    redirect_uri: str = config["OAuthConfig"][
        "redirect_uri"
    ]  # URL where the user is redirected after authentication
    profile_endpoint: str = config["OAuthConfig"][
        "profile_endpoint"
    ]  # Endpoint to obtain the user profile

    def auth(self) -> bool:
        # Generating a random string for the code verifier
        code_verifier = secrets.token_urlsafe(48)
        # Generating the code challenge hash
        code_challenge = create_s256_code_challenge(code_verifier)

        auth_params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri.format(port=self.port),
            "scope": self.scope,
            "response_type": "code",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

        # URL where the user is directed for authentication
        auth_url_with_params = (
            f"{self.base_url}{self.auth_endpoint}?{urllib.parse.urlencode(auth_params)}"
        )

        base_url = self.base_url
        token_endpoint = self.token_endpoint
        profile_endpoint = self.profile_endpoint
        login_successful = False

        class Handler(http.server.BaseHTTPRequestHandler):
            """
            Temporary server to handle the callback
            This class is used to handle the callback from the authentication server.
            """

            def do_GET(self):

                # To access the variables from the outer function
                nonlocal base_url
                nonlocal token_endpoint
                nonlocal profile_endpoint
                nonlocal login_successful

                url = urllib.parse.urlparse(self.path)
                query = urllib.parse.parse_qs(url.query)

                # Handles the case where the user denied the authorization / closed the browser
                if "error" in query:
                    print(f"Authorization denied by user: {query['error'][0]}")
                    self.send_error(403, "Authorization denied by user")
                    return

                # Temporary code, which is used to obtain the API key
                code = query.get("code")[0]

                token_params = {
                    "client_id": "oauth2_tide",
                    "redirect_uri": "http://localhost:8083/callback",
                    "grant_type": "authorization_code",
                    "code": code,
                    "code_verifier": code_verifier,
                }

                response = requests.post(
                    url=f"{base_url}{token_endpoint}",
                    data=token_params,
                )

                # If the response is successful, the API key is saved, else an error message is printed
                if response.status_code == 200:
                    access_token = response.json().get("access_token")
                else:
                    print(f"{response.status_code}, Error message: {response.text}")
                    return

                # Get the user profile to save token for right user
                try:
                    res = requests.get(
                        f"{base_url}{profile_endpoint}",
                        headers={"Authorization": f"Bearer {access_token}"},
                    )
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
                    return

                save_token(token=access_token, username=res.json().get("username"))

                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    "Login successful! You can now close the browser.".encode("utf-8")
                )
                login_successful = True

        # Start temporary server to handle the callback
        server = http.server.HTTPServer(("localhost", self.port), Handler)

        # Open the TIM login page
        webbrowser.open(auth_url_with_params)

        # Wait for the user to sign in or deny the authorization
        server.handle_request()

        return login_successful


def authenticate() -> bool:
    """
    Authenticates the user for the TIM API
    """
    auth = OAuthAuthenticator()
    return auth.auth()
