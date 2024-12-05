from os import name
from click.testing import CliRunner
from playwright.sync_api import Playwright
import pytest
import webbrowser

from conftest import user1
from tidecli.main import login, logout

def test_login(playwright: Playwright, monkeypatch: pytest.MonkeyPatch):
    # TODO: server.handle_request() @ oauth_login.py is blocked by playwright

    def handle_login(url: str):
        browser = playwright.chromium.launch(headless=False)
        ctx = browser.new_context()
        # ctx.set_default_timeout(5000)
        page = ctx.new_page()

        # Navigate to the auth page
        page.goto(url)

        # Click login button
        page.get_by_role("button", name="Log in").click()

        # Click "Email login"
        page.get_by_role("button", name="Email login").click()

        # Fill in login info
        page.fill("#email", user1.username)
        page.fill("#password", user1.password)

        # Click "Log in"
        page.locator("tim-login-dialog").get_by_role("button", name="Log in").click()


        # Click the authentication button
        page.click("tim-oauth-button[ng-reflect-name='Authenticate to TIDE']")

        # page.wait_for_url("http://192.168.122.102/oauth/authorize")

        # def handle_redirect(res):
        #     print(f"asd {res}")

        # page.on("response", handle_redirect)
        
        # Wait for auth success
        page.locator("text='Login successful! You can now close this tab.'").wait_for()

        page.close()

    monkeypatch.setattr(webbrowser, "open", handle_login)

    runner = CliRunner()

    res = runner.invoke(login)
    print(f"click says: {res}")

    pass


def test_login_json():
    runner = CliRunner()
    res = runner.invoke(logout)
    pass

