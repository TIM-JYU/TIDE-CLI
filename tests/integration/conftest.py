"""Test functions from client to server."""

from dataclasses import dataclass
import os
from pathlib import Path, PurePosixPath
from typing import List
import pytest
import shutil
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
    tim_documents = parse_tim_document_tree()
    for doc in tim_documents:
        tim_api.create_or_get_item(tim_api.ItemType.Document, doc.path)
        tim_api.upload_markdown(doc.path, doc.markdown)
        if doc.is_landing_page:
            tim_api.add_document_to_my_courses(doc.path)
    pass


def teardown_tim_test_data():
    # TODO: Poista testitapaus dokumentit lokaalista timistä
    # ei valttamatonta, koska setup ylikirjoittaa edellisella ajolla luomiensa dokumenttien markdownit (?)
    pass


@dataclass
class TimDocument:
    """Data used to create a TIM document."""

    path: str
    """TIM path of the document."""

    markdown: str
    """Markdown content of the document."""

    is_landing_page: bool
    """Is the document the main document of a course"""


def parse_tim_document_tree() -> List[TimDocument]:
    tim_document_tree_root = Path(__file__).parent.joinpath("tim_document_tree")
    parsed_docs: List[TimDocument] = []
    for dirpath, _, filenames in os.walk(tim_document_tree_root):
        for filename in filenames:
            with open(Path(dirpath, filename), "r") as md_file:
                doc_path = str(
                    PurePosixPath(
                        PurePosixPath(dirpath).relative_to(tim_document_tree_root),
                        PurePosixPath(filename).stem,
                    )
                )
                doc_markdown = md_file.read()
                is_landing_page = "landing" in filename
                parsed_docs.append(
                    TimDocument(
                        path=doc_path,
                        markdown=doc_markdown,
                        is_landing_page=is_landing_page,
                    )
                )

    return parsed_docs


# TODO: create a constants file or something?
tmp_dir_path = "tmp-test-resources"

@pytest.fixture(scope="function")
def tmp_dir():
    """
    Create and remove temporary directory for task files.
    """
    os.makedirs(tmp_dir_path, exist_ok=True)

    yield

    shutil.rmtree(tmp_dir_path)
