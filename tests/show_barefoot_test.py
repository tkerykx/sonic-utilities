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


@pytest.mark.usefixtures('config_env')
class TestShowBarefoot(object):
    TEST_CURRENT_PROFILE = ["x1", "x2", "x6", "y1", "y2"]
    TEST_AVAILABLE_PROFILE = ["x1", "x2", "x6", "y1", "y2"]

    # Test 'show platform barefoot'
    def test_summary(self):
        expected_output = """\
            Current profile: {}
            Available profile(s): {}
            """.format(self.TEST_CURRENT_PROFILE, self.TEST_AVAILABLE_PROFILE)

        with mock.patch("sonic_py_common.device_info.get_platform_info",
                return_value={"curr_profile": self.TEST_CURRENT_PROFILE, "avail_profile": self.TEST_AVAILABLE_PROFILE}):
            result = CliRunner().invoke(show.cli.commands["platform"].commands["barefoot"], [])
            assert result.output == textwrap.dedent(expected_output)


class TestShowPlatformPsu(object):
    """
        Note: `show platform barefoot`  Here we test that the utility is called
        with the appropriate option(s). 
    """
    def test_barefoot(self):
        with mock.patch('utilities_common.cli.run_command') as mock_run_command:
            CliRunner().invoke(show.cli.commands['platform'].commands['barefoot'], [])
        assert mock_run_command.call_count == 1
        mock_run_command.assert_called_with('show platform barefoot', display_cmd=False)


