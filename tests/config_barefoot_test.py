import os
import sys
import textwrap
from unittest import mock

import pytest
from click.testing import CliRunner
import config.plugins.barefoot as bf
import config.main as config_main

@pytest.fixture(scope='class')
def config_env():
    os.environ["UTILITIES_UNIT_TESTING"] = "1"

    yield

    os.environ["UTILITIES_UNIT_TESTING"] = "0"

class TestConfigPlatformBarefoot(object):
    @classmethod
    def setup_class(cls):
        print("SETUP")
    
    def test_profile(self):
        runner = CliRunner()
        expected_output = "Swss service will be restarted, continue? [y/N]: \nAborted!\n"
        #result = runner.invoke(show.cli.commands['platform'].commands['barefoot'], ['profile'])
        #result = runner.invoke(show.cli.commands['platform'].commands['barefoot'].commands['profile'])
        result = runner.invoke(bf.barefoot.commands['profile'], ['default'])
        #assert mock_run_command.call_count == 0
        #assert result.exit_code == 2
        #assert result.exit_code == 0
        print("result.exit_code:", result.exit_code)
        print("result.output:", result.output)
        assert result.output == expected_output

        runner = CliRunner()
        expected_output = "Swss service will be restarted, continue? [y/N]: \nAborted!\n"
        result = runner.invoke(bf.barefoot.commands['profile'], ['x1'])
        print("result.exit_code:", result.exit_code)
        print("result.output:", result.output)
        assert result.output == expected_output

        runner = CliRunner()
        expected_output = "Swss service will be restarted, continue? [y/N]: \nAborted!\n"
        result = runner.invoke(bf.barefoot.commands['profile'], ['y2'])
        print("result.exit_code:", result.exit_code)
        print("result.output:", result.output)
        assert result.output == expected_output

        #mock_run_command.assert_called_with('show platform barefoot profile', display_cmd=False)
    
    def test_register(self):
        bf.register(config_main.config)