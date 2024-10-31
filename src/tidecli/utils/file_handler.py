"""Module for creating file structures for tasks and demos."""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"

import re
import json
from typing import Any
import click.exceptions
from pathlib import Path
import itertools

from tidecli.models.task_data import SupplementaryFile, TaskData, TaskFile
from tidecli.utils.error_logger import Logger
from tidecli.api import routes

METADATA_NAME = ".timdata"
"""File to store metadata in task folder."""

# Search strings for finding the beginning and end of the task content
BEGIN_MSG_SEARCH_STRING = r"Write your code below this line"
END_MSG_SEARCH_STRING = r"Write your code above this line"

def write_file(file_path: Path, content: str | bytes) -> None:
    """
    Write content to a file.

    :param file_path: Path to the file
    :param content: Content to write
    """
    if isinstance(content, str):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
            file.close()
    else:
        with open(file_path, "wb") as file:
            file.write(content)
            file.close()


def create_tasks(
    tasks: list[TaskData], overwrite: bool, user_path: str | None = None
) -> bool:
    """
    Create multiple tasks.

    :param tasks: List of TaskData objects
    :param overwrite: Flag if overwrite
    :param user_path: Path to user given folder

    return: True if all tasks are created, False if not
    """
    combined_tasks = combine_tasks(tasks)

    task_creation_successes: list[bool] = []
    for task in combined_tasks:
        task_creation_successes.append(create_task(task=task, overwrite=overwrite, user_path=user_path))

    return all(task_creation_successes)
    

def combine_tasks(tasks: list[TaskData]) -> list[TaskData]:
    """
    Combine tasks with same ide_task_id.

    :param tasks: List of TaskData objects
    return: List of TaskData objects
    """
    # Combine tasks with same ide_task_id
    tasks_by_ide_task_id: dict[str, list[TaskData]] = {}
    for t in tasks:
        ide_task_id = t.ide_task_id
        task_list = tasks_by_ide_task_id.get(ide_task_id, [])
        task_list.append(t)
        tasks_by_ide_task_id[ide_task_id] = task_list

    # Create new list with combined tasks
    combined_tasks = []
    for ide_task_id, task_list in tasks_by_ide_task_id.items():
        combined_tasks.append(
            TaskData(
                path=task_list[0].path,
                type=task_list[0].type,
                doc_id=task_list[0].doc_id,
                ide_task_id=ide_task_id,
                task_files=[f for t in task_list for f in t.task_files],
                supplementary_files=[f for t in task_list for f in t.supplementary_files],
                stem=task_list[0].stem,
                header=task_list[0].header,
            )
        )

    return combined_tasks


def get_file_content_from_source(source: str) -> bytes | Any:
    """
    Get content of a file from its source address.
    If address does not start with http URL, it is assumed to be a TIM path.

    :param supplementary_file: SupplementaryFile object
    return: Content of the source
    """
    if source is not None:
        if re.match(r"^https?://", source):
            # Source is a http URL
            return routes.get_file_content(source)
        else:
            # Source is assumed to be a TIM path
            return routes.get_file_content(source, is_tim_file=True)


def create_task(task: TaskData, overwrite: bool, user_path: str | None = None) -> bool:
    """
    Create a single task.

    :param task: TaskData object
    :param overwrite: Flag if overwrite
    :param user_path: Path to user given folder

    return: True if task is created, False if not
    """
    # Sets path to current path or user given path
    if user_path:
        user_folder = Path.cwd() / user_path
    else:
        user_folder = Path.cwd()

    # Add course path to create task path
    user_folder = user_folder / Path(task.path).name / task.ide_task_id

    # Fix for tasks that have file_name without suffix
    for f in task.task_files:
        path = Path(f.file_name)
        suffix = path.suffix
        if suffix != "":
            continue
        f.file_name = add_suffix(f.file_name, task.run_type)

    saved = save_files(
        task_files=task.task_files, save_path=user_folder, overwrite=overwrite
    )
 
    if task.supplementary_files is not None:
        save_files(task_files=task.supplementary_files, save_path=user_folder, overwrite=overwrite)

    if saved:
        write_metadata(
            folder_path=user_folder,
            metadata=task,
        )

    return saved


def add_suffix(file_name: str, file_type: str) -> str:
    """
    Add suffix to file name if it is missing. Fix for C++ and C files.

    TODO: Support more file types, should this be done in TIM?

    :param file_name: Name of the file
    :param file_type: Type of the file
    :return: File name with suffix
    """
    if file_type == "c++" or file_type == "cpp":
        return file_name + ".cpp"

    if file_type == "cc":
        return file_name + ".c"

    return file_name


def save_files(task_files: list[TaskFile] | list[SupplementaryFile], save_path: Path, overwrite=False) -> bool:
    """
    Create files of tasks in the given path.

    :param task_files: Dict or list of dicts.
    Contain name with file extension (.eg .py or .txt ...) and content
    :param save_path: Path to exercises in TIM
    :param overwrite: Flag if overwrite
    """
    save_path.mkdir(parents=True, exist_ok=True)
    
    jsondata = click.get_current_context().params["jsondata"]

    for f in task_files:
        file_path = save_path / f.file_name
        if file_path.exists():
            if not overwrite:
                if not jsondata:
                    click.echo(
                        f"File {file_path} already exists\n"
                        f"To overwrite give tide task create -f {save_path}\n"
                    )
                return False
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if f.content is not None:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f.content)
                file.close()
        elif f.source is not None:
            # TODO: Handle potential errors from API call (allow errors so that consequent files are saved)
            # Currently, only files that in the list before an error are saved
            content = get_file_content_from_source(f.source)
            with open(file_path, "wb") as file:
                file.write(content)
                file.close()

    if not jsondata:
        click.echo(f"Task created in {save_path}")
    return True


def write_metadata(folder_path: Path, metadata: TaskData) -> None:
    """
    Write metadata.json to the given folder path.

    :param metadata: TaskData object
    :param folder_path: Path to folder to create metadata.json
    """
    metadata_path = Path(folder_path) / METADATA_NAME
    write_mode = "w"
    if metadata_path.exists():
        write_mode = "w"
    with open(metadata_path, write_mode, encoding="utf-8") as file:
        content = metadata.model_dump_json()
        file.write(content)
        file.close()


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
            raise click.ClickException(f"Folder {folder_path} already exists")

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
    logger = Logger()
    task_files = metadata.task_files

    files_in_dir = [
        f for f in file_path.iterdir() if f.is_file() and not f.suffix == METADATA_NAME
    ]
    for f1 in task_files:
        for f2 in files_in_dir:
            if f1.file_name == f2.name:
                logger.debug(
                    "Validating {0} against metadata content of task.".format(f2.name))
                with open(f2, "r", encoding="utf-8") as answer_file:
                    answer_content = answer_file.read()
                    answer_bycode, answer_gapcode = split_file_contents(
                        answer_content)
                    metadata_bycode, metadata_gapcode = split_file_contents(
                        f1.content
                    )

                    if len(metadata_bycode) == 0:
                        f1.content = answer_content
                        logger.debug("Normal exercise, no gap found.")
                        continue

                    if validate_answer_file(answer_bycode, metadata_bycode):
                        # TODO: tarvitaan lisää testitapauksia,
                        # Validator OK
                        logger.debug("Gap-type exercise answer file is valid.")
                        f1.content = "\n".join(answer_gapcode)
                    else:
                        logger.debug("Gap-type exercise answer not valid.")

                        # Validator complains about answer.
                        # Answer is submitted despite of complains.
                        f1.content = "\n".join(answer_gapcode)
                        # return []


    logger.debug(f"Task files being submitted: {task_files}")
    return task_files


def get_metadata(metadata_path: Path) -> TaskData:
    """
    Get metadata from the given path.

    :param metadata_path: Path to the directory containing the
    metadata.json file.
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


def split_file_contents(content: str) -> tuple[list[str], list[str]]:
    """
    Split file contents to find gaps in tasks.

    :param content: Content of the file
    """
    lines = re.split(r"\r?\n", content)
    gap = find_gaps_in_tasks(lines)
    if gap is None:
        return [], []

    start, end = gap

    # Create list of strings for validation
    bycodebegin = lines[:start + 1]
    bycodeend = lines[end :]
    gap_content = lines[start + 1: end]
    bycode = bycodebegin + bycodeend

    logger = Logger()
    log_text = "\n".join(gap_content)
    logger.debug(f"Text in the gap: \n{0}".format(log_text))

    return bycode, gap_content


def validate_answer_file(answer_by: list[str], metadata_by: list[str]) -> bool:
    """
    Validate answer file with the metadata.

    No other lines in the file should be modified
    than the task content lines. The task content lines are marked with
    comments/messages

    :param answerfile: Path to the answer file
    :param metadata_taskfile: Path to the metadata task file
    :return: True if the file is valid, False if not
    """
    logger = Logger()

    if len(answer_by) == 0 and len(metadata_by) == 0:
        logger.debug("Both files are empty.")
        return False

    # Clear the contents of the answer file and metadata content
    clear_answer = clear_contents(answer_by)
    clear_metadata_content = clear_contents(metadata_by)

    if clear_answer is None or clear_metadata_content is None:
        return False

    bycodediff = clear_answer.difference(clear_metadata_content)
    logger.debug("Diff between cleared answer and .timdata content: \n")
    logger.debug(bycodediff)

    if len(bycodediff) > 0:
        logger.info("Note: file has been modified outside of desired area.")

    return len(bycodediff) == 0


def clear_contents(lines_by: list[str]) -> set[str] | None:
    """
    Clear the contents of the answer file.

    :param lines: List of lines in the file
    :return: Set of lines in the file
    """
    logger = Logger()

    # Remove empty lines for comparison
    for i, line in enumerate(lines_by):
        clean = line.strip()
        if clean == "" or clean == "\n":
            lines_by.pop(i)

    logger.debug("\n".join(lines_by))

    return set(lines_by)


def find_gaps_in_tasks(lines: list[str]) -> tuple[int, int] | None:
    """
    Find gaps in tasks.

    :param lines: List of lines in the file
    """
    # TODO: Find multiple gaps, store tuples into a list
    gap = None
    start: int | None = None
    end: int | None = None

    for i, line in enumerate(lines):
        if re.search(BEGIN_MSG_SEARCH_STRING, line):
            start = i
        if re.search(END_MSG_SEARCH_STRING, line):
            end = i

    gap = (start, end)
    if start is None or end is None:
        return None

    return gap


def answer_with_original_noneditable_sections(answer: str, original: str) -> str:
    """
    Combine answer with original file, keeping non-editable sections from original.

    :param answer: Answer file content
    :param original: Original file content
    """
    answer_lines = re.split(r"\r?\n", answer)
    original_lines = re.split(r"\r?\n", original)

    answer_gaps = find_gaps_in_tasks(answer_lines)
    original_gaps = find_gaps_in_tasks(original_lines)

    if answer_gaps is None or original_gaps is None:
        # TODO! add error handling
        return answer

    combined_lines = itertools.chain(original_lines[:original_gaps[0] + 1],
                                     answer_lines[answer_gaps[0] + 1:answer_gaps[1]],
                                     original_lines[original_gaps[1]:]
                                     )
    
    return "\n".join(combined_lines)
