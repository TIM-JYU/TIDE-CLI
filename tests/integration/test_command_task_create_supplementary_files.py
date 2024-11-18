
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest
from click.testing import CliRunner
from conftest import tmp_dir_path

from utils import validate_json
from tidecli.main import task

# @pytest.mark.xfailed
def test_create_a_task_external_source():
    # failll
