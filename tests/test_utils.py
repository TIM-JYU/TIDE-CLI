import os
import unittest
from src.tidecli.utils import file_saver
# Testdata for creating filestructure
file_data = {
    "code": "print('Hello World1')",
    "path": None,
    "ideTask_id": "T1",
    "paragraph_id": "P1",
}

class TestCreateFolders(unittest.TestCase):
    """
    Test the folder structure creation
    """

    def test_create_folders():
        pass


class TestCreateFile(unittest.TestCase):
    def test_create_task_file():
        """
        Test helper function for creating a file
        """
        
        file = file_saver.create_task_file(file_data)
        assert os.path.exists(os.path.join(file, 'T1.py'))
