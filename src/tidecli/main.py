import random

import click

from tidecli.models.TimFeedback import TimFeedback
from tidecli.utils.file_saver import create_demo_task
from tidecli.api.routes import Routes
from tidecli.models.Course import Course
from tidecli.models.SubmitData import SubmitData
from tidecli.models.TaskData import TaskData, TaskFile
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

    if not data:
        # TODO: With no courses found, should we print an error message from TIM? 404 in this case
        click.echo("No courses found")
        return

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

    if "error" in data:
        click.echo(data["error"])
        return

    tasks = [TaskData(**task) for task in data]
    for task in tasks:
        click.echo(task.header + ", " + task.ide_task_id)


@tim_ide.command()
@click.argument("ide_task_id", type=str, required=True)
@click.argument("demo_path", type=str, required=True)
def task(ide_task_id, demo_path):
    """
    Tallentaa valitun tehtävän hakemistopolkuun.
    """
    data = Routes().get_task_by_ide_task_id(ide_task_id=ide_task_id, doc_path=demo_path)

    if "error" in data:
        click.echo(data["error"])
        return
        
    td = TaskData(**data)
    # create_demo_task(td) TODO: some error here
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

    if "error" in submit_object:
        click.echo(submit_object["error"])
        return


    validation = TimFeedback(**submit_object.get("result"))

    click.echo(validation.console_output())


if __name__ == "__main__":
    tim_ide()
