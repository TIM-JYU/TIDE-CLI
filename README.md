# TIDE-CLI

## Development
Use following in your local repo:
```
git config core.eol native
git config core.autocrlf true
```

## Usage as python application
Step 1: Clone TIDE-CLI repository https://github.com/TIDE-project/TIDE-CLI

Step 2: Modify src/tidecli/tide_config.py BASE_URL to correspond the TIM-server being used

Step 3: Python 3.10 or higher is required

Step 4: Run `pip install poetry` to install poetry

Step 5: Run `poetry shell` to enter virtual environment 

Step 6: Run `poetry install` to install dependencies. If poetry install fails, run first `poetry lock`

Step 7: Go to correct folder: `cd src/tidecli`

Step 8: To run the application, run `python main.py login` to login to the application

Step 9: Run `python main.py` to see the list of commands available

## Building CLI tool to executable
There may be a need for build the CLI tool into an executable using user's own operating system. If that is the case, please follow these after above steps are completed untill `Step 6`.

**Build the CLI tool**

Step 1: `poetry run build`

Step 2: `cd dist && ls -la`, file permissions should look like `-rwxr-xr-x`

Step 3: Move app named 'main' as 'tide' to some folder that is in PATH. E.g. `mv main /usr/bin/tide`.

Step 4: Start use, please refer user instructions in TIM.
