import os
import sys
import textwrap
import json
from unittest.mock import patch, mock_open

import pytest
from click.testing import CliRunner
import utilities_common.cli as cli

import show.main as show
import config.main as config
import show.plugins.barefoot as bfshow
import config.plugins.barefoot as bfconfig

@pytest.fixture(scope='class')
def config_env():
    os.environ["UTILITIES_UNIT_TESTING"] = "1"
    yield
    os.environ["UTILITIES_UNIT_TESTING"] = "0"

class TestStdout:
    stdout = ""

class TestReturncode:
    returncode = False

class TestShowPlatformBarefoot(object):

    def test_config_barefoot(self):
        runner = CliRunner()
        expected_output = ""
        result = CliRunner().invoke(show.cli.commands["platform"], ["barefoot"])
        assert result.output == expected_output

    def test_config_profile(self):
        runner = CliRunner()
        expected_output = "Swss service will be restarted, continue? [y/N]: \nAborted!\n"
        result = runner.invoke(bfconfig.barefoot.commands['profile'], ['x1'])
        print("result.exit_code:", result.exit_code)
        print("result.output:", result.output)
        assert result.output == expected_output

    def test_check_profile_exist(self):
        ret = TestReturncode()
        ret.returncode = 0
        with patch('show.plugins.barefoot.subprocess.run', return_value=ret):
            result = bfconfig.check_profile_exist("x1", "tofino")
            assert result == True

    def test_show_profile(self):
        runner = CliRunner()
        expected_output = "Current profile: default\n"
        result = runner.invoke(bfshow.barefoot.commands['profile'], [])
        print("result.exit_code:", result.exit_code)
        print("result.output:", result.output)
        assert result.output == expected_output

    def test_get_chip_family1(self):
        with patch('show.plugins.barefoot.device_info.get_path_to_hwsku_dir', return_value=""):
            chip_family = json.dumps({"chip_list": [{"instance": 0,"chip_family": "tofino"}]})
            with patch('show.plugins.barefoot.open', mock_open(read_data=chip_family)):
                result = bfshow.get_chip_family()
                assert result == "tofino"

    def test_get_chip_family2(self):
        with patch('config.plugins.barefoot.device_info.get_path_to_hwsku_dir', return_value=""):
            chip_family = json.dumps({"chip_list": [{"instance": 0,"chip_family": "tofino2"}]})
            with patch('show.plugins.barefoot.open', mock_open(read_data=chip_family)):
                result = bfconfig.get_chip_family()
                assert result == "tofino2"

    def test_get_chip_family3(self):
        with patch('config.plugins.barefoot.device_info.get_path_to_hwsku_dir', return_value=""):
            chip_family = json.dumps({"chip_list": [{"instance": 0,"chip_family": "tofino3"}]})
            with patch('show.plugins.barefoot.open', mock_open(read_data=chip_family)):
                result = bfconfig.get_chip_family()
                assert result == "tofino3"

    def test_show_profile_default(self):
        runner = CliRunner()
        expected_output = "Current profile: default\n"
        with patch("show.plugins.barefoot.check_profile", return_value=1):
            print(show.plugins.barefoot.check_profile())
            result = runner.invoke(bfshow.barefoot.commands['profile'], [])
            print("result.exit_code:", result.exit_code)
            print("result.output:", result.output)
            assert result.output == expected_output

    def test_check_profile1(self):
        ret = TestReturncode()
        ret.returncode = 1
        with patch('show.plugins.barefoot.subprocess.run', return_value=ret):
            result = bfshow.check_profile()
            print(result)
            assert result == True

    def test_check_profile2(self):
        ret = TestReturncode()
        ret.returncode = 1
        with patch('config.plugins.barefoot.subprocess.run', return_value=ret):
            result = bfconfig.check_profile()
            print(result)
            assert result == True

    def test_check_profile3(self):
        ret = TestReturncode()
        ret.returncode = 0
        with patch('show.plugins.barefoot.subprocess.run', return_value=ret):
            result = bfshow.check_profile()
            print(result)
            assert result == False

    def test_check_profile4(self):
        ret = TestReturncode()
        ret.returncode = 0
        with patch('config.plugins.barefoot.subprocess.run', return_value=ret):
            result = bfconfig.check_profile()
            print(result)
            assert result == False

    def test_check_supported_profile1(self):
        result = bfconfig.check_supported_profile("x1", "tofino")
        print(result)
        assert result == True
    
    def test_check_supported_profile2(self):
        result = bfconfig.check_supported_profile("y2", "tofino2")
        print(result)
        assert result == True

    def test_check_supported_profile3(self):
        result = bfconfig.check_supported_profile("x1", "tofino2")
        print(result)
        assert result == False

    def test_check_supported_profile4(self):
        result = bfconfig.check_supported_profile("y2", "tofino")
        print(result)
        assert result == False

    def test_get_current_profile(self):
        profile = TestStdout()
        profile.stdout = "y2"
        with patch('show.plugins.barefoot.subprocess.run', return_value=profile):
            result = bfshow.get_current_profile()
            assert result == "y2"

    def test_get_available_profiles(self):
        profile = TestStdout()
        profile.stdout = "x2"
        with patch('show.plugins.barefoot.subprocess.run', return_value=profile):
            result = bfshow.get_available_profiles("install_x1_tofino")
            assert result == "x2"

    def test_show_profile(self):
        runner = CliRunner()
        expected_output = """\
Current profile: x2
Available profile(s):
x1
x2
y2
y3
"""
        with patch("show.plugins.barefoot.check_profile", return_value=False):
            with patch("show.plugins.barefoot.get_chip_family", return_value="tofino"):
                with patch("show.plugins.barefoot.get_current_profile", return_value="x2\n"):
                    with patch("show.plugins.barefoot.get_available_profiles", return_value="x1\nx2\ny2\ny3\n"):
                        result = runner.invoke(bfshow.barefoot.commands['profile'], [])
                        print("result.exit_code:", result.exit_code)
                        print("result.output:", result.output)
                        assert result.output == expected_output

    def test_show_profile2(self):
        runner = CliRunner()
        expected_output = """\
Current profile: y2
Available profile(s):
x1
x2
y2
y3
"""
        with patch("show.plugins.barefoot.check_profile", return_value=False):
            with patch("show.plugins.barefoot.get_chip_family", return_value="tofino2"):
                with patch("show.plugins.barefoot.get_current_profile", return_value="y2\n"):
                    with patch("show.plugins.barefoot.get_available_profiles", return_value="x1\nx2\ny2\ny3\n"):
                        result = runner.invoke(bfshow.barefoot.commands['profile'], [])
                        print("result.exit_code:", result.exit_code)
                        print("result.output:", result.output)
                        assert result.output == expected_output

    def test_show_profile3(self):
        runner = CliRunner()
        expected_output = """\
Current profile: y2
Available profile(s):
x1
x2
y2
y3
"""
        with patch("show.plugins.barefoot.check_profile", return_value=False):
            with patch("show.plugins.barefoot.get_chip_family", return_value="tofino3"):
                with patch("show.plugins.barefoot.get_current_profile", return_value="y2\n"):
                    with patch("show.plugins.barefoot.get_available_profiles", return_value="x1\nx2\ny2\ny3\n"):
                        result = runner.invoke(bfshow.barefoot.commands['profile'], [])
                        print("result.exit_code:", result.exit_code)
                        print("result.output:", result.output)
                        assert result.output == expected_output