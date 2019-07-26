# arrangeit - cross-platform desktop utility for easy windows management
# Copyright (C) 1999-2019 Ivica Paleka

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>

import logging
import os

import pytest

import arrangeit
from arrangeit import __main__, base
from arrangeit.utils import get_component_class, platform_path


class TestStructure(object):
    """Testing class for platform specific subpackages structure."""

    ## BaseApp
    def test_host_platform_App_issubclass_of_BaseApp(self):
        assert issubclass(get_component_class("App"), base.BaseApp)

    ## BaseController
    def test_host_platform_Controller_issubclass_of_BaseController(self):
        assert issubclass(get_component_class("Controller"), base.BaseController)

    ## BaseCollector
    def test_host_platform_Collector_issubclass_of_BaseCollector(self):
        assert issubclass(get_component_class("Collector"), base.BaseCollector)


class TestSetup(object):
    """Testing class for main app initialization and configuration."""

    ## main
    def test_main_calls_logging_basicConfig(self, mocker):
        mocker.patch("arrangeit.__main__.get_component_class")
        mocked = mocker.patch("arrangeit.__main__.logging.basicConfig")
        __main__.main()
        mocked.assert_called_once()
        mocked.assert_called_with(
            format="%(asctime)s - %(message)s", level=logging.INFO
        )

    def test_main_calls_get_component_class_App(self, mocker):
        mocked = mocker.patch("arrangeit.__main__.get_component_class")
        __main__.main()
        mocked.assert_called_once()
        mocked.assert_called_with("App")

    def test_main_initializes_platform_specific_App(self, mocker):
        mocked = mocker.patch("arrangeit.{}.app.App".format(platform_path()))
        __main__.main()
        mocked.assert_called()

    def test_main_calls_App_run(self, mocker):
        mocked = mocker.patch("arrangeit.{}.app.App".format(platform_path()))
        __main__.main()
        assert mocked.return_value.run.call_count == 1


class TestFiles(object):
    """Testing class for program resources files."""

    ## resources
    @pytest.mark.parametrize(
        "asset",
        [
            "resize.png",
            "move.png",
            "restore.png",
            "minimize.png",
            "blank.png",
            "white.png",
            "arrangeit.ico",
            "icon128.png",
            "icon32.png",
        ],
    )
    def test_resources_icon_file_exist(self, asset):
        path = os.path.abspath(
            os.path.join(os.path.dirname(arrangeit.__file__), "resources", asset)
        )
        assert os.path.exists(path)

    @pytest.mark.parametrize("asset", ["logo.png", "COPYRIGHT"])
    def test_resources_misc_file_exist(self, asset):
        path = os.path.abspath(
            os.path.join(os.path.dirname(arrangeit.__file__), "resources", asset)
        )
        assert os.path.exists(path)
