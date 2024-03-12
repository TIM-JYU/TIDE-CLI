import os

from tidecli.api.routes import get_user_task_by_taskId


# def create_task_file(course, task):
#     """
#     Create a file for a task
#     """
#     task_id = f"{course}:{task}"
#     user_task = get_user_task_by_taskId(task_id=task_id, doc_id=43)


def create_folders(course_data, user_location):
    """
    Creates folder structure for task/demo paths in course data.
    """

    for course in course_data:
        course_name = course.get("course_name")
        demo_paths = course.get("demo_paths", [])

        for demo in demo_paths:
            demo_path = demo.get("path")
            full_path = os.path.join(user_location, course_name, demo_path)

            # Creates directory and parent directories if they don't exist
            os.makedirs(full_path, exist_ok=True)
            print(f"Folders created for {full_path}")


# Usage with test data
course_data = [
    {'course_name': 'Ohjelmointikurssi1',
     'course_id': 58,
     'course_path': '/view/courses/ohjelmointikurssi1/ohjelmointikurssi1',
     'demo_paths': [{'path': 'courses/ohjelmointikurssi1/Demot/Demo1'},
                    {'path': 'courses/ohjelmointikurssi1/Demot/Demo1'}]}]

# User choice for custom location
user_location = input("Enter the custom location where you want to create the folder structure: ")


create_folders(course_data, user_location)
