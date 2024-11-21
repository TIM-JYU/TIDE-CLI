from dataclasses import dataclass
from pathlib import Path

import pytest
from click.testing import CliRunner

from tidecli.main import task

# @pytest.mark.xfailed
def test_create_a_task_external_source():
    # failll
