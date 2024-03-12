import click

from tidecli.api.routes import Routes
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

    Usage:
    [OPTIONS] USERNAME
    """

    click.echo(delete_token())


@tim_ide.command()
def courses():
    """
    Lists user courses.
    """

    click.echo(Routes().get_ide_courses())


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
        click.echo(f"Pulled task {task} for course {course}")
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
