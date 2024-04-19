"""Module for creating file structures for tasks and demos."""

import json
import click.exceptions
from pathlib import Path

from tidecli.models.task_data import TaskData, TaskFile

METADATA_NAME = ".timdata"


def create_tasks(
    task_datas: list[TaskData], overwrite: bool, user_path: str | None = None
) -> bool:
    """
    Create multiple tasks.

    :param task_datas: List of TaskData objects
    :param overwrite: Flag if overwrite
    :param user_path: Path to user given folder

    return: True if tasks are created, False if not
    """
    for task in task_datas:
        create_task(task_data=task, overwrite=overwrite, user_path=user_path)
    return True


def create_task(
    task_data: TaskData, overwrite: bool, user_path: str | None = None
) -> bool:
    """
    Create a single task.

    :param task_data: TaskData object
    :param overwrite: Flag if overwrite
    :param user_path: Path to user given folder

    return: True if task is created, False if not
    """

    # Sets path to current path or user given path
    if user_path:
        user_folder = Path.cwd().joinpath(user_path)
    else:
        user_folder = Path.cwd()

    end = Path(task_data.ide_task_id)
    end_path = Path(Path(task_data.path).parts[-1])
    end_path = end_path.joinpath(end)

    # Add course path to create task path
    user_folder = user_folder.joinpath(end_path)

    # Fix for tasks that have file_name without suffix
    for f in task_data.task_files:
        path = Path(f.file_name)
        suffix = path.suffix

        if suffix != "":
            continue

        file_type = task_data.run_type
        if file_type == "c++" or file_type == "cpp":
            f.file_name = f.file_name + ".cpp"

        if file_type == "cc":
            f.file_name = f.file_name + ".c"

    saved = save_file(
        task_files=task_data.task_files, save_path=user_folder, overwrite=overwrite
    )

    if not saved:
        return False

    saved = write_metadata(
        folder_path=user_folder,
        metadata=task_data,
    )

    return saved


def save_file(task_files: list[TaskFile], save_path: Path, overwrite=False) -> bool:
    """
    Create files of tasks in the given path.

    :param task_files: Dict or list of dicts. Contain name with file extension (.eg .py or .txt ...) and content
    :param save_path: Path to exercises in TIM
    :param overwrite: Flag if overwrite

    """

    save_path.mkdir(parents=True, exist_ok=True)

    for f in task_files:
        file_path = save_path.joinpath(f.file_name)
        if file_path.exists():
            if not overwrite:
                click.echo(
                    f"File {file_path} already exists\nTo overwrite give tide task create -f {save_path} \n"
                )
                return False
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f.content)
            file.close()
    click.echo(f"Task created in {save_path}")
    return True


def write_metadata(folder_path: Path, metadata: TaskData) -> bool:
    """
    Write metadata.json to the given folder path.
    :param metadata: TaskData object
    :param folder_path: Path to folder to create metadata.json
    """
    metadata_path = Path(folder_path).joinpath(METADATA_NAME)
    write_mode = "w"
    if metadata_path.exists():
        write_mode = "w"
    with open(metadata_path, write_mode, encoding="utf-8") as file:
        content = metadata.model_dump_json()
        file.write(content)
        file.close()

    return True


def create_file(item: dict, folder_path: Path, overwrite=False):
    """
    Create files of tasks in the given path.

    :param item: Single dict, contains file data
    :param folder_path: Path to folder to create task folder and file
    :param overwrite: Flag if overwrite

    """
    # By default, writemode is CREATE
    # If path exists already, write mode is WRITE (overwrites)
    if folder_path.exists():
        if not overwrite:
            # Raise SystemExit with code 1
            click.ClickException(f"Folder {folder_path} already exists")

    # Write the file with desired writemode, CREATE or WRITE
    with open(folder_path, "x", encoding="utf-8") as file:
        file.write(item["code"])
        file.close()


def get_task_file_data(file_path: Path, metadata: TaskData) -> list[TaskFile]:
    """
    Get file data from the given path excluding .json files.

    :param metadata: TaskData object
    :param file_path: Path to the directory containing the files.
    :return: File data
    """

    task_files = metadata.task_files

    files_in_dir = [
        f for f in file_path.iterdir() if f.is_file() and not f.suffix == METADATA_NAME
    ]

    for f1 in task_files:
        for f2 in files_in_dir:
            if f1.file_name == f2.name:
                with open(f2, "r", encoding="utf-8") as answer_file:
                    f1.content = answer_file.read()

    return task_files


def get_metadata(metadata_path: Path) -> TaskData:
    """
    Get metadata from the given path.

    :param metadata_path: Path to the directory containing the metadata.json file.
    :return: Metadata
    :raises: ClickException if metadata not found
    """

    metadata_path = metadata_path / METADATA_NAME
    if not metadata_path.exists():
        raise click.ClickException(f"Metadata not found in {metadata_path}")
    try:
        with open(metadata_path, "r", encoding="utf-8") as file:
            metadata = json.load(file)
            return TaskData(**metadata)
    except Exception as e:
        raise click.ClickException(f"Error reading metadata: {e}")
