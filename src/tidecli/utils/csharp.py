import os
from pathlib import Path
import subprocess
import shutil
from tidecli.models.task_data import TideCourseData


def verify_dotnet_installed() -> None:
    """Check if .NET is installed on the system."""
    if shutil.which("dotnet") is None:
        print("Dotnet is not installed. Please install it to use this feature.")
        raise EnvironmentError("Dotnet is not installed.")


def init_dotnet_solution(course_path: Path) -> None:
    """Initialize a .NET solution for the course.
    This function creates a .NET solution file in the specified course path
    """
    verify_dotnet_installed()

    os.chdir(course_path)
    solution_file_path = os.path.join(course_path, course_path.name) + ".sln"

    create_solution_result = subprocess.run(
        ["dotnet", "new", "sln", "-n", course_path.name],
        capture_output=True,
        text=True,
    )

    if create_solution_result.returncode != 0 or not os.path.exists(solution_file_path):
        raise EnvironmentError(
            f"Failed to create solution: {create_solution_result.stderr}"
        )

    print(f"Solution created at {course_path}")


def add_project_to_solution(solution_path: Path, project_path: Path) -> None:
    """Add a .NET project to an existing solution."""
    verify_dotnet_installed()

    add_project_result = subprocess.run(
        ["dotnet", "sln", str(solution_path), "add", str(project_path)],
        capture_output=True,
        text=True,
    )

    if add_project_result.returncode != 0:
        raise EnvironmentError(
            f"Failed to add project to solution: {add_project_result.stderr}"
        )

    print(f"Project {project_path} added to solution {solution_path}")


def init_dotnet_projects(course_data: TideCourseData, course_path: Path) -> None:

    verify_dotnet_installed()

    course_path = course_path.resolve()
    solution_file_path = course_path / (course_path.name + ".sln")
    if not os.path.exists(solution_file_path):
        print(
            f"Solution file {solution_file_path} does not exist. Initializing solution."
        )
        init_dotnet_solution(course_path)

    for course_part in course_data.course_parts.values():
        for task in course_part.tasks.values():
            for supplementary_file in task.supplementary_files:
                if supplementary_file.file_name.endswith(".csproj"):
                    project_file_path = (
                        course_path
                        / task.get_task_directory()
                        / supplementary_file.file_name
                    )
                    add_project_to_solution(solution_file_path, project_file_path)
