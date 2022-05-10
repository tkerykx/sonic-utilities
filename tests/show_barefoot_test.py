import os
import pytest
import subprocess
from click.testing import CliRunner

import show.main as show
from .utils import get_result_and_return_code

class TestShowBarefoot(object):
    def test_show_platform_barefoot_profile(self):
        return_code, result = get_result_and_return_code("show platform bareboot profile")
        assert return_code == 0
