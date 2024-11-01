from tim_api import login, get_session

def auth_test_user():
    session = get_session()
    login("testuser1", "test1pass", session)
    

def setup_tim_test_data():
    # TODO: Luo testidataa/dokumentteja ide clitä varten
    pass

def teardown_tim_test_data():
    # TODO: Poista testitapaus dokumentit lokaalista timistä
    pass