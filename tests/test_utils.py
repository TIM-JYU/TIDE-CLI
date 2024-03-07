import os
from src.tidecli.utils import file_saver
# Testdata for creating filestructure
data = [
    {"course_name": "testcourse1", "course_id": 42},
    {"course_name": "testcourse2", "course_id": 1}
]


#     Root
#        |
#        testCourse2
#        |
#        tesCourse1
def test_create_structure():
    """
    Test the folder structure creation
    """
    root = file_saver.create_structure(data)
    first_course = os.path.join(root, 'testCourse2')
    second_course = os.path.join(root, 'tesCourse1')
    assert os.path.exists(first_course)
    assert os.path.exists(second_course)


def test_formulate_structure():
    """
    Test helper function for creating a structure
    """
    formulated = file_saver.write_structure(data)
    assert formulated == ['testcourse1', 'testcourse2']
