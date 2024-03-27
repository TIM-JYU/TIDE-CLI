"""
Main module for the Tide CLI.

This module contains the main command group for the Tide CLI.
The whole CLI app may be located in different module.
"""
import click
from tidecli.models.TimFeedback import TimFeedback
from tidecli.utils import file_handler
from tidecli.utils.file_handler import create_demo_task
from tidecli.api.routes import Routes
from tidecli.models.Course import Course
from tidecli.models.SubmitData import SubmitData
from tidecli.models.TaskData import TaskData, TaskFile
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


@tim_ide.command()
def logout():
    """Log out the user and deletes the token from the keyring."""
    click.echo(delete_token())


@tim_ide.command()
def courses():
    """List  all courses."""
    data = Routes().get_ide_courses()

    if not data or "error" in data:
        # TODO: With no courses found, should we print an error message from TIM? 404 in this case
        click.echo("No courses found")
        return

    all_courses = [Course(**course) for course in data]
    for course in all_courses:
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
    data = Routes().get_tasks_by_doc(doc_path=demo_path)

    if "error" in data:
        click.echo(data["error"])
        return

    tasks = [TaskData(**task) for task in data]
    for task in tasks:
        click.echo(task.header + ", " + task.ide_task_id)


@task.command()
@click.option("--all", '-a', 'all', is_flag=True, default=False)
@click.argument("demo_path", type=str)
@click.argument("ide_task_id", type=str, default=None)
def create(demo_path, ide_task_id, all):
    """Create all tasks or single if option given."""
    data = None
    if not all:
        data = Routes().get_task_by_ide_task_id(ide_task_id=ide_task_id, doc_path=demo_path)

        # TODO: katso että ttarkistukset toimii kunnolla
        if not data:
            click.echo("No file saved, maybe wrong id?")
            return

        if "error" in data:
            click.echo(data["error"])
            return

        td = TaskData(**data)
        create_demo_task(td, "Ohjelmointi 1", demo_path)
        click.echo(td.header + " was saved")
    else:
        # TODO: luo kaikkien harjoitusten kaikki tehtävät
        data = None


@tim_ide.command()
@click.argument("path", type=str, required=True)
def submit(path):
    """
    Enter the path of the task folder to submit the task to TIM.
    Path must be inserted in the following format: "/path/to/task/folder".
    """

    # Get task file data from the task folder
    code_file = file_handler.get_task_file_data(path)
    # Get metadata from the task folder
    meta_data = file_handler.get_metadata(path)

    t = SubmitData(code_files=TaskFile(content=code_file, path=""),
                   task_id=meta_data["task_id"], doc_id=meta_data["doc_id"],
                   code_language=meta_data["code_language"])

    submit_object = Routes().submit_task(t)

    # TODO: Invalid path error handling

    if "error" in submit_object:
        click.echo(submit_object["error"])
        return

    validation = TimFeedback(**submit_object.get("result"))

    click.echo(validation.console_output())


tim_ide.add_command(task)

if __name__ == "__main__":
    tim_ide()
