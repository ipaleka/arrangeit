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

from arrangeit import base
from arrangeit.settings import Settings


def mocked_setup(mocker):
    mocker.patch("arrangeit.base.get_tkinter_root")
    mocker.patch("arrangeit.base.get_screenshot_widget")
    mocker.patch("arrangeit.base.ViewApplication")


def mocked_setup_root(mocker):
    mocked_setup(mocker)
    return mocker.patch("arrangeit.base.get_tkinter_root")


def mocked_setup_view(mocker):
    mocked_setup(mocker)
    return mocker.patch("arrangeit.base.ViewApplication")


def controller_mocked_app(mocker):
    app = mocker.MagicMock()
    app.grab_window_screen.return_value = (mocker.MagicMock(), (0, 0))
    return base.BaseController(app)


def controller_mocked_key_press(mocker, key):
    event = mocker.MagicMock()
    type(event).keysym = mocker.PropertyMock(return_value=key)
    base.BaseController(mocker.MagicMock()).on_key_pressed(event)


def controller_mocked_for_run(mocker):
    mocked_setup(mocker)
    mocker.patch("arrangeit.base.BaseController.prepare_view")
    mocker.patch("arrangeit.base.BaseController.next")
    return base.BaseController(mocker.MagicMock())


def controller_mocked_for_next(mocker):
    mocked_setup(mocker)
    mocker.patch("arrangeit.base.BaseController.set_screenshot")
    mocker.patch("arrangeit.base.BaseController.set_default_geometry")
    mocker.patch("arrangeit.base.BaseController.place_on_top_left")
    controller = base.BaseController(mocker.MagicMock())
    controller.model = base.WindowModel(workspace=1)
    controller.generator = mocker.MagicMock(side_effect=[0, 1, 2])
    controller.state = Settings.LOCATE
    return controller


def controller_mocked_next(mocker):
    mocked_setup(mocker)
    mocker.patch("arrangeit.base.BaseController.next")
    mocker.patch("arrangeit.base.WindowModel")
    mocker.patch("arrangeit.base.BaseMouse")
    controller = base.BaseController(mocker.MagicMock())
    controller.model = base.WindowModel(rect=(50, 50, 100, 100), workspace=1)
    controller.state = Settings.LOCATE
    return controller


def mocked_for_about_setup(mocker):
    mocker.patch("arrangeit.options.AboutDialog.geometry")
    mocker.patch("arrangeit.options.tk.Toplevel.__init__")
    mocker.patch("arrangeit.options.AboutDialog.title")
    mocker.patch("arrangeit.options.AboutDialog.destroy")
    mocker.patch("arrangeit.options.set_icon")
    mocker.patch("arrangeit.options.tk.Button")
    mocker.patch("arrangeit.options.tk.Label")
    mocker.patch("arrangeit.options.open")
    mocker.patch("arrangeit.options.get_resource_path")
    mocker.patch("arrangeit.options.get_resized_image")
    mocker.patch("arrangeit.options.ttk.Separator")


def mocked_for_about(mocker):
    mocker.patch("arrangeit.options.AboutDialog.setup_widgets")
    mocker.patch("arrangeit.options.AboutDialog.geometry")
    mocker.patch("arrangeit.options.tk.Toplevel.__init__")
    mocker.patch("arrangeit.options.AboutDialog.title")
    mocker.patch("arrangeit.options.AboutDialog.destroy")
    mocker.patch("arrangeit.options.set_icon")


def mocked_for_options(mocker):
    mocker.patch("arrangeit.options.OptionsDialog.setup_widgets")
    mocker.patch("arrangeit.options.OptionsDialog.setup_bindings")
    mocker.patch("arrangeit.options.OptionsDialog.geometry")
    mocker.patch("arrangeit.options.tk.Toplevel.__init__")
    mocker.patch("arrangeit.options.OptionsDialog.title")
    mocker.patch("arrangeit.options.OptionsDialog.destroy")
    mocker.patch("arrangeit.options.set_icon")


def mocked_for_options_setup(mocker, without_section=False, without_files=False):
    if not without_section:
        mocker.patch("arrangeit.options.OptionsDialog.setup_section")
    if not without_files:
        mocker.patch("arrangeit.options.OptionsDialog.setup_files_section")
    mocker.patch("arrangeit.options.OptionsDialog.setup_bindings")
    mocker.patch("arrangeit.options.OptionsDialog.geometry")
    mocker.patch("arrangeit.options.tk.Toplevel.__init__")
    mocker.patch("arrangeit.options.OptionsDialog.title")
    mocker.patch("arrangeit.options.OptionsDialog.destroy")
    mocker.patch("arrangeit.options.ttk.LabelFrame")
    mocker.patch("arrangeit.options.tk.StringVar")
    mocker.patch("arrangeit.options.tk.IntVar")
    mocker.patch("arrangeit.options.tk.Label")
    mocker.patch("arrangeit.options.tk.Button")
    mocker.patch("arrangeit.options.set_icon")
