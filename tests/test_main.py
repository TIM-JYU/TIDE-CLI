from click.testing import CliRunner
from src.tidecli.main import login

# Tests for login function
def test_login_simple():
    runner = CliRunner()
    res = runner.invoke(login)
    assert res.output == "Login link: https://example.org/\n"
