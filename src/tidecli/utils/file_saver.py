import os

from tidecli.api.routes import Routes


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
            print(f"Invalid path or insufficient permissions for {user_selected_path} \nTry again.\n"
                  f"Enter 'q' to quit.\n"
                  f"Enter 'pwd' to print current working directory.")
    # TODO: exit loop if user enters 'q' or 'quit'
    # TODO: print current working directory


routes = Routes()

# Get course data
user_course_data = routes.get_ide_courses()

# Users choice for custom path
user_path = check_path_validity()


create_folders(user_course_data, user_path)
