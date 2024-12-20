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

Step 4: Run `pip install poetry` to install Poetry tool for dependency management and packaging

Step 5: Run `poetry shell` to enter virtual environment

Step 6: Run `poetry install` to install dependencies. If Poetry install fails, run first `poetry lock`

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

## Running unit tests

After cloning and starting the Poetry environment:

Step 1: Navigate to test folder `cd tests`

Step 2: Run unit tests with command `python -m unittest`

## Running integration tests

Step 1: Start up TIM dev server (for instructions on this, see https://github.com/TIM-JYU/TIM)

Step 1.5: Authenticate to TIDE. See [Manual authentication required for running the tests](#manual-authentication-required-for-running-the-tests) section below.

Step 2: Navigate to integration test folder `cd tests/integration`

Step 3: Run `poetry run pytest`. If the TIM instance used for tests is not running in localhost, set the correct address to TIM_DOMAIN environmental variable, e.g. `TIM_DOMAIN=192.168.148.69 poetry run pytest`

### Current state of intergration tests

This section covers the current state of integration tests, and running them.

#### Manual authentication required for running the tests

In the current state, there is no implementation for authenticating TIDE automatically, thus the test user has to authenticate TIDE manually before running the tests.

Step 1: Run `DEV=true poetry run python src/tidecli/main.py login` at the project root.

Step 2: Log in using the test user credentials ("testuser1", "test1pass") and authenticate TIDE.

#### State of tests for the login command

Tide uses webbrowser.open function to show the authentication page to the user.
The problem faced while trying to mock this function was the fact that
webbrowser.open is followed by a code that has to be running while the user
interacts with the browser, thus the mock would have to be non-blocking like
the original function. This proved to be too complex of a problem to tackle.

A solution to the problem of authenticating the user automatically may lie in not mocking the webbrowser.open function and instead getting it to launch Chromium with --remote-debugging-port flag and attaching to it. See [connect over cdp in Playwright documentation](https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect-over-cdp).

#### TIM document IDs and file content comparison

As it currently stands, the TIM document ID is hard-coded into the files inside
the `expected_task_files` directory. However, these hard-coded values do not
(except with extreme luck) match the ones TIM generates for the documents when
they are created for the test session.

Possible solutions to the problem, from the fastest one to implement to the
most solid one.

1. Ignore .timdata during file content comparison
2. Ignore the doc_id inside .timdata during file content comparison
3. Get the document ID dynamically while setting up the test documents
