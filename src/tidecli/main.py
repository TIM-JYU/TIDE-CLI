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
@click.argument("demo_path", type=str, required=True)
def tasks(demo_path):
    """
    Hakee käyttäjän tehtävät valitusta hakemistopolusta.
    """

    click.echo(Routes().get_tasks_by_doc_path(doc_path=demo_path))


@tim_ide.command()
@click.argument("ide_task_id", type=str, required=True)
@click.argument("demo_path", type=str, required=True)
def task(ide_task_id, demo_path):
    print(ide_task_id, demo_path)
    """
    Tallentaa valitun tehtävän hakemistopolkuun.
    """

    click.echo(Routes().get_task_by_ide_task_id(ide_task_id=ide_task_id, doc_path=demo_path))


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
