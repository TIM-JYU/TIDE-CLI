# Configuration for the TIM /oauth
CLIENT_ID = "oauth2_tide"
BASE_URL = "http://webapp04.it.jyu.fi"
AUTH_ENDPOINT = "/oauth/authorize"
TOKEN_ENDPOINT = "/oauth/token"
PORT = 8083
REDIRECT_URI = f"http://localhost:{PORT}/callback"
SCOPE = "profile user_tasks user_courses"
PROFILE_ENDPOINT = "/oauth/profile"
INTROSPECT_ENDPOINT = "/oauth/introspect"

# Configuration for the TIM /ide endpoints
IDE_COURSES_ENDPOINT = "/ide/ideCourses"
TASK_FOLDERS_BY_DOC_ENDPOINT = "/ide/taskFoldersByDoc"
TASKS_BY_DOC_ENDPOINT = "/ide/tasksByDoc"
TASK_BY_IDE_TASK_ID_ENDPOINT = "/ide/tasksByIdeTaskId"
SUBMIT_TASK_ENDPOINT = "/ide/submitTask"