import os
import unittest
from tidecli.utils import file_saver
# Testdata for creating filestructure
file_data = {
    "code": "print('Hello World1')",
    "path": "main.py",
    "ide_task_id": "T1",
    "paragraph_id": "123",
}

folder_data =  [{'ide_files': {'code': "print('Hello world!')",
                               'path': 'main.py'},
                 'task_info': {'header': 'Hello world!',
                               'stem': 'Kirjoita viesti maailmalle',
                               'answer_count': None,
                               'type': 'py'},
                 'task_id': '60.pythontesti',
                 'document_id': 60,
                 'paragraph_id': 'Xelt2CQGvUwL',
                 'ide_task_id': 'Tehtävä1'}]


class TestCreateFolders():
    """
    Test the folder structure creation
    """

    def test_create_folders():
        temp = '/home/riikoovy'
        file_saver.create_folders(folder_data, temp)
        assert os.path.exists(os.path.join(temp, 'Ohjelmointikurssi1/courses/ohjelmointikurssi1/Demot/Demo1'))


class TestCreateFile():
    def test_create_task_file():
        """
        Test helper function for creating a file
        """
        
        file = file_saver.create_task_file(file_data)
        assert os.path.exists(os.path.join(file, 'main.py'))
