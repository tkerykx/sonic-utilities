import os
import sys
import textwrap
from unittest import mock

import pytest
from click.testing import CliRunner
import show.plugins.barefoot as bf
import show.main as show

@pytest.fixture(scope='class')
def config_env():
    os.environ["UTILITIES_UNIT_TESTING"] = "1"

    yield

    os.environ["UTILITIES_UNIT_TESTING"] = "0"

#class TestConfigPlatformBarefoot(object):
class TestBarefoot(object):
    print("===TK===\n")
    @classmethod
    def setup_class(cls):
        print("SETUP")
        os.environ["UTILITIES_UNIT_TESTING"] = "1"
    
    def test_barefoot(self):
        print("===TK===\n")
        runner = CliRunner()
        #result = runner.invoke(show.cli.commands["chassis"].commands["modules"].commands["status"], [])
        result = runner.invoke(show.cli.commands["platform"].commands["barefoot"], ['profile'])
        
        print(result)
        print(result.output)
        #assert(result.output == show_chassis_modules_output)

    #def test_profile(self):
        #runner = CliRunner()
        #for Azure test
        #expected_output = "Current profile: default\n"
        
        #result = runner.invoke(show.cli.commands['platform'].commands['barefoot'], ['profile'])
        #result = runner.invoke(show.cli.commands['platform'].commands['barefoot'].commands['profile'])
        #result = runner.invoke(bf.barefoot.commands['profile'], [])
        #assert mock_run_command.call_count == 0
        #assert result.exit_code == 2
        #assert result.exit_code == 0
        #print("result.exit_code:", result.exit_code)
        #print("result.output:", result.output)
        #assert result.output == expected_output
        #mock_run_command.assert_called_with('show platform barefoot profile', display_cmd=False)

    def test_barefoot_register(self):
       os.environ["UTILITIES_UNIT_TESTING"] = "1"
       bf.register(show.cli)


