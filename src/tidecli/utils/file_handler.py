"""Module for creating file structures for tasks and demos."""

import json
from pathlib import Path

import click.exceptions

from tidecli.models.TaskData import TaskData, TaskFile

METADATA_NAME = ".timdata"


def create_task_set(
    task_data: TaskData | list[TaskData], overwrite: bool, user_path: str | None = None
) -> bool:
    """
    Create a single task.

    :param task_data: TaskData object
    :param overwrite: Flag if overwrite
    :param user_path: Path to user given folder

    return: True if task is created, False if not
    """

    if isinstance(task_data, list):
        for task in task_data:
            create_task_set(task_data=task, overwrite=overwrite, user_path=user_path)

    # Sets path to current path or user given path
    if user_path:
        user_folder = Path(user_path)
    else:
        user_folder = Path.cwd()

    end = Path(task_data.ide_task_id)

    end_path = Path(Path(task_data.path).parts[-1])

    end_path = end_path.joinpath(end)

    # Add course path to create task path
    user_folder = user_folder.joinpath(end_path)

    saved = save_file(
        file=task_data.task_files, save_path=user_folder, overwrite=overwrite
    )

    if not saved:
        return False

    saved = write_metadata(
        folder_path=user_folder,
        metadata=task_data,
    )

    return saved


def save_file(file: list[TaskFile], save_path: Path, overwrite=False) -> bool:
    """
    Create files of tasks in the given path.

    :param file: Dict or list of dicts. Contain name with file extension (.eg .py or .txt ...) and content
    :param save_path: Path to exercises in TIM
    :param overwrite: Flag if overwrite

    """

    if save_path.exists() and not overwrite:
        raise click.ClickException(
            f"File {save_path} already exists\n\n"
            f"Give    main.py task create -f {save_path} <ide_task_id>    to overwrite"
        )

    save_path.mkdir(parents=True, exist_ok=overwrite)

    for f in file:
        file_path = save_path.joinpath(f.file_name)
        if file_path.exists():
            if not overwrite:
                raise click.ClickException(
                    f"File {file_path} already exists\n\n"
                    f"Give    main.py task create -f {save_path} <ide_task_id>    to overwrite"
                )
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as file:
            file.write(f.content)
            file.close()

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
    with open(metadata_path, write_mode) as file:
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
    with open(folder_path, "x") as file:
        file.write(item["code"])
        file.close()


def get_task_file_data(file_path: Path, filename: str) -> str:
    """
    Get file data from the given path excluding .json files.

    :param file_path: Path to the directory containing the files.
    :return: File data
    """

    files_in_dir = [
        f for f in file_path.iterdir() if f.is_file() and not f.suffix == METADATA_NAME
    ]

    if not files_in_dir:
        click.ClickException(f"No files found in {file_path}")

    for file in files_in_dir:
        if file.name == filename:
            with open(file, "r") as f:
                file_data = f.read()
                return file_data


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
        with open(metadata_path, "r") as file:
            metadata = json.load(file)
            return TaskData(**metadata)
    except Exception as e:
        raise click.ClickException(f"Error reading metadata: {e}")
