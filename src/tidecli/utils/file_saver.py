import os
import sys
import json
import shutil
from tidecli.api.routes import Routes
from tidecli.models.TaskData import TaskData
from tidecli.models.Course import Course


def create_task_files(task_data, file_path):
    """
    Creates files of tasks in the given path.
    """
    # TODO: Tiedoston luonti useammalle tehtävälle
    # TODO: file_name oikeasta datasta
    file_name = "metadata.json"
    full_file_path = os.path.join(file_path, file_name)

    # task_data string conversion
    task_data = json.dumps(task_data, indent=4)

    # Check if the file already exists
    overwrite = ""
    if os.path.exists(full_file_path):
        while overwrite.lower() not in ["y", "n"]:
            overwrite = input(f"File already exists: {full_file_path} \nDo you want to overwrite the file? (y/n): ")
            if overwrite.lower() == "y":
                with open(full_file_path, "w") as file:
                    file.write(task_data)
                    print(f"File overwritten: {full_file_path}")
            elif overwrite.lower() == "n":
                print(f"File {file_name} not overwritten.")
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    if overwrite == "n":
        return
    # Write task data to file
    with open(full_file_path, "w") as file:
        file.write(task_data)


def create_metadata(courses: list[Course]):
    """
    Creates a metadata.json for each course
    """

    # TODO: tee metadata kaikkien kurssien kaikista tehtävistä
    metadata = []
    for course in courses:
        item = {
            "name": course.name,
            "id": course.id,
            "path": course.path,
            "demos":[]
        }

        for demo in course.demo_paths:
            #tasks = Routes.get_tasks_by_doc_path(doc_path=demo)
            pass

        metadata.append(item)
    print(metadata)
            

def create_demo_strucure(courses: list[Course], overwrite=False):
    """
    This creates a whole folder and filestructure

    :param tasks: List of tasks validated to TaskData
    :param tasks_demo_path: The path from course object, tells where to create tasks
    """

    # TODO: luo demotehtävien perusteella tiedostorakenne
    for course in courses:
        # create_files(files=task.task_files, folder_path=tasks_demo_path, overwrite=overwrite)
        pass


def create_demo_task(task_data: TaskData):
    """
    Creates a single demo
    :param task_data: Validated task data
    
    """
    # TODO: ehkä pitäsi vaan luoda kaikki demot kerralla

    files = []
    for task in task_data.task_files:
        item = {
            "code": task.content,
            "path": task.path,
            "header": task_data.header
        }

        files.append(item)
        
        folder_path = os.path.join(os.environ['HOME'], 'Desktop', 'Ohjelmointikurssi/Demo')
    create_files(files=files, folder_path=folder_path)
    
        
def create_files(files: list[dict]|dict, folder_path: str, overwrite=False):
    """
    Creates files of tasks in the given path.

    :param files: Dict or list of dicts. Contain name with file extension (.eg .py or .txt ...) and content
    :param folder_path: Demo path to folder to create taskfolder and file
    :param overwrite: Flag if overwrite

    """

    if os.path.exists(folder_path):
        if isinstance(files, dict):
            create_file(files, folder_path=folder_path, overwrite=overwrite)
            return
        
        if os.listdir(folder_path) != 0:
            if not overwrite:
                # Raise SystemExit with code 1
                #TODO: käsittele ylikirjoitus kunnolla, sekä yhden että monen tiedoston tapauksessa
                print("Ei ylikirjoiteta, tämä on käsiteltävä erikseen.")
                exit(1)
            else:
                shutil.rmtree(folder_path)


    os.makedirs(folder_path, exist_ok=overwrite)
    
    for item in files:
        full_file_path = os.path.join(folder_path, item['header'], item['path'])

        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        with open(full_file_path, 'x') as file:
            file.write(item['code'])
            file.close()


def create_file(item: dict, folder_path: str, overwrite=False):
    """
    Creates files of tasks in the given path.
    :param item: Single dict, contains file data
    :param folder_path: Path to folder to create task folder and file 
    :param overwrite: Flag if overwrite

    """
    
    full_file_path = os.path.join(folder_path, item['header'], item['path'])
    # By default, writemode is CREATE
    # If path exists already, write mode is WRITE (overwrites)
    writemode = 'x'
    if os.path.exists(full_file_path):
        if not overwrite:
            # Raise SystemExit with code 1
            exit(1)
            
        writemode = 'w'
            
    #os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
    # Write the file with desired writemode, CREATE or WRITE
    with open(full_file_path, 'x') as file:
        file.write(item['code'])
        file.close()
        
            

def formulate_metadata(courses: list, tasks: list):
    return [courses, tasks]


def create_folders(course_data, user_location):
    """
    Creates folder structure for task/demo paths in course data.
    """
    test_task_data = Routes().get_task_by_ide_task_id(ide_task_id="Tehtävä1", doc_path="courses/ohjelmointikurssi1"
                                                                                       "/Demot/Demo1")
    if not test_task_data:
        print("No task data found for the given ide_task_id.")
        return

       # [{'ide_files': {'code': "print('Hello world!')",
       #                              'path': 'main.py'},
       #                'task_info': {'header': 'Hello world!',
       #                              'stem': 'Kirjoita viesti maailmalle',
       #                              'answer_count': None,
       #                              'type': 'py'},
       #                'task_id': '60.pythontesti',
       #                'document_id': 60,
       #                'paragraph_id': 'Xelt2CQGvUwL',
       #                'ide_task_id': 'Tehtävä1'}]

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
            print(f"Invalid path or insufficient permissions for {user_selected_path} \nTry again.\n"
                  f"Enter 'q' to quit.\n"
                  f"Enter 'pwd' to print current working directory.")


# routes = Routes()

# Get course data
# user_course_data = routes.get_ide_courses()

# Users choice for custom path
# user_path = check_path_validity()
