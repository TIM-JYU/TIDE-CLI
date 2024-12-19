from os import name
from _pytest.outcomes import xfail
from click.testing import CliRunner
from playwright.sync_api import Playwright
import pytest
import subprocess
import threading
import webbrowser

from conftest import user1
from tidecli.main import login, logout


@pytest.mark.xfail(reason="Under development")
@pytest.mark.skip(reason="Under development")
def test_login(playwright: Playwright, monkeypatch: pytest.MonkeyPatch):

    def handle_login(url: str):
        # attach to existing browser
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        # ctx.set_default_timeout(5000)
        page = ctx.pages[0]

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

        # Wait for auth success
        page.locator("text='Login successful! You can now close this tab.'").wait_for()

        page.close()

    # def launch_browser_in_debug_mode(url):
    #     arguments = ["--remote-debugging-port=9001"]
    #     subprocess.run(["chromium", *arguments, url])

    # monkeypatch.setattr(webbrowser, "open", launch_browser_in_debug_mode)

    runner = CliRunner()

    res = runner.invoke(login)
    # TODO: run handle_login function after invoking the click command.
    # Both invoke and handle_login are blocking so threading is necessary.

    print(f"click says: {res}")
