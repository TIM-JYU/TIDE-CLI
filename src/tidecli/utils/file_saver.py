"""Module for creating file structures for tasks and demos."""

import os
import shutil
from tidecli.api.routes import Routes
from tidecli.models.TaskData import TaskData
from tidecli.models.TaskMetadata import TaskMetadata
from tidecli.models.Course import Course
from pathlib import Path


def create_demo_tasks(course: Course):
    """
    Create all tasks in excercise.

    :param tasks: all tasks in
    """
    for demo_path in course.demo_paths:
        tasks = Routes.get_tasks_by_doc_path(demo_path)
        for task in tasks:
            create_demo_task(task_data=task, course_name=course.name, demo_path=demo_path)


def create_demo_task(task_data: TaskData, course_name: str, demo_path: str):
    """
    Create a single task.

    :param task_data: Validated task data
    :param course_name: course name
    :param demo_path: path to demo in TIM

    """
    # TODO: ehkä pitäsi vaan luoda kaikki demot kerralla

    files = []
    for task in task_data.task_files:
        item = {
            "code": task.content,
            "path": task.path,
        }

        files.append(item)

    code_language = task_data.type
    demo_folder = demo_path.split("/")[-1]
    # TODO: muuta toimimaan käyttäjän antamalla polulla
    user_folder = Path.home()
    folder_path = str(user_folder.joinpath('Desktop', course_name, demo_folder, task_data.header))

    create_files(files=files,
                 folder_path=folder_path,
                 demo_path=demo_path,
                 overwrite=False)

    write_metadata(folder_path,
                   task_data.task_id,
                   demo_path=demo_path,
                   doc_id=task_data.doc_id,
                   code_language=code_language)


def create_files(files: list[dict] | dict, folder_path: str, demo_path: str, overwrite=False):
    """
    Create files of tasks in the given path.

    :param files: Dict or list of dicts. Contain name with file extension (.eg .py or .txt ...) and content
    :param folder_path: Demo path to folder to create taskfolder and file
    :param demo_path: Path to excercises in TIM
    :param overwrite: Flag if overwrite

    """
    if os.path.exists(folder_path):
        if isinstance(files, dict):
            create_file(files, folder_path=folder_path, overwrite=overwrite)
            return

        if os.listdir(folder_path) != 0:
            if not overwrite:
                # Raise SystemExit with code 1
                # TODO: käsittele ylikirjoitus kunnolla, sekä yhden että monen tiedoston tapauksessa
                print("TODO: Ei ylikirjoiteta, tämä on käsiteltävä erikseen.")
                exit(1)
            else:
                shutil.rmtree(folder_path)

    os.makedirs(folder_path, exist_ok=overwrite)

    for item in files:
        full_file_path = str(Path(folder_path).joinpath(item['path']))
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        with open(full_file_path, 'x') as file:
            file.write(item['code'])
            file.close()


def write_metadata(folder_path: str, task_id: str, demo_path: str, doc_id: int, code_language: str):
    """
    Write metadata.json to the given folder path.

    :param folder_path: Path to folder to create metadata.json
    :param task_id: Task id
    :param demo_path: Path to excercises in TIM
    :param doc_id: Document id
    :param code_language: Language of the code
    """
    metadata = {
        "task_id": task_id,
        "demo_path": demo_path,
        "doc_id": doc_id,
        "code_language": code_language
    }

    valid_metadata = TaskMetadata(**metadata)
    metadata_path = str(Path(folder_path).joinpath("metadata.json"))
    writemode = "w"
    if os.path.exists(metadata_path):
        writemode = "x"
    with open(metadata_path, writemode) as file:
        content = valid_metadata.pretty_print()
        file.write(content)
        file.close()


def create_file(item: dict, folder_path: str, overwrite=False):
    """
    Create files of tasks in the given path.

    :param item: Single dict, contains file data
    :param folder_path: Path to folder to create task folder and file
    :param overwrite: Flag if overwrite

    """
    full_file_path = str(Path(folder_path).joinpath(item['path']))
    # By default, writemode is CREATE
    # If path exists already, write mode is WRITE (overwrites)
    if os.path.exists(full_file_path):
        if not overwrite:
            # Raise SystemExit with code 1
            exit(1)

    # os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
    # Write the file with desired writemode, CREATE or WRITE
    with open(full_file_path, 'x') as file:
        file.write(item['code'])
        file.close()


def get_task_file_data(file_path: str):
    """
    Get file data from the given path excluding .json files.

    :param file_path: Path to the directory containing the files.
    :return: File data
    """
    files_in_dir = os.listdir(file_path)

    if not files_in_dir:
        print(f"No files found in {file_path}")
        return

    for file_name in files_in_dir:
        if os.path.isfile(os.path.join(file_path, file_name)) and not file_name.endswith('.json'):
            with open(os.path.join(file_path, file_name), "r") as file:
                file_data = file.read()
                return file_data


def get_metadata(path: str):
    """
    Get metadata from the given path.

    :param path: Path to the directory containing the metadata.json file.
    :return: Metadata
    """
    metadata_path = os.path.join(path, "metadata.json")
    if not os.path.exists(metadata_path):
        print(f"Metadata not found in {path}")
        return

    with open(metadata_path, "r") as file:
        metadata = json.load(file)
        file.close()
    return metadata
  