import os
import unittest
from tidecli.utils import file_saver
from unittest_prettify.colorize import (
    colorize,
    GREEN,
    YELLOW
)

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
        # file_saver.create_folders(folder_data, temp)
        assert os.path.exists(os.path.join(temp, 'Ohjelmointikurssi1/courses/ohjelmointikurssi1/Demot/Demo1'))

@colorize(color=YELLOW)
class TestCreateFile(unittest.TestCase):
    def test_create_task_file(self):
        """
        Create file when it does not exist yet
        """
        
        file = file_saver.create_task_file(file_name=file_data['path'], file_path='/home/ylivuoto', file_content=file_data['code'])
        assert os.path.exists('/home/ylivuoto/main.py')

        
    def test_create_task_file_overwrite(self):
        """
        Overwrite an existing file
        """
        
        file = file_saver.create_task_file(file_name=file_data['path'], file_path='/home/ylivuoto', file_content='HELLO', overwrite=True)
        assert os.path.exists('/home/ylivuoto/main.py')

        contents = ''
        with open('/home/ylivuoto/main.py', 'r') as file:
            contents = file.read() 
        self.assertEqual(contents, 'HELLO')

        
    def test_create_task_file_not_overwrite(self):
        """
        Do not overwrite an existing file
        """
        
        with self.assertRaises(SystemExit) as cm:
            file_saver.create_task_file(file_name=file_data['path'], file_path='/home/ylivuoto', file_content=file_data['code'])
        
            
        self.assertEqual(cm.exception.code, 1)
        

    def tearDownClass():
        os.remove('/home/ylivuoto/main.py')

