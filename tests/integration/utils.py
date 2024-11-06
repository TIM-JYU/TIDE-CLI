# from tim_api import ItemType, create_item, login, get_session
from pathlib import Path
import pytest
import tim_api

def auth_test_user():
    session = tim_api.get_session()
    tim_api.login("testuser1", "test1pass", session)
    
def setup_tim_test_data():
    tim_api.create_item(tim_api.ItemType.Document, "kissa/istuu", "foo")
    # TODO: Luo testidataa/dokumentteja ide clitä varten
    pass

def teardown_tim_test_data():
    # TODO: Poista testitapaus dokumentit lokaalista timistä
    pass

@pytest.fixture(scope="session", autouse=True)
def tim_test_data():
    print("fdsa")
    auth_test_user()
    setup_tim_test_data()

    # wait for tests to run
    yield
    
    # teardown

