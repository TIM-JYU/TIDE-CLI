import http.server
import os
import urllib.parse
import webbrowser
from http.server import SimpleHTTPRequestHandler
import requests


def authenticate():
    scope = "profile user_tasks submit_tasks user_courses"
    auth_params = {
        "client_id": os.environ["CLIENT_ID"],
        "redirect_uri": os.environ["REDIRECT_URI"],
        "response_type": "code",
        "scope": scope,
    }

    auth_url_with_params = (
        f"{os.environ['AUTH_URL']}?{urllib.parse.urlencode(auth_params)}"
    )

    class SilentHandler(SimpleHTTPRequestHandler):
        # Remove log messages
        def log_message(self, format, *args):
            pass

    class OauthHandler(SilentHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(
                    bytes(
                        f"<a href='{auth_url_with_params}'>Authenticate with TIM</a>",
                        "utf-8",
                    )
                )
            if self.path.startswith("/callback"):
                code = urllib.parse.parse_qs(
                    urllib.parse.urlparse(self.path).query
                ).get("code")
                if code:
                    code = code[0]
                    token_params = {
                        "grant_type": "authorization_code",
                        "code": code,
                        "redirect_uri": os.environ["REDIRECT_URI"],
                        "client_id": os.environ["CLIENT_ID"],
                        "client_secret": os.environ["CLIENT_SECRET"],
                    }
                    response = requests.post(os.environ["TOKEN_URL"], data=token_params)
                    access_token = response.json().get("access_token")

                    # save_token_to_user(access_token, "username")

                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(
                        bytes(
                            f"Authentication successful! You can return to TIDE-cli.",
                            "utf-8",
                        )
                    )
                    httpd.shutdown()
                    httpd.server_close()

                    return access_token

    port = 8083
    server_address = ("", port)
    httpd = http.server.HTTPServer(server_address, OauthHandler)
    print(f"Open http://localhost:{port}/ in your web browser.")
    webbrowser.open(f"http://localhost:{port}/")
    httpd.serve_forever()
