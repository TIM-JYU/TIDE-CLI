"""
Main module for the Tide CLI.

This module contains the main command group for the Tide CLI.
The whole CLI app may be located in different module.
"""
import random

import click

from tidecli.utils.file_saver import create_demo_task
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
    all_courses = [Course(**course) for course in data]
    for course in all_courses:
        click.echo(course.pretty_print())


@click.group()
def task():
    """Task related commands

    It is possible to list and create all tasks per excercise or just
    create one task.

    """
    # TODO: printtaa esim. aiemmin noudetut taskit tms järkevää. Tai sitten ole printtaamatta
    pass


@task.command()
@click.argument("demo_path", type=str, required=True)
def list(demo_path):
    """Fetch tasks by doc path."""
    data = Routes().get_tasks_by_doc_path(doc_path=demo_path)
    tasks = [TaskData(**task) for task in data]
    for task in tasks:
        click.echo(task.header + ", " + task.ide_task_id)


@task.command()
@click.option("--all", '-a', is_flag=True, default=False)
@click.argument("demo_path", type=str, required=True)
@click.argument("ide_task_id", type=str, required=False, default=None)
def create(ide_task_id, demo_path, all):
    """Create all tasks or single if option given."""
    data = None
    if not all:
        data = Routes().get_task_by_ide_task_id(ide_task_id=ide_task_id, doc_path=demo_path)
        td = TaskData(**data)
        create_demo_task(td)
        click.echo(td.header + " was saved")
    else:
        # TODO: luo kaikkien harjoitusten kaikki tehtävät
        data = None

    if not data:
        click.echo("No file saved, maybe wrong id?")
        return


@tim_ide.command()
@click.argument("course", type=str, required=True)
@click.argument("task", type=str, required=True)
def push(course, task):
    """
    Submit course or task data.

    Usage:
    [OPTIONS] COURSE

    Options:
    --task NAME (not required)
    """
    rand = random.randint(0, 10000)  # Just an example for generating different asnwers

    code_file = TaskFile(content=f"print('hello worlds! x {rand}')", path="main.py")  # TaskFile for single file
    code_files = [TaskFile(content="#include <stdio.h>\n#include \"add.h\"\n\nint main() {\nprintf(\"%d\", add(1, 2));\nreturn 1;\n}\n", path="main.cc"),
                  TaskFile(content="int add(int a, int b) {\nreturn 0;\n}\n", path="add.cc"),
                  TaskFile(content="int add(int a, int b);", path="add.h")]

    t = SubmitData(code_files=code_file, task_id="pythontesti", doc_id=60,
                   code_language="py")  # Submitdata for single file

    t2 = SubmitData(code_files=code_files, task_id="Tehtava3", doc_id=60, code_language="cc")

    submit_object = Routes().submit_task(t)

    # submit_object = Routes().submit_task(t2)

    click.echo(submit_object.console_output())


tim_ide.add_command(task)

if __name__ == "__main__":
    tim_ide()
