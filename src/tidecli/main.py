import click

from tidecli.api.oauth_login import authenticate
from tidecli.api.routes import Routes
from tidecli.utils.login_handler import login_details
from tidecli.utils.handle_token import delete_token


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
@click.argument("username")
def logout(username):
    """
    Logs out the user and deletes the token from the keyring

    Usage:
    [OPTIONS] USERNAME
    """

    click.echo(delete_token(username))


@tim_ide.command()
@click.argument("course", required=False)
def list(course=None):
    """
    Lists user courses. If course is provided, it will list the course tasks.

    Usage:
    [OPTIONS] [COURSE]

    Options:
    COURSE  Course name (not required)
    """

    if course:
        click.echo(f"Listed tasks for course {course}")
    else:
        click.echo("Listed all courses")


@tim_ide.command()
@click.argument("course")
@click.option("--task", help="Specific task to pull")
def pull(course, task=None):
    """
    Fetches course or task data

    Usage:
    [OPTIONS] COURSE

    Options:
    --task NAME (not required)
    """
    # Do something
    if task:
        click.echo(
            Routes().get_user_task_by_taskId(task_id="Ohjelmointi2:T1", doc_id=43)
        )
    else:
        click.echo(f"Pulled course {course}")


@tim_ide.command()
@click.argument("course")
@click.option("--task", help="Specific task to submit")
def push(course, task=None):
    """
    Submits course or task data

    Usage:
    [OPTIONS] COURSE

    Options:
    --task NAME (not required)
    """
    # Do something
    if task:
        click.echo(f"Pushed task {task} for course {course}")
    else:
        click.echo(f"Pushed course {course}")


if __name__ == "__main__":
    tim_ide()
