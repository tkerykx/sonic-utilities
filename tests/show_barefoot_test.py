import os
import sys
import textwrap
from unittest import mock

import pytest
from click.testing import CliRunner

test_path = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.dirname(test_path)
sys.path.insert(0, modules_path)
import show.main as show


@pytest.fixture(scope='class')
def config_env():
    os.environ["UTILITIES_UNIT_TESTING"] = "1"

    yield

    os.environ["UTILITIES_UNIT_TESTING"] = "0"

class TestShowPlatformBarefoot(object):
    """
        Note: `show platform barefoot`  Here we test that the utility is called
        with the appropriate option(s). 
    """
    def test_barefoot(self):
        with mock.patch('utilities_common.cli.run_command') as mock_run_command:
            CliRunner().invoke(show.cli.commands['platform'].commands['barefoot'].commands['profile'], [])
        assert mock_run_command.call_count == 1
        mock_run_command.assert_called_with('show platform barefoot', display_cmd=False)
