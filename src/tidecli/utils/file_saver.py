import os

from tidecli.api.routes import Routes


def create_task_files(task_data, file_path):
    """
    Creates files of tasks in the given path.
    """
    # TODO: Tiedoston luonti useammalle tehtävälle
    # TODO: file_name oikeasta datasta
    file_name = "testing.txt"
    full_file_path = os.path.join(file_path, file_name)

    # task_data string conversion
    task_data_str = str(task_data)

    # Check if the file already exists
    if os.path.exists(full_file_path):
        print(f"File already exists: {full_file_path} \nFile not created.")
        return
    # TODO: käyttäjälle mahdollisuus valita haluaako ylikirjoittaa olemassa olevan tiedoston

    # Write task data to file
    with open(full_file_path, "w") as file:
        file.write(task_data_str)


def create_folders(course_data, user_location):
    """
    Creates folder structure for task/demo paths in course data.
    """

    test_task_data = [{'ide_files': {'code': "print('Hello world!')",
                                     'path': 'main.py'},
                       'task_info': {'header': 'Hello world!',
                                     'stem': 'Kirjoita viesti maailmalle',
                                     'answer_count': None,
                                     'type': 'py'},
                       'task_id': '60.pythontesti',
                       'document_id': 60,
                       'paragraph_id': 'Xelt2CQGvUwL',
                       'ide_task_id': 'Tehtävä1'}]

    for course in course_data:
        course_name = course.get("course_name")
        demo_paths = course.get("demo_paths", [])

        for i, demo in enumerate(demo_paths):
            demo_path = demo.get("path")
            full_path = os.path.join(user_location, course_name, demo_path)

            # Creates directory and parent directories if they don't exist
            os.makedirs(full_path, exist_ok=True)
            print(f"Folders created for {full_path}")

            # Call create_task_files for the last folder in demo_paths
            if i == len(demo_paths) - 1:
                create_task_files(test_task_data, full_path)


def check_path_validity():
    """
    Check if the input path is valid
    """
    while True:
        user_selected_path = input("Enter custom path where folder structure is created: ")
        if os.path.exists(user_selected_path) and os.access(user_selected_path, os.W_OK):
            return user_selected_path
        if user_selected_path.lower() in ["q", "quit"]:
            exit()
        if user_selected_path.lower() in ["pwd", "current"]:
            print(f"Current working directory: {os.getcwd()}")
        else:
            print(f"Invalid path or insufficient permissions for {user_selected_path} \nTry again."
                  f"Enter 'q' to quit.\n"
                  f"Enter 'pwd' to print current working directory.")


routes = Routes()

# Get course data
user_course_data = routes.get_ide_courses()

# Users choice for custom path
user_path = check_path_validity()

create_folders(user_course_data, user_path)
