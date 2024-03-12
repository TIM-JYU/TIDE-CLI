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

class TestFolderStructure(unittest.TestCase):
    """
    Test the folder structure creation
    """

    def test_create_structure():
        pass


class TestCreateFile(unittest.TestCase):
    def test_create_file():
        """
        Test helper function for creating a file
        """
        
        file = file_saver.create_file(file_data)
        assert os.path.exists(os.path.join(file, 'T1.py'))
