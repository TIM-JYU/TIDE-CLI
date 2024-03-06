import click

@click.group()
def tim_ide():
    pass


@tim_ide.command()
def login():
    """
    Opens a login link.
    """
    if authenticate():
        click.echo("Login successful.")
    else:
        click.echo("Login failed.")


@tim_ide.command()
def logout():
    """User logout"""
    # Do something
    click.echo("Logout successful.")


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
