from tidecli.api.routes import get_user_task_by_taskId


def create_task_file(course, task):
    """
    Create a file for a task
    """
    task_id = f"{course}:{task}"
    user_task = get_user_task_by_taskId(task_id=task_id, doc_id=43)
