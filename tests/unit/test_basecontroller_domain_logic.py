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

import pytest

from arrangeit import base
from arrangeit.settings import MESSAGES, Settings
from arrangeit.utils import Rectangle

from .fixtures import ROOT_SNAPPING_RECTANGLES_SOURCES
from .mock_helpers import (
    controller_mocked_app,
    controller_mocked_for_next,
    controller_mocked_for_run,
    controller_mocked_next,
    mocked_setup,
    mocked_setup_view,
)


class TestBaseControllerDomainLogic:
    """Testing class for base Controller class' domain logic methods."""

    ## BaseController.apply_snapping
    def test_BaseController_apply_snapping_calls_move_cursor_for_RESIZE(self, mocker):
        mocked_setup(mocker)
        mocked_check = mocker.patch(
            "arrangeit.base.BaseController.check_snapping_state"
        )
        mocked = mocker.patch("arrangeit.base.BaseMouse.move_cursor")
        controller = controller_mocked_app(mocker)
        controller.state = Settings.RESIZE
        NEW_X, NEW_Y = 101, 202
        controller.apply_snapping(NEW_X, NEW_Y, [], [])
        mocked.assert_called_once()
        mocked.assert_called_with(NEW_X, NEW_Y)
        mocked_check.assert_not_called()

    def test_BaseController_apply_snapping_calls_check_snapping_state(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseMouse.move_cursor")
        mocker.patch("arrangeit.base.BaseController.setup_corner")
        mocked = mocker.patch("arrangeit.base.BaseController.check_snapping_state")
        controller = controller_mocked_app(mocker)
        controller.state = Settings.LOCATE
        SOURCES, INTERSECTIONS = 401, 502
        controller.apply_snapping(1, 1, SOURCES, INTERSECTIONS)
        mocked.assert_called_once()
        mocked.assert_called_with(SOURCES, INTERSECTIONS)

    def test_BaseController_apply_snapping_not_calling_setup_corner(self, mocker):
        mocked_setup(mocker)
        mocker.patch(
            "arrangeit.base.BaseController.check_snapping_state", return_value=None
        )
        mocked_move = mocker.patch("arrangeit.base.BaseMouse.move_cursor")
        mocked = mocker.patch("arrangeit.base.BaseController.setup_corner")
        controller = controller_mocked_app(mocker)
        controller.state = Settings.LOCATE
        controller.apply_snapping(1, 1, 402, 503)
        mocked.assert_not_called()
        mocked_move.assert_called_once()

    def test_BaseController_apply_snapping_changes_state(self, mocker):
        mocked_setup(mocker)
        STATE = 3
        mocker.patch(
            "arrangeit.base.BaseController.check_snapping_state", return_value=STATE
        )
        mocker.patch("arrangeit.base.BaseMouse.move_cursor")
        mocker.patch("arrangeit.base.BaseController.setup_corner")
        controller = controller_mocked_app(mocker)
        controller.state = Settings.LOCATE
        controller.apply_snapping(1, 1, 403, 504)
        assert controller.state == STATE

    def test_BaseController_apply_snapping_calls_setup_corner(self, mocker):
        mocked_setup(mocker)
        mocker.patch(
            "arrangeit.base.BaseController.check_snapping_state", return_value=1
        )
        mocked_move = mocker.patch("arrangeit.base.BaseMouse.move_cursor")
        mocked = mocker.patch("arrangeit.base.BaseController.setup_corner")
        controller = controller_mocked_app(mocker)
        controller.state = Settings.LOCATE
        controller.apply_snapping(1, 1, 402, 503)
        mocked.assert_called_once()
        mocked.assert_called_with()
        mocked_move.assert_called_once()

    @pytest.mark.parametrize(
        "new_state,state,added_x,added_y",
        [
            (1, 0, 1, 0),
            (2, 0, 1, 1),
            (1, 3, 1, -1),
            (2, 3, 1, 0),
            (0, 1, -1, 0),
            (3, 1, -1, 1),
            (0, 2, -1, -1),
            (3, 2, -1, 0),
            (2, 0, 1, 1),
            (3, 0, 0, 1),
            (2, 1, 0, 1),
            (3, 1, -1, 1),
            (0, 2, -1, -1),
            (1, 2, 0, -1),
            (0, 3, 0, -1),
            (1, 3, 1, -1),
        ],
    )
    def test_BaseController_apply_snapping_changes_move_cursor_call(
        self, mocker, new_state, state, added_x, added_y
    ):
        view = mocked_setup_view(mocker)
        WIDHEI = 800
        view.return_value.master.winfo_width.return_value = WIDHEI
        view.return_value.master.winfo_height.return_value = WIDHEI
        mocked_corner = mocker.patch("arrangeit.base.BaseController.setup_corner")
        mocked = mocker.patch("arrangeit.base.BaseMouse.move_cursor")
        mocker.patch(
            "arrangeit.base.BaseController.check_snapping_state", return_value=new_state
        )
        controller = controller_mocked_app(mocker)
        controller.state = state
        NEW_X, NEW_Y = 505, 506
        INTERSECTIONS = (
            (
                ROOT_SNAPPING_RECTANGLES_SOURCES[
                    Settings.CORNER_RECT_INDEXES[new_state][0]
                ],
                Rectangle(420, 295, 1050, 299),
            ),
            (
                ROOT_SNAPPING_RECTANGLES_SOURCES[
                    Settings.CORNER_RECT_INDEXES[new_state][1]
                ],
                Rectangle(1278, 25, 1282, 1082),
            ),
        )
        controller.apply_snapping(
            NEW_X, NEW_Y, ROOT_SNAPPING_RECTANGLES_SOURCES, INTERSECTIONS
        )
        assert controller.state == new_state
        mocked_corner.assert_called_once()
        NEW_X += added_x * (WIDHEI - 2 * Settings.SHIFT_CURSOR)
        NEW_Y += added_y * (WIDHEI - 2 * Settings.SHIFT_CURSOR)
        mocked.assert_called_once()
        mocked.assert_called_with(NEW_X, NEW_Y)

    ## BaseController.check_snapping
    def test_BaseController_check_snapping_snapping_is_on_false(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.offset_for_intersections")
        controller = controller_mocked_app(mocker)
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        type(mocked_settings).SNAPPING_IS_ON = mocker.PropertyMock(return_value=False)
        returned = controller.check_snapping(100, 100)
        mocked.assert_not_called()
        assert returned is False

    def test_BaseController_check_snapping_calls_get_root_rect(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseMouse")
        mocker.patch("arrangeit.base.check_intersections")
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        type(mocked_settings).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        type(mocked_settings).LOCATE = mocker.PropertyMock(return_value=0)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        type(mocked_settings).SNAP_PIXELS = mocker.PropertyMock(return_value=10)
        mocker.patch("arrangeit.base.BaseController.apply_snapping")
        mocked = mocker.patch("arrangeit.base.BaseController.get_root_rect")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        view.return_value.workspaces.active = 1001
        controller.snapping_targets = {1001: ["foo"]}
        controller.state = Settings.LOCATE
        controller.check_snapping(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(x, y)

    def test_BaseController_check_snapping_calls_get_snapping_sources_for_locate(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseMouse")
        mocker.patch("arrangeit.base.check_intersections")
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        type(mocked_settings).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        type(mocked_settings).LOCATE = mocker.PropertyMock(return_value=0)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        SNAP = 4
        type(mocked_settings).SNAP_PIXELS = mocker.PropertyMock(return_value=SNAP)
        mocker.patch("arrangeit.base.BaseController.apply_snapping")
        mocked_rect = mocker.patch("arrangeit.base.BaseController.get_root_rect")
        mocked = mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        view.return_value.workspaces.active = 1001
        controller.snapping_targets = {1001: ["foo"]}
        controller.state = Settings.LOCATE
        controller.check_snapping(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_rect.return_value, SNAP, corner=None)

    def test_BaseController_check_snapping_calls_get_snapping_sources_for_resize(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseMouse")
        mocker.patch("arrangeit.base.check_intersections")
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        type(mocked_settings).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        type(mocked_settings).LOCATE = mocker.PropertyMock(return_value=0)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        SNAP = 4
        type(mocked_settings).SNAP_PIXELS = mocker.PropertyMock(return_value=SNAP)
        mocker.patch("arrangeit.base.BaseController.apply_snapping")
        mocked_rect = mocker.patch("arrangeit.base.BaseController.get_root_rect")
        mocked = mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        view.return_value.workspaces.active = 1001
        controller.snapping_targets = {1001: ["foo"]}
        controller.state = Settings.RESIZE
        controller.check_snapping(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(
            mocked_rect.return_value, SNAP, corner=controller.state % 10
        )

    def test_BaseController_check_snapping_calls_check_intersection(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseMouse")
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        type(mocked_settings).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        type(mocked_settings).LOCATE = mocker.PropertyMock(return_value=0)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        SNAP = 4
        type(mocked_settings).SNAP_PIXELS = mocker.PropertyMock(return_value=SNAP)
        mocker.patch("arrangeit.base.BaseController.apply_snapping")
        root_rects = mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        mocked = mocker.patch("arrangeit.base.check_intersections")
        view.return_value.workspaces.active = 1001
        controller = controller_mocked_app(mocker)
        SAMPLE = ["foo"]
        controller.snapping_targets = {1001: SAMPLE}
        controller.state = Settings.LOCATE
        controller.check_snapping(100, 100)
        mocked.assert_called_once()
        mocked.assert_called_with(root_rects.return_value, SAMPLE)

    def test_BaseController_check_snapping_calls_offset_for_intersections(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseMouse")
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        type(mocked_settings).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        type(mocked_settings).LOCATE = mocker.PropertyMock(return_value=0)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        SNAP = 4
        type(mocked_settings).SNAP_PIXELS = mocker.PropertyMock(return_value=SNAP)
        mocker.patch("arrangeit.base.BaseController.apply_snapping")
        mocked_check = mocker.patch("arrangeit.base.check_intersections")
        mocked = mocker.patch("arrangeit.base.offset_for_intersections")
        view.return_value.workspaces.active = 1001
        controller = controller_mocked_app(mocker)
        SAMPLE = ["foo"]
        controller.snapping_targets = {1001: SAMPLE}
        controller.state = Settings.LOCATE
        controller.check_snapping(100, 100)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_check.return_value, SNAP)

    def test_BaseController_check_snapping_calls_apply_snapping(self, mocker):
        view = mocked_setup_view(mocker)
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        type(mocked_settings).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        type(mocked_settings).LOCATE = mocker.PropertyMock(return_value=0)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        SNAP = 4
        type(mocked_settings).SNAP_PIXELS = mocker.PropertyMock(return_value=SNAP)
        mocked_sources = mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        mocked_intersections = mocker.patch("arrangeit.base.check_intersections")
        offset = (10, 12)
        mocker.patch("arrangeit.base.offset_for_intersections", return_value=offset)
        mocker.patch("arrangeit.base.BaseMouse.move_cursor")
        mocked = mocker.patch("arrangeit.base.BaseController.apply_snapping")
        view.return_value.workspaces.active = 1001
        controller = controller_mocked_app(mocker)
        SAMPLE = ["foo"]
        controller.snapping_targets = {1001: SAMPLE}
        controller.state = Settings.LOCATE
        x, y = 204, 207
        returned = controller.check_snapping(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(
            x + offset[0],
            y + offset[1],
            mocked_sources.return_value,
            mocked_intersections.return_value,
        )
        assert returned is True

    def test_BaseController_check_snapping_not_calling_apply_snapping(self, mocker):
        view = mocked_setup_view(mocker)
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        type(mocked_settings).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        type(mocked_settings).LOCATE = mocker.PropertyMock(return_value=0)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        SNAP = 4
        type(mocked_settings).SNAP_PIXELS = mocker.PropertyMock(return_value=SNAP)
        mocker.patch("arrangeit.base.check_intersections")
        offset = (0, 0)
        mocker.patch("arrangeit.base.offset_for_intersections", return_value=offset)
        mocked = mocker.patch("arrangeit.base.BaseMouse.move_cursor")
        mocked_check = mocker.patch("arrangeit.base.BaseController.apply_snapping")
        view.return_value.workspaces.active = 1001
        controller = controller_mocked_app(mocker)
        SAMPLE = ["foo"]
        controller.snapping_targets = {1001: SAMPLE}
        controller.state = Settings.LOCATE
        x, y = 204, 207
        returned = controller.check_snapping(x, y)
        mocked.assert_not_called()
        mocked_check.assert_not_called()
        assert returned is False

    ## BaseController.check_snapping_state
    def test_BaseController_check_snapping_state_returns_state_for_single_axis_snapping(
        self, mocker
    ):
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        STATE = Settings.LOCATE
        controller.state = STATE
        INTERSECTIONS = (
            ROOT_SNAPPING_RECTANGLES_SOURCES[1],
            Rectangle(1278, 25, 1282, 1082),
        )
        returned = controller.check_snapping_state(
            ROOT_SNAPPING_RECTANGLES_SOURCES, INTERSECTIONS
        )
        assert returned is not None

    def test_BaseController_check_snapping_state_returns_None_for_single_axis_snapping(
        self, mocker
    ):
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        STATE = Settings.LOCATE
        controller.state = STATE
        INTERSECTIONS = (
            ROOT_SNAPPING_RECTANGLES_SOURCES[0],
            Rectangle(420, 295, 1050, 299),
        )
        returned = controller.check_snapping_state(
            ROOT_SNAPPING_RECTANGLES_SOURCES, INTERSECTIONS
        )
        assert returned is None

    def test_BaseController_check_snapping_state_returns_state_for_both_axes_snapping(
        self, mocker
    ):
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        STATE = Settings.LOCATE
        controller.state = STATE
        INTERSECTIONS = (
            (ROOT_SNAPPING_RECTANGLES_SOURCES[0], Rectangle(420, 295, 1050, 299)),
            (ROOT_SNAPPING_RECTANGLES_SOURCES[1], Rectangle(1278, 25, 1282, 1082)),
        )
        returned = controller.check_snapping_state(
            ROOT_SNAPPING_RECTANGLES_SOURCES, INTERSECTIONS
        )
        assert returned is not None

    def test_BaseController_check_snapping_state_returns_None_for_both_axes_snapping(
        self, mocker
    ):
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        STATE = Settings.LOCATE + 1
        controller.state = STATE
        INTERSECTIONS = (
            (ROOT_SNAPPING_RECTANGLES_SOURCES[0], Rectangle(420, 295, 1050, 299)),
            (ROOT_SNAPPING_RECTANGLES_SOURCES[1], Rectangle(1278, 25, 1282, 1082)),
        )
        returned = controller.check_snapping_state(
            ROOT_SNAPPING_RECTANGLES_SOURCES, INTERSECTIONS
        )
        assert returned is None

    ## BaseController.listed_window_activated
    def test_BaseController_listed_window_activated_calls_task_rerun_from_window(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        SAMPLE1, SAMPLE2 = 91405, 90102
        controller.model.wid = SAMPLE2
        controller.listed_window_activated(SAMPLE1)
        controller.app.run_task.assert_called_with(
            "rerun_from_window", SAMPLE1, SAMPLE2
        )

    def test_BaseController_listed_window_activated_calls_windows_clear_list(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseController.display_message")
        controller = controller_mocked_next(mocker)
        controller.listed_window_activated(90192)
        assert controller.view.windows.clear_list.call_count == 1

    def test_BaseController_listed_window_activated_calls_windowslist_add_windows(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocker.patch("arrangeit.base.BaseController.next")
        windows_list = [0, 1, 2]
        controller = base.BaseController(mocker.MagicMock())
        controller.app.collector.collection.get_windows_list.return_value = windows_list
        controller.listed_window_activated(90108)
        view.return_value.windows.add_windows.assert_called_once()
        view.return_value.windows.add_windows.assert_called_with(windows_list[1:])

    def test_BaseController_listed_window_activated_calls_recapture_mouse_for_OTHER(
        self, mocker
    ):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocker.patch("arrangeit.base.BaseController.next")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.OTHER
        controller.listed_window_activated(90103)
        mocked.assert_called_once()

    @pytest.mark.parametrize("state", [Settings.LOCATE, Settings.RESIZE])
    def test_BaseController_listed_window_activated_not_calling_recapture_not_OTHER(
        self, mocker, state
    ):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocker.patch("arrangeit.base.BaseController.next")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = state
        controller.listed_window_activated(90104)
        mocked.assert_not_called()

    def test_BaseController_listed_window_activated_initializes_generator(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(mocker.MagicMock())
        controller.listed_window_activated(90147)
        controller.app.collector.collection.generator.assert_called()

    def test_BaseController_listed_window_activated_sets_generator_attr(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(mocker.MagicMock())
        controller.listed_window_activated(90152)
        assert (
            controller.generator
            == controller.app.collector.collection.generator.return_value
        )

    def test_BaseController_listed_window_activated_calls_next(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(mocker.MagicMock())
        controller.listed_window_activated(90423)
        mocked.assert_called_once()
        mocked.assert_called_with(
            first_time=True, from_workspace=controller.model.workspace
        )

    def test_BaseController_listed_window_activated_calls_display_message(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.next")
        mocked = mocker.patch("arrangeit.base.BaseController.display_message")
        controller = base.BaseController(mocker.MagicMock())
        controller.listed_window_activated(90424)
        mocked.assert_called_once()
        mocked.assert_called_with(MESSAGES["msg_listed_window"])

    ## BaseController.next
    def test_BaseController_next_sets_state_attr_to_positioning_corner_0(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.state == None
        controller.next()
        assert controller.state == Settings.LOCATE

    def test_BaseController_next_runs_generator(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.next(True)
        controller.generator.__next__.assert_called_once()

    def test_BaseController_next_calls_save_on_StopIteration(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.generator.__next__.side_effect = StopIteration()
        mocker.patch("arrangeit.base.BaseController.shutdown")
        mocked = mocker.patch("arrangeit.base.BaseController.save")
        mocked_setting = mocker.patch("arrangeit.base.Settings")
        type(mocked_setting).SAVE_ON_EXIT = mocker.PropertyMock(return_value=True)
        controller.next()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_BaseController_next_not_calling_save_on_StopIteration(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.generator.__next__.side_effect = StopIteration()
        mocker.patch("arrangeit.base.BaseController.shutdown")
        mocked = mocker.patch("arrangeit.base.BaseController.save")
        mocked_setting = mocker.patch("arrangeit.base.Settings")
        type(mocked_setting).SAVE_ON_EXIT = mocker.PropertyMock(return_value=False)
        controller.next()
        mocked.assert_not_called()

    def test_BaseController_next_calls_shutdown_on_StopIteration(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.generator.__next__.side_effect = StopIteration()
        mocked = mocker.patch("arrangeit.base.BaseController.shutdown")
        controller.next()
        mocked.assert_called_once()

    def test_BaseController_next_returns_True_on_StopIteration(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.generator.__next__.side_effect = StopIteration()
        mocker.patch("arrangeit.base.BaseController.shutdown")
        returned = controller.next()
        assert returned

    def test_BaseController_next_calls_remove_listed_window(self, mocker):
        controller = controller_mocked_for_next(mocker)
        SAMPLE = 4800
        controller.generator.__next__.return_value = base.WindowModel(wid=SAMPLE)
        mocked = mocker.patch("arrangeit.base.BaseController.remove_listed_window")
        mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.next()
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    def test_BaseController_next_not_calling_remove_listed(self, mocker):
        controller = controller_mocked_for_next(mocker)
        mocked_lw = mocker.patch("arrangeit.base.BaseController.remove_listed_window")
        mocked_ws = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.next(True)
        mocked_lw.assert_not_called()
        mocked_ws.assert_not_called()

    def test_BaseController_next_calls_switch_workspace_not_first_time(self, mocker):
        controller = controller_mocked_for_next(mocker)
        mocker.patch("arrangeit.base.BaseController.remove_listed_window")
        mocked = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.next()
        mocked.assert_called_once()

    def test_BaseController_next_calls_switch_workspace_from_workspace(self, mocker):
        controller = controller_mocked_for_next(mocker)
        mocker.patch("arrangeit.base.BaseController.remove_listed_window")
        mocked = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.next(first_time=True, from_workspace=1)
        mocked.assert_called_once()

    def test_BaseController_next_not_calling_switch_workspace_first_time(self, mocker):
        controller = controller_mocked_for_next(mocker)
        mocked_ws = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.next(first_time=True)
        mocked_ws.assert_not_called()

    def test_BaseController_next_not_calling_switch_workspace_same_workspace(
        self, mocker
    ):
        controller = controller_mocked_for_next(mocker)
        mocked_lw = mocker.patch("arrangeit.base.BaseController.remove_listed_window")
        mocked_ws = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.generator.__next__.return_value = base.WindowModel(workspace=1)
        controller.next()
        mocked_lw.assert_called()
        mocked_ws.assert_not_called()

    def test_BaseController_next_not_calling_switch_workspace_from_workspace(
        self, mocker
    ):
        controller = controller_mocked_for_next(mocker)
        mocker.patch("arrangeit.base.BaseController.remove_listed_window")
        mocked_ws = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.generator.__next__.return_value = base.WindowModel(
            workspace=1, rect=(0, 0, 100, 100)
        )
        controller.next(first_time=True, from_workspace=1)
        mocked_ws.assert_not_called()

    def test_BaseController_next_calls_set_screenshot(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.screenshot_when_exposed = False
        mocked = mocker.patch("arrangeit.base.BaseController.set_screenshot")
        controller.next(True)
        mocked.assert_called_once()

    def test_BaseController_next_not_calling_set_screenshot(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.screenshot_when_exposed = True
        mocked = mocker.patch("arrangeit.base.BaseController.set_screenshot")
        controller.next(True)
        mocked.assert_not_called()

    def test_BaseController_next_calls_create_snapping_sources(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.next(True)
        controller.app.create_snapping_sources.assert_called_once()
        controller.app.create_snapping_sources.assert_called_with(controller.model)

    def test_BaseController_next_sets_snapping_targets_attribute(self, mocker):
        controller = controller_mocked_for_next(mocker)
        SAMPLE = {1: []}
        controller.app.create_snapping_sources.return_value = SAMPLE
        controller.next(True)
        assert controller.snapping_targets == SAMPLE

    def test_BaseController_next_calls_set_default_geometry(self, mocker):
        controller = controller_mocked_for_next(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        controller.next(True)
        mocked.assert_called_once()
        mocked.assert_called_with(controller.view.master)

    def test_BaseController_next_calls_update_widgets(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.next(True)
        controller.view.update_widgets.assert_called_once()
        controller.view.update_widgets.assert_called_with(controller.model)

    def test_BaseController_next_calls_place_on_top_left(self, mocker):
        controller = controller_mocked_for_next(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        controller.next(True)
        mocked.assert_called_once()

    def test_BaseController_next_calls_get_root_rect_for_first_time_True(self, mocker):
        controller = controller_mocked_for_next(mocker)
        x, y = 120, 130
        controller.generator.__next__.return_value = base.WindowModel(
            rect=(x, y, 100, 100)
        )
        mocked = mocker.patch(
            "arrangeit.base.BaseController.get_root_rect", return_value=(0, 0, 100, 100)
        )
        controller.next(True)
        mocked.assert_called_once()
        mocked.assert_called_with(x + Settings.SHIFT_CURSOR, y + Settings.SHIFT_CURSOR)

    def test_BaseController_next_calls_root_geometry_for_first_time_True(self, mocker):
        controller = controller_mocked_for_next(mocker)
        x, y = 220, 230
        controller.generator.__next__.return_value = base.WindowModel(
            rect=(0, 0, 100, 100)
        )
        mocker.patch(
            "arrangeit.base.BaseController.get_root_rect", return_value=(x, y, 100, 100)
        )
        controller.next(True)
        controller.view.master.geometry.assert_called_once()
        controller.view.master.geometry.assert_called_with("+{}+{}".format(x, y))

    def test_BaseController_next_not_calling_root_geometry_for_first_time_False(
        self, mocker
    ):
        controller = controller_mocked_for_next(mocker)
        controller.generator.__next__.return_value = base.WindowModel(
            rect=(0, 0, 100, 100)
        )
        mocker.patch(
            "arrangeit.base.BaseController.get_root_rect", return_value=(0, 0, 100, 100)
        )
        controller.next(False)
        controller.view.master.geometry.assert_not_called()

    def test_BaseController_next_returns_False(self, mocker):
        controller = controller_mocked_for_next(mocker)
        returned = controller.next(True)
        assert not returned

    ## BaseController.run
    def test_BaseController_run_calls_prepare_view(self, mocker):
        controller = controller_mocked_for_run(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.prepare_view")
        controller.run(mocker.MagicMock())
        mocked.assert_called_once()

    def test_BaseController_run_sets_generator_attr_from_provided_attr(self, mocker):
        generator = mocker.MagicMock()
        controller = controller_mocked_for_run(mocker)
        controller.run(generator)
        assert controller.generator == generator

    def test_BaseController_run_calls_next(self, mocker):
        controller = controller_mocked_for_run(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller.run(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with(first_time=True)

    def test_BaseController_run_calls_mouse_start(self, mocker):
        controller = controller_mocked_for_run(mocker)
        mocked = mocker.patch("arrangeit.base.BaseMouse.start")
        controller.run(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_BaseController_run_calls_view_startup(self, mocker):
        controller = controller_mocked_for_run(mocker)
        controller.run(mocker.MagicMock())
        controller.view.startup.assert_called_once()
        controller.view.startup.assert_called_with()

    def test_BaseController_run_calls_display_message(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseController.display_message")
        controller = controller_mocked_for_run(mocker)
        controller.run(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with(MESSAGES["msg_release_mouse"], permanent=True)

    def test_BaseController_run_calls_activate_root_task(self, mocker):
        controller = controller_mocked_for_run(mocker)
        controller.run(mocker.MagicMock())
        controller.app.run_task.assert_called_once()
        controller.app.run_task.assert_called_with(
            "activate_root", controller.view.get_root_wid.return_value
        )

    def test_BaseController_run_calls_mainloop(self, mocker):
        controller = controller_mocked_for_run(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.mainloop")
        controller.run(mocker.MagicMock())
        mocked.assert_called_once()

    ## BaseController.update
    def test_BaseController_update_calls_display_message_for_LOCATE(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.update_positioning")
        mocked = mocker.patch("arrangeit.base.BaseController.display_message")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.LOCATE
        controller.update(420, 520)
        mocked.assert_called_once()
        mocked.assert_called_with(MESSAGES["msg_finished_positioning"])

    def test_BaseController_update_calls_update_positioning_for_LOCATE(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocked = mocker.patch("arrangeit.base.BaseController.update_positioning")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.LOCATE
        x, y = 400, 500
        controller.update(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(x, y)

    def test_BaseController_update_calls_display_message_for_RESIZE(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.update_resizing")
        mocked = mocker.patch("arrangeit.base.BaseController.display_message")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.RESIZE
        controller.update(540, 640)
        mocked.assert_called_once()
        mocked.assert_called_with(MESSAGES["msg_finished_resizing"])

    def test_BaseController_update_calls_update_resizing_for_RESIZE(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocked = mocker.patch("arrangeit.base.BaseController.update_resizing")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.RESIZE
        x, y = 500, 600
        controller.update(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(x, y)

    @pytest.mark.parametrize("state", [Settings.OTHER, 150, 5000])
    def test_BaseController_update_not_calling_update_methods_for_other_states(
        self, mocker, state
    ):
        mocked_setup(mocker)
        update1 = mocker.patch("arrangeit.base.BaseController.update_positioning")
        update2 = mocker.patch("arrangeit.base.BaseController.update_resizing")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = state
        controller.update(100, 100)
        update1.assert_not_called()
        update2.assert_not_called()

    ## BaseController.update_positioning
    @pytest.mark.parametrize(
        "state,sign_x,sign_y", [(0, -1, -1), (1, 1, -1), (2, 1, 1), (3, -1, 1)]
    )
    def test_BaseController_update_positioning_calls_set_changed(
        self, mocker, state, sign_x, sign_y
    ):
        controller = controller_mocked_next(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_opposite_corner")
        x, y = 440, 441
        controller.state = state
        mocked_setting = mocker.patch("arrangeit.base.Settings")
        SHIFT = 10
        type(mocked_setting).SHIFT_CURSOR = mocker.PropertyMock(return_value=SHIFT)
        controller.update_positioning(x, y)
        controller.model.set_changed.assert_called_with(
            x=x + sign_x * SHIFT, y=y + sign_y * SHIFT
        )

    def test_BaseController_update_positioning_calls_run_task_move_window_not_resizable(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        SAMPLE = 2002
        controller.model.resizable = False
        controller.model.wid = SAMPLE
        controller.model.changed = (200, 200)
        controller.update_positioning(101, 202)
        controller.app.run_task.assert_called_with("move", SAMPLE)

    def test_BaseController_update_positioning_calls_run_task_move_w_not_resizable_ws(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        SAMPLE = 2005
        controller.model.resizable = False
        controller.model.wid = SAMPLE
        controller.model.changed = ()
        controller.model.is_ws_changed = True
        controller.update_positioning(101, 202)
        controller.app.run_task.assert_called_with("move", SAMPLE)

    def test_BaseController_update_positioning_not_calling_run_task_move_w_not_resize(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        controller.model.resizable = False
        controller.model.wid = 2008
        controller.model.changed = ()
        controller.model.is_ws_changed = False
        controller.update_positioning(101, 202)
        controller.app.run_task.assert_not_called()

    def test_BaseController_update_positioning_calls_next_for_not_resizable(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        controller.model.resizable = False
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller.update_positioning(101, 202)
        mocked.assert_called_once()

    def test_BaseController_update_positioning_for_resizable_sets_state(self, mocker):
        controller = controller_mocked_next(mocker)
        controller.model.resizable = True
        mocker.patch("arrangeit.base.BaseController.place_on_opposite_corner")
        mocked_next = mocker.patch("arrangeit.base.BaseController.next")
        new_state = controller.resizing_state_counterpart()
        controller.update_positioning(101, 202)
        assert controller.state == new_state
        mocked_next.assert_not_called()
        controller.app.run_task.assert_not_called()

    def test_BaseController_update_positioning_for_resizable_calls_place_on_opposite(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        controller.model.resizable = True
        mocked = mocker.patch("arrangeit.base.BaseController.place_on_opposite_corner")
        controller.update_positioning(101, 202)
        mocked.assert_called_once()

    def test_BaseController_update_positioning_for_resizable_calls_master_update(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        controller.model.resizable = True
        controller.screenshot_when_exposed = True
        mocker.patch("arrangeit.base.BaseController.place_on_opposite_corner")
        mocker.patch("arrangeit.base.BaseController.set_screenshot")
        controller.update_positioning(109, 243)
        controller.view.master.update_idletasks.assert_called_once()
        controller.view.master.update_idletasks.assert_called_with()

    def test_BaseController_update_positioning_for_resizable_calls_set_screenshot(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        controller.model.resizable = True
        controller.screenshot_when_exposed = True
        mocker.patch("arrangeit.base.BaseController.place_on_opposite_corner")
        mocked = mocker.patch("arrangeit.base.BaseController.set_screenshot")
        controller.update_positioning(110, 244)
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_BaseController_update_positioning_for_resizable_not_calling_set_screenshot(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        controller.model.resizable = True
        controller.screenshot_when_exposed = False
        mocker.patch("arrangeit.base.BaseController.place_on_opposite_corner")
        mocked = mocker.patch("arrangeit.base.BaseController.set_screenshot")
        controller.update_positioning(110, 244)
        mocked.assert_not_called()
        controller.view.master.update.assert_not_called()

    ## BaseController.update_resizing
    def test_BaseController_update_resizing_corner_0_calls_set_changed(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.next")
        mocked = mocker.patch("arrangeit.base.WindowModel")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.RESIZE
        x, y, w, h = 111, 112, 328, 423
        view.return_value.master.winfo_width.return_value = w
        view.return_value.master.winfo_height.return_value = h
        controller.update_resizing(x, y)
        mocked.return_value.set_changed.assert_called_with(
            x=x - Settings.SHIFT_CURSOR, y=y - Settings.SHIFT_CURSOR, w=w, h=h
        )

    def test_BaseController_update_resizing_corner_1_calls_set_changed(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.next")
        mocked = mocker.patch("arrangeit.base.WindowModel")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.RESIZE + 1
        x, y, w, h = 111, 112, 328, 423
        view.return_value.master.winfo_width.return_value = w
        view.return_value.master.winfo_height.return_value = h
        controller.update_resizing(x, y)
        mocked.return_value.set_changed.assert_called_with(
            y=y - Settings.SHIFT_CURSOR, w=w, h=h
        )

    def test_BaseController_update_resizing_corner_2_calls_set_changed(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.next")
        mocked = mocker.patch("arrangeit.base.WindowModel")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.RESIZE + 2
        x, y, w, h = 158, 159, 310, 380
        view.return_value.master.winfo_width.return_value = w
        view.return_value.master.winfo_height.return_value = h
        controller.update_resizing(x, y)
        mocked.return_value.set_changed.assert_called_with(w=w, h=h)

    def test_BaseController_update_resizing_corner_3_calls_set_changed(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.next")
        mocked = mocker.patch("arrangeit.base.WindowModel")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.RESIZE + 3
        x, y, w, h = 108, 109, 320, 410
        view.return_value.master.winfo_width.return_value = w
        view.return_value.master.winfo_height.return_value = h
        controller.update_resizing(x, y)
        mocked.return_value.set_changed.assert_called_with(
            x=x - Settings.SHIFT_CURSOR, w=w, h=h
        )

    def test_BaseController_update_resizing_calls_run_task_move_and_resize_window(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        SAMPLE = 5005
        controller.model.wid = SAMPLE
        controller.model.changed = (200, 200)
        controller.update_resizing(101, 202)
        controller.app.run_task.assert_called_with("move_and_resize", SAMPLE)

    def test_BaseController_update_resizing_calls_run_task_move_and_resize_for_ws(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        SAMPLE = 5005
        controller.model.wid = SAMPLE
        controller.model.changed = ()
        controller.model.is_ws_changed = True
        controller.update_resizing(101, 202)
        controller.app.run_task.assert_called_with("move_and_resize", SAMPLE)

    def test_BaseController_update_resizing_skips_run_task_move_and_resize_window(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        controller.model.wid = 5412
        controller.model.changed = ()
        controller.model.is_ws_changed = False
        controller.update_resizing(101, 202)
        controller.app.run_task.assert_not_called()

    def test_BaseController_update_resizing_calls_next(self, mocker):
        controller = controller_mocked_next(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller.update_resizing(100, 100)
        mocked.assert_called_once()

    ## BaseController.workspace_activated
    def test_BaseController_workspace_activated_calls_task_move_to_workspace(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        controller = base.BaseController(mocker.MagicMock())
        SAMPLE = 1003
        controller.workspace_activated(SAMPLE)
        controller.app.run_task.assert_called_with(
            "move_to_workspace", view.return_value.get_root_wid.return_value, SAMPLE
        )

    def test_BaseController_workspace_activated_calls_set_changed(self, mocker):
        mocker.patch("arrangeit.base.get_tkinter_root")
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocked = mocker.patch("arrangeit.data.WindowModel.set_changed")
        controller = base.BaseController(mocker.MagicMock())
        SAMPLE = 1044
        controller.workspace_activated(SAMPLE)
        mocked.assert_called_with(ws=SAMPLE)

    def test_BaseController_workspace_activated_calls_recapture_mouse_for_OTHER(
        self, mocker
    ):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.OTHER
        controller.workspace_activated(1074)
        mocked.assert_called_once()

    @pytest.mark.parametrize("state", [Settings.LOCATE, Settings.RESIZE])
    def test_BaseController_workspace_activated_not_calling_recapture_mouse_not_OTHER(
        self, mocker, state
    ):
        mocker.patch("arrangeit.base.get_tkinter_root")
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.BaseController.display_message")
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = state
        controller.workspace_activated(1074)
        mocked.assert_not_called()

    def test_BaseController_workspace_activated_calls_display_message(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        mocked = mocker.patch("arrangeit.base.BaseController.display_message")
        controller = base.BaseController(mocker.MagicMock())
        controller.workspace_activated(1278)
        mocked.assert_called_once()
        mocked.assert_called_with(MESSAGES["msg_workspace_changed"])
