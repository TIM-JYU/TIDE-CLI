"""Helper for poetry."""

from pathlib import Path
import PyInstaller.__main__

HERE = Path(__file__).parent.absolute()
PATH_TO_MAIN = str(HERE / "main.py")

def install():
    """
    Helper for build binaries.

    Used by poetry.
    """
    PyInstaller.__main__.run([
        PATH_TO_MAIN,
        '--onefile'
        # other pyinstaller options... 
    ])
