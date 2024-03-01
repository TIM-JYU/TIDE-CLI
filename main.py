import click

@click.group()
def tim_ide():

    pass

@tim_ide.command()
def login():
    """Returns a login link"""
    # Do something
    click.echo("Login link: https://example.org/")


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
    tim_ide list [OPTIONS] [COURSE]

    Options:
    COURSE  Course name (not required)
    """
    # Do something
    if course:
        click.echo(f"Listed tasks for course {course}")
    else:
        click.echo("Listed all courses")


if __name__ == "__main__":
    tim_ide()