import base64
import os
from dataclasses import dataclass
import hashlib
import requests
import webbrowser
import urllib.parse
import secrets
import http.server

import configparser

config = configparser.ConfigParser()
config_path = os.path.abspath(os.path.join('..', 'config.ini'))
config.read(config_path)

client_id = config['OAuthConfig']['client_id']
auth_url = config['OAuthConfig']['auth_url']
token_url = config['OAuthConfig']['token_url']
redirect_uri = config['OAuthConfig']['redirect_uri']
scope = config['OAuthConfig']['scope']


def create_s256_code_challenge(code_verifier: str):
    data = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


# Apuluokka, joka hoitaa OAuth-autentikoinnin ilman lisäkirjastoja
@dataclass
class OAuthAuthenticator:
    client_id: str  # Sovelluksen ID (oltava sama kuin TIM:ssä)
    auth_url: str  # URL, johon käyttäjä ohjataan autentikoinnin ajaksi
    token_url: str  # URL, josta saa API-avaimen
    port: int  # Portti, jossa odotetaan autentikointipalvelimen vastausta. Tämä oltava TIMin tiedossa.
    scope: str  # Mitä oikeuksia avain pyytää

    def authenticate(self) -> str:
        # Generoidaan varmistusavain
        # Tämä avain toimii samalla tavalla kuin client_secret, mutta se generoidaan autentikoinnin yhteydessä
        code_verifier = secrets.token_urlsafe(48)
        # Hashataan varmistusavain, joka lähetetään autentikointipalvelimelle
        code_challenge = create_s256_code_challenge(code_verifier)

        # Tämä osoite tulee olla TIMin tiedossa. Tähän ohjataan käyttäjä autentikoinnin jälkeen.
        redirect_uri = f"http://localhost:{self.port}/callback"

        auth_params = {
            "client_id": self.client_id,  # Sovelluksen ID (oltava sama kuin TIM:ssä)
            "redirect_uri": redirect_uri,  # URL, johon TIM vie autentikoinnin jälkeen (oltava sama kuin TIM:ssä)
            "scope": self.scope,  # Mitä oikeuksia avain pyytää
            "response_type": "code",
            # Mitä avainta pyydetään. code = autentikointikoodi, jolla voi pyytää väliaikaisia avaimia
            "code_challenge": code_challenge,  # Varmistusavaimen hash, joka palvelin tallentaa
            "code_challenge_method": "S256",  # Varmistuksen tyyppi
        }

        # URL, johon käyttäjä ohjataan autentikoinnin ajaksi
        auth_url_with_params = f"{self.auth_url}?{urllib.parse.urlencode(auth_params)}"

        # API-avain, jota voi käyttää API-pyyntöihin
        # access_token kannattaa tallentaa johonkin, sillä se on voimassa aina pitkän ajan (oletuksena 10 pv, voi säätää TIMin puolella)
        access_token = None

        # OAuth-autentikointi vaatii, että käyttäjän tietokoneella käynnistetään väliaikainen palvelin, joka kuuntelee autentikointipalvelimen vastausta
        # Tämä tehdään siksi, koska onnistuneen autentikoinnin jälkeen käyttäjä ohjataan takaisin sovellukseen autentikointikoodin kanssa
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                # Kikka, jolla access_token saadaan ulos tästä metodista
                nonlocal access_token

                url = urllib.parse.urlparse(self.path)
                query = urllib.parse.parse_qs(url.query)

                # Handle the case where the user denied the authorization / closed the browser
                if "error" in query:
                    # Handle the case where the user denied the authorization
                    print(f"Authorization denied by user: {query['error'][0]}")
                    self.send_error(403, "Authorization denied by user")
                    return

                # Väliaikainen autentikointikoodi, jolla voi pyytää API-avainta
                # Oletuksena autentikointikoodi on voimassa 5 minuuttia, jonka aikana sitä saa käyttää vain kerran
                code = query.get("code")[0]

                # API-avain on voimassa rajoitetun ajan (oletuksena 10 pv, voi säätää TIMin puolella)
                token_params = {
                    "client_id": client_id,  # Sovelluksen ID (oltava sama kuin TIM:ssä)
                    "redirect_uri": redirect_uri,
                    # URL, johon TIM vie autentikoinnin jälkeen (oltava sama kuin TIM:ssä)
                    "grant_type": "authorization_code",
                    # Autentikointityyppi. authorization_code = käytetään autentikointikoodia, jota saatiin autentikoinnissa
                    "code": code,  # Autentikointikoodi
                    "code_verifier": code_verifier,
                    # Varmistusavain. Huom, tätä ei nyt hashata, vaan lähetetään sellaisenaan
                }


                response = requests.post(url=token_url, data=token_params)
                # Huomaa, että nyt code ei ole enää käyttökelpoinen, vaan se on hävitetty

                # Talletetaan API-avain access_token-muuttujaan

                if response.status_code == 200:
                    access_token = response.json().get("access_token")
                else:
                    print(f"Virheellinen vastauskoodi: {response.status_code}, Virheviesti: {response.text}")
                    return None

                access_token = response.json().get("access_token")



                # Lähetetään joku vastaus, jossa pyydetään käyttäjä sulkemaan selain
                self.send_response(200)
                # Palauta tekstiä UTF-8 -muodossa
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    "Sisäänkirjautuminen onnistui! Voit sulkea tämän selainikkunan.".encode(
                        "utf-8"
                    )
                )

        # Käynnistetään väliaikainen palvelin, joka kuuntelee autentikointipalvelimen vastausta
        server = http.server.HTTPServer(("localhost", self.port), Handler)

        # Avataan selain, jonka osoite on autentikointipalvelimen osoite
        webbrowser.open(auth_url_with_params)

        # Odotetaan, että käyttäjä kirjautuu sisään ja palvelin saa vastauksen
        server.handle_request()

        return access_token


authenticator = OAuthAuthenticator(client_id, auth_url, token_url, 8083, scope)

if __name__ == "__main__":
    authentication_code = authenticator.authenticate()

    # Koodia voi nyt käyttää API-kutsuihin
    # Esimerkiksi:
    res = requests.get(
        "http://webapp04.it.jyu.fi/oauth/profile",
        headers={"Authorization": f"Bearer {authentication_code}"},
    )
    print(res.json())
