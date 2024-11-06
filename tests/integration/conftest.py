"""Test functions from client to server."""

from dataclasses import dataclass
import os
from pathlib import Path, PurePosixPath
from typing import List
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


@pytest.fixture(scope="session", autouse=True)
def tim_test_data():
    auth_test_user()
    setup_tim_test_data()

    # wait for tests to run
    yield
    
    # teardown
    teardown_tim_test_data()


# @pytest.fixture(autouse=True, scope="module")
# def user_setup():
#     """Set up user login for running tests."""
#     session = tim_api.get_session()
#     tim_api.login(user1.username, user1.password, session)

#     # By using tim_api, create some documents for testing purposes into local TIM.

def auth_test_user():
    session = tim_api.get_session()
    tim_api.login(user1.username, user1.password, session)
    

def setup_tim_test_data():
    tim_documents = parse_tim_document_tree(f"/users/test-user-1")
    for doc in tim_documents:
        tim_api.create_or_get_item(tim_api.ItemType.Document, doc.path)
        tim_api.upload_markdown(doc.path, doc.markdown)
    pass


def teardown_tim_test_data():
    # TODO: Poista testitapaus dokumentit lokaalista timistä
    # ei valttamatonta, koska setup ylikirjoittaa edellisella ajolla luomiensa dokumenttien markdownit (?)
    pass


@dataclass
class TimDocument:
    path: str
    markdown: str


def parse_tim_document_tree(user_path_root: str) -> List[TimDocument]:
    # tim task document paths (the user path part) are currently hard coded to the .md -files in tim_document_tree directory
    user_path_root = "/users/test-user-1"
    tim_document_tree_root = Path(__file__).parent.joinpath('tim_document_tree')
    print(tim_document_tree_root)
    parsed_docs: List[TimDocument] = []
    for dirpath, _, filenames in os.walk(tim_document_tree_root):
        for file in filenames:
            with open(Path(dirpath, file), "r") as md_file:
                doc_path = str(PurePosixPath(user_path_root, PurePosixPath(dirpath).relative_to(tim_document_tree_root), PurePosixPath(file).stem))
                doc_markdown = md_file.read()
                parsed_docs.append(TimDocument(path=doc_path, markdown=doc_markdown))

    return parsed_docs
