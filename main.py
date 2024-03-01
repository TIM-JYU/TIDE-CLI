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


if __name__ == "__main__":
    tim_ide()