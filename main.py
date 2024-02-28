import os

from OauthSinFlask import authenticate, get_ideTasksByBooksmarks

import click
from dotenv import load_dotenv

# test

@click.group()
def cli():
    load_dotenv()


@cli.command()
def login():
    if os.environ.get('OAUTH_TOKEN'):
        click.echo("You are already logged in.")
    else:
        token = authenticate()
        if token:
            with open('.env', 'a') as env_file:
                env_file.write(f'OAUTH_TOKEN={token}\n')
            click.echo("Login successful.")

        else:
            click.echo("Login failed.")


@cli.command()
def login_status():
    click.echo("status")


@cli.command()
def logout():
    if os.environ.get('OAUTH_TOKEN'):
        os.environ['OAUTH_TOKEN'] = ''
        click.echo("Logout successful.")
    else:
        click.echo("You are not logged in.")


@cli.command()
@click.option('--courseID', help='Tasks from course folder')
def tasks():
    login_check()
    get_ideTasksByBooksmarks()


@cli.command()
def courses():
    """
    All courses bookmarked by user
    :return: Dict of courses
    """
    login_check()
    click.echo(get_ideTasksByBooksmarks())


@cli.command()
@click.option('--path', default='/courses', help='Path where courses are saved related to TIDE-app')
def config(path):
    login_check()
    with open('.env', 'a') as env_file:
        env_file.write(f'TIDE_COURSES_PATH={path}\n')


@cli.command()
@click.option('--course', '--tasks_ID', help='Submit answer to task with given ID')
def submit_answer(course, task_ID):
    login_check()
    # TODO: Vastaus tehtävän idllä


def login_check():
    if os.environ.get('OAUTH_TOKEN') == '':
        click.echo("Please login.")
        # TODO: Tokenin voimassaolon tarkistus
        raise click.Abort()  # Abort the command if not logged in


if __name__ == '__main__':
    cli()
