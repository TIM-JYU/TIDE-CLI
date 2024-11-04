"""Test functions from client to server."""

import pytest
import tim_api


class User:
    """User class for testing."""

    def __init__(self, username: str, password: str):
        """Initialize user."""
        self.username = username
        self.password = password


user1 = User("testuser1", "test1pass")
user2 = User("testuser2", "test2pass")


# @pytest.fixture(autouse=True, scope="module")
# def user_setup():
#     """Set up user login for running tests."""
#     session = tim_api.get_session()
#     tim_api.login(user1.username, user1.password, session)

#     # By using tim_api, create some documents for testing purposes into local TIM.

# TODO: install dependencies before tests

def auth_test_user():
    session = tim_api.get_session()
    tim_api.login(user1.username, user1.password, session)
    
def setup_tim_test_data():
    tim_api.create_or_get_item(tim_api.ItemType.Document, "/users/test-user-1/kissa/istuu")
    # TODO: Luo testidataa/dokumentteja ide clitä varten
    pass

def teardown_tim_test_data():
    # TODO: Poista testitapaus dokumentit lokaalista timistä
    pass

@pytest.fixture(scope="session", autouse=True)
def tim_test_data():
    auth_test_user()
    setup_tim_test_data()

    # wait for tests to run
    yield
    
    # teardown
    teardown_tim_test_data()

