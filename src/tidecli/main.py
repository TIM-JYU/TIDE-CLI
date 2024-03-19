import click

from tidecli.api.routes import Routes
from tidecli.models.Course import Course
from tidecli.models.SubmitData import SubmitData
from tidecli.models.TaskData import TaskData
from tidecli.utils.handle_token import delete_token
from tidecli.utils.login_handler import login_details


@click.group()
def tim_ide():
    pass


@tim_ide.command()
def login():
    """
    Opens a login link.
    """
    click.echo(login_details())


@tim_ide.command()
def logout():
    """
    Logs out the user and deletes the token from the keyring
    """
    click.echo(delete_token())


@tim_ide.command()
def courses():
    """
    Lists user courses.
    """
    data = Routes().get_ide_courses()
    all_courses = [Course(**course) for course in data]
    for course in all_courses:
        click.echo(course.pretty_print())


@tim_ide.command()
@click.argument("demo_path", type=str, required=True)
def tasks(demo_path):
    """
    Hakee käyttäjän tehtävät valitusta hakemistopolusta.
    """
    data = Routes().get_tasks_by_doc_path(doc_path=demo_path)
    tasks = [TaskData(**task) for task in data]
    for task in tasks:
        click.echo(task.header)


@tim_ide.command()
@click.argument("ide_task_id", type=str, required=True)
@click.argument("demo_path", type=str, required=True)
def task(ide_task_id, demo_path):
    """
    Tallentaa valitun tehtävän hakemistopolkuun.
    """
    data = Routes().get_task_by_ide_task_id(ide_task_id=ide_task_id, doc_path=demo_path)
    td = TaskData(**data)
    click.echo(td.header + " was saved")  # Just an example


@tim_ide.command()
@click.argument("course", type=str, required=True)
@click.argument("task", type=str, required=True)
def push(course, task):
    """
    Submits course or task data

    Usage:
    [OPTIONS] COURSE

    Options:
    --task NAME (not required)
    """
    t = SubmitData(code_files="print('hello worlds')", path="main.py", task_id="Tehtävä1", doc_id=60)
    click.echo(Routes().submit_task(t))

    # TODO: Response handling


if __name__ == "__main__":
    tim_ide()
