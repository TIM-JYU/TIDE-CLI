# TIDE-CLI

## Development
Use following in your local repo:
```
git config core.eol native
git config core.autocrlf true
```

## Usage as python application
Step 1: Clone TIDE-CLI repository https://github.com/TIDE-project/TIDE-CLI

Step 2: Outside JYU network, VPN is required

Step 3: Visit http://webapp04.it.jyu.fi to check it is running

Step 4: Python 3.10 or higher is required

Step 5: Run `pip install poetry` to install poetry

Step 6: Run `poetry shell` to enter virtual environment 

Step 7: Run `poetry install` to install dependencies. If poetry install fails, run first `poetry lock`

Step 8: Go to correct folder: `cd src/tidecli`

Step 9: To run the application, run `python main.py login` to login to the application

Step 10: Login details can be acquired from the TIDE project team vie email

Step 11: Run `python main.py` to see the list of commands available

