"""Module for creating file structures for tasks and demos."""

import json
import shutil
from tidecli.api.routes import get_tasks_by_doc
from tidecli.models.TaskData import TaskData
from tidecli.models.TaskMetadata import TaskMetadata
from tidecli.models.Course import Course
from pathlib import Path


def create_demo_tasks(course: Course):
    """
    Create all tasks in excercise.

    :param course: Course object
    """
    for demo_path in course.demo_paths:
        tasks = get_tasks_by_doc(demo_path)
        for task in tasks:
            create_demo_task(task_data=task, course_name=course.name, demo_path=demo_path, overwrite=False)


def create_demo_task(task_data: TaskData, course_name: str, demo_path: str, overwrite: bool):
    """
    Create a single task.

    :param task_data: Validated task data
    :param course_name: course name
    :param demo_path: path to demo in TIM
    :param overwrite: Flag if overwrite

    """
    # TODO: ehkä pitäsi vaan luoda kaikki demot kerralla

    files = []
    for task in task_data.task_files:
        item = {
            "code": task.content,
            "path": task.file_name,
        }

        files.append(item)

    code_language = task_data.type
    demo_folder = demo_path.split("/")[-1]
    # TODO: muuta toimimaan käyttäjän antamalla polulla
    user_folder = Path.home()
    folder_path = str(user_folder.joinpath('Desktop', course_name, demo_folder, task_data.ide_task_id))

    create_files(files=files,
                 folder_path=folder_path,
                 demo_path=demo_path,
                 overwrite=overwrite)

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
    folder = Path(folder_path)
    if folder.exists():
        if isinstance(files, dict):
            create_file(files, folder_path=folder_path, overwrite=overwrite)
            return

        if list(folder.iterdir()):
            if not overwrite:
                # Raise SystemExit with code 1
                print(f"Folder {folder_path} already exists\n\n"
                      f"Give    main.py task create -f {demo_path} <ide_task_id>    to overwrite")
                exit(1)
            else:
                shutil.rmtree(folder_path)

    folder.mkdir(parents=True, exist_ok=overwrite)

    for item in files:
        full_file_path = Path(folder_path).joinpath(item['path'])
        full_file_path.parent.mkdir(parents=True, exist_ok=True)
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
    metadata_path = Path(folder_path).joinpath("metadata.json")
    writemode = "w"
    if metadata_path.exists():
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
    full_file_path = Path(folder_path).joinpath(item['path'])
    # By default, writemode is CREATE
    # If path exists already, write mode is WRITE (overwrites)
    if full_file_path.exists():
        if not overwrite:
            # Raise SystemExit with code 1
            exit(1)

    # Write the file with desired writemode, CREATE or WRITE
    with open(full_file_path, 'x') as file:
        file.write(item['code'])
        file.close()


def get_task_file_data(file_path: Path):
    """
    Get file data from the given path excluding .json files.

    :param file_path: Path to the directory containing the files.
    :return: File data
    """

    files_in_dir = [f for f in file_path.iterdir() if f.is_file() and not f.suffix == '.json']

    if not files_in_dir:
        print(f"No files found in {file_path}")
        return

    for file in files_in_dir:
        with open(file, "r") as f:
            file_data = f.read()
            return file_data


def get_metadata(metadata_path: Path):
    """
    Get metadata from the given path.

    :param metadata_path: Path to the directory containing the metadata.json file.
    :return: Metadata
    """
    metadata_path = metadata_path / "metadata.json"
    if not metadata_path.exists():
        print(f"Metadata not found in {metadata_path}")
        return

    with open(metadata_path, "r") as file:
        metadata = json.load(file)
    return metadata
