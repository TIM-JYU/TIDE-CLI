"""
Main module for the Tide CLI.

This module contains the main command group for the Tide CLI.
The whole CLI app may be located in different module.
"""

from pathlib import Path

import click

from tidecli.models.submit_data import SubmitData
from tidecli.models.task_data import TaskData
from tidecli.utils.file_handler import (
    create_task,
    get_task_file_data,
    get_metadata,
)
from tidecli.api.routes import (
    get_ide_courses,
    get_tasks_by_doc,
    get_task_by_ide_task_id,
    submit_task,
)

from tidecli.utils.handle_token import delete_token
from tidecli.utils.login_handler import login_details


@click.group()
def tim_ide():
    """Tide CLI base command?."""
    pass


@tim_ide.command()
def login():
    """
    Log in the user and saves the token to the keyring.

    Functionality: Opens a browser window for the user to log in.

    """
    click.echo(login_details())

    # Verify the login
    try:
        get_ide_courses()
    except Exception as e:
        raise click.ClickException(f"An error raised after login. Have you added IDE-courses to bookmarks already? Error message: {e}")


@tim_ide.command()
def logout():
    """Log out the user and deletes the token from the keyring."""
    click.echo(delete_token())


@tim_ide.command()
def courses():
    """List  all courses."""
    data = get_ide_courses()

    for course in data:
        click.echo(course.pretty_print())


@click.group()
def task():
    """Task related commands.

    It is possible to list and create all tasks per excercise or just
    create one task.

    """
    # TODO: printtaa esim. aiemmin noudetut taskit tms järkevää. Tai sitten ole printtaamatta
    pass


@task.command()
@click.argument("demo_path", type=str, required=True)
def list(demo_path):
    """Fetch tasks by doc path."""
    tasks = get_tasks_by_doc(doc_path=demo_path)

    for task in tasks:
        click.echo(task.pretty_print())


@task.command()
@click.option("--all", "-a", "all", is_flag=True, default=False)
@click.option("--force", "-f", "force", is_flag=True, default=False)
@click.option("--dir", "-d", "dir", type=str, default=None)
@click.argument("demo_path", type=str)
@click.argument("ide_task_id", type=str, default=None, required=False)
def create(demo_path, ide_task_id, all, force, dir):
    """Create tasks based on options."""
    if all:
        # Create all tasks
        tasks = get_tasks_by_doc(doc_path=demo_path)
        for task in tasks:
            if create_task(task_data=task, overwrite=force, user_path=dir):
                click.echo(f"{task.ide_task_id} was saved")
            else:
                click.echo(f"{task.ide_task_id} was not saved")

    elif ide_task_id:
        # Create a single task
        task_data: TaskData = get_task_by_ide_task_id(
            ide_task_id=ide_task_id, doc_path=demo_path
        )
        if create_task(task_data=task_data, overwrite=force, user_path=dir):
            click.echo(f"{task_data.ide_task_id} was saved")
        else:
            click.echo(f"{task_data.ide_task_id} was not saved")

    else:
        click.echo("Please provide either --all or an ide_task_id.")


@tim_ide.command()
@click.argument("path", type=str, required=True)
def submit(path):
    """
    Enter the path of the task folder to submit the task to TIM.
    Path must be inserted in the following format: "/path/to/task/folder".
    """
    path = Path(path)

    if not path.exists():
        raise click.ClickException("Invalid path")

    metadata = get_metadata(path)
    answer_files = get_task_file_data(path, metadata)

    if not answer_files:
        raise click.ClickException("Invalid task file")

    # Get metadata from the task folder
    if not metadata:
        raise click.ClickException("Invalid metadata")

    t = SubmitData(
        code_files=answer_files,
        code_language=metadata.run_type,
    )

    feedback = submit_task(t)
    click.echo(feedback.console_output())


tim_ide.add_command(task)

if __name__ == "__main__":
    tim_ide()
