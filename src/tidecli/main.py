"""
Main module for the Tide CLI.

This module contains the main command group for the Tide CLI.
The whole CLI app may be located in different module.
"""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"

import json
from os import name
from pathlib import Path
from typing import List
from tidecli.utils import login_handler
from tidecli.utils.error_logger import Logger
import click

from tidecli.api.routes import (
    get_ide_courses,
    get_task_points,
    get_tasks_by_doc,
    get_task_by_ide_task_id,
    submit_task,
)
from tidecli.models.submit_data import SubmitData
from tidecli.models.task_data import TaskData
from tidecli.utils.file_handler import (
    answer_with_original_noneditable_sections,
    create_task,
    get_task_file_data,
    get_metadata,
    create_tasks,
)
from tidecli.utils.handle_token import delete_token
from tidecli.utils.login_handler import is_logged_in

logger = Logger()


@click.group()
def tim_ide() -> None:
    """CLI tool for downloading and submitting TIM tasks."""
    pass


@tim_ide.command()
@click.option("--json", "-j", "jsondata", is_flag=True, default=False)
def login(jsondata: bool) -> None:
    """
    Log in the user and saves the token to the keyring.

    Functionality: Opens a browser window for the user to log in.
    """
    if is_logged_in(print_errors=False, print_token_info=True):
        return

    if jsondata:
        click.echo(
            json.dumps(login_handler.login(jsondata=True), ensure_ascii=False, indent=4)
        )
    else:
        details = login_handler.login()
        logger.info(str(details).split("\n"))
        click.echo(details)


@tim_ide.command()
def logout() -> None:
    """Log out the user and deletes the token from the keyring."""
    click.echo(delete_token())


@tim_ide.command()
@click.option("--json", "-j", "jsondata", is_flag=True, default=False)
def courses(jsondata: bool) -> None:
    """
    List all courses.

    Prints all courses that the user has access to.

    If --json flag is used, the output is printed in JSON format.
    """
    if not is_logged_in():
        return

    data = get_ide_courses()

    if not jsondata:
        for course in data:
            click.echo(course.pretty_print())

    if jsondata:
        # Create JSON object list
        courses_json = [course.model_dump() for course in data]
        click.echo(json.dumps(courses_json, ensure_ascii=False, indent=4))


@click.group()
def task() -> None:
    """
    Task related commands.

    This command is used with subcommands.
    """
    pass


@task.command(name="list")
@click.option("--json", "-j", "jsondata", is_flag=True, default=False)
@click.argument("demo_path", type=str, required=True)
def list_tasks(demo_path: str, jsondata: bool) -> None:
    """
    Fetch tasks by doc path.

    Fetches all tasks from the given doc path and prints them.
    :param demo_path: Path to the demo file.
    :param jsondata: If True, prints the output in JSON format.

    """
    if not is_logged_in():
        return

    tasks: List[TaskData] = get_tasks_by_doc(doc_path=demo_path)

    if not jsondata:
        for t in tasks:
            click.echo(t.pretty_print())

    if jsondata:
        # Create JSON object list
        tasks_json = [t.to_json() for t in tasks]
        click.echo(json.dumps(tasks_json, ensure_ascii=False, indent=4))



@task.command(name="points")
@click.option("--json", "-j", "json_format", is_flag=True, default=False)
@click.argument("doc_path", type=str, required=True)
@click.argument("ide_task_id", type=str, required=True)
def points(doc_path: str, ide_task_id: str, json_format: bool):
    points = get_task_points(ide_task_id, doc_path)
    click.echo(points)


@task.command()
@click.option("--all", "-a", "all", is_flag=True, default=False)
@click.option("--force", "-f", "force", is_flag=True, default=False)
@click.option("--dir", "-d", "dir", type=str, default=None)
@click.argument("demo_path", type=str)
@click.argument("ide_task_id", type=str, default=None, required=False)
def create(demo_path: str, ide_task_id: str, all: bool, force: bool, dir: str) -> None:
    """Create tasks based on options."""
    if not is_logged_in():
        return

    if all:
        # Create all tasks
        tasks: List[TaskData] = get_tasks_by_doc(doc_path=demo_path)
        create_tasks(tasks=tasks, overwrite=force, user_path=dir)

    elif ide_task_id:
        # Create a single task
        task_data: TaskData = get_task_by_ide_task_id(
            ide_task_id=ide_task_id, doc_path=demo_path
        )
        create_task(task=task_data, overwrite=force, user_path=dir)

    else:
        click.echo("Please provide either --all or an ide_task_id.")


@task.command()
@click.argument("file_path_string", type=str, required=True)
def reset(file_path_string: str):
    """
    Enter the path of the task file to reset.
    """
    if not is_logged_in():
        return

    file_path = Path(file_path_string)
    if not file_path.exists() or not file_path.is_file():
        raise click.ClickException("Invalid path.")

    file_contents = file_path.read_text()

    metadata = get_metadata(file_path.parent)
    task_file_contents = next((x.content for x in metadata.task_files if x.file_name == file_path.name), None)
 
    if task_file_contents == None:
        raise click.ClickException("File is not part of this task")
    
    combined_contents = answer_with_original_noneditable_sections(file_contents, task_file_contents)
    
    file_path.write_text(combined_contents)


@tim_ide.command()
@click.argument("path", type=str, required=True)
@click.argument("file_name", type=str, required=False)
def submit(path: str, file_name: str) -> None:
    """
    Enter the path of the task folder to submit the task/tasks to TIM.

    Path must be inserted in the following format: "/path/to/task/folder".
    """
    if not is_logged_in():
        return

    path = Path(path)
    if not path.exists():
        raise click.ClickException(
            "Invalid path. Give an absolute path to the task folder \
            in the local file system"
        )

    # Get metadata from the task folder
    metadata = get_metadata(path)
    if not metadata:
        raise click.ClickException("Invalid metadata")

    answer_files = get_task_file_data(path, metadata)
    if not answer_files:
        raise click.ClickException("Invalid task file")

    for f in answer_files:
        if file_name and f.file_name != file_name:
            continue

        t = SubmitData(
            code_files=[f],
            code_language=metadata.run_type,
        )
        feedback = submit_task(t)
        click.echo(feedback.console_output())


tim_ide.add_command(task)

if __name__ == "__main__":
    tim_ide()
