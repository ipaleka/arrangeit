import pytest

from arrangeit import base, data
from arrangeit.settings import Settings

from .mock_helpers import (
    mocked_setup,
    mocked_setup_root,
    mocked_setup_view,
    controller_mocked_app,
    controller_mocked_key_press,
)


class TestBaseController(object):
    """Testing class for base Controller class."""

    ## BaseController
    @pytest.mark.parametrize(
        "attr",
        [
            "app",
            "model",
            "generator",
            "view",
            "listener",
            "state",
            "screenshot_widget",
            "screenshot",
            "snapping_targets",
        ],
    )
    def test_BaseController_inits_attr_as_None(self, attr):
        assert getattr(base.BaseController, attr) is None

    ## BaseController.__init__
    def test_BaseController_init_sets_app_attribute(self, mocker):
        mocker.patch("arrangeit.base.BaseController.setup")
        app = mocker.MagicMock()
        controller = base.BaseController(app)
        assert controller.app == app

    def test_BaseController_initialization_instantiates_WindowModel(self, mocker):
        mocker.patch("arrangeit.base.BaseController.setup")
        controller = base.BaseController(None)
        assert getattr(controller, "model", None) is not None
        assert isinstance(getattr(controller, "model"), data.WindowModel)

    def test_BaseController_initialization_calls_setup(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseController.setup")
        base.BaseController(mocker.MagicMock())
        mocked.assert_called_once()

    ## BaseController.setup
    def test_BaseController_setup_calls_get_tkinter_root(self, mocker):
        mocked = mocked_setup_root(mocker)
        controller = base.BaseController(None)
        mocked.call_count = 0
        controller.setup()
        assert mocked.call_count == 1

    def test_BaseController_setup_calls_get_screenshot_widget(self, mocker):
        root = mocked_setup_root(mocker)
        mocked = mocker.patch("arrangeit.base.get_screenshot_widget")
        controller = base.BaseController(None)
        mocked.call_count = 0
        controller.setup()
        assert mocked.call_count == 1
        mocked.assert_called_with(root.return_value)

    def test_BaseController_setup_calls_setup_root_window(self, mocker):
        root = mocked_setup_root(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.setup_root_window")
        controller = base.BaseController(None)
        mocked.call_count = 0
        controller.setup()
        assert mocked.call_count == 1
        mocked.assert_called_with(root.return_value)

    def test_BaseController_setup_initializes_ViewApplication(self, mocker):
        root = mocked_setup_root(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(None)
        mocked.call_count = 0
        controller.setup()
        assert mocked.call_count == 1
        mocked.assert_called_with(master=root.return_value, controller=controller)

    def test_BaseController_setup_withdraws_root_tk_window(self, mocker):
        root = mocked_setup_root(mocker)
        controller = base.BaseController(None)
        root.return_value.withdraw.call_count = 0
        controller.setup()
        assert root.return_value.withdraw.call_count == 1

    ## BaseController.setup_root_window
    def test_BaseController_setup_root_window_calls_wm_attributes(self, mocker):
        root = mocker.MagicMock()
        base.BaseController(None).setup_root_window(root)
        assert root.wm_attributes.call_count == 2
        calls = [
            mocker.call("-alpha", Settings.ROOT_ALPHA),
            mocker.call("-topmost", True),
        ]
        root.wm_attributes.assert_has_calls(calls, any_order=True)

    ## BaseController.set_default_geometry
    def test_BaseController_set_default_geometry_calls_quarter_by_smaller(self, mocker):
        root = mocker.MagicMock()
        mocked = mocker.patch(
            "arrangeit.base.quarter_by_smaller", return_value=(100, 100)
        )
        w, h = 1001, 1002
        root.winfo_screenwidth.return_value = w
        root.winfo_screenheight.return_value = h
        base.BaseController(None).set_default_geometry(root)
        assert mocked.call_count == 1
        mocked.assert_called_with(w, h)

    def test_BaseController_set_default_geometry_calls_geometry(self, mocker):
        root = mocker.MagicMock()
        w, h = 1003, 1004
        mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(w, h))
        base.BaseController(None).set_default_geometry(root)
        assert root.geometry.call_count == 1
        root.geometry.assert_called_with("{}x{}".format(w, h))

    ## BaseController.prepare_view
    def test_BaseController_prepare_view_calls_WorkspacesCollection_add_workspaces(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        app = mocker.MagicMock()
        base.BaseController(app).prepare_view()
        assert view.return_value.workspaces.add_workspaces.call_count == 1
        calls = [mocker.call(app.collector.get_available_workspaces.return_value)]
        view.return_value.workspaces.add_workspaces.assert_has_calls(
            calls, any_order=True
        )

    def test_BaseController_prepare_view_calls_WindowsList_add_windows_without_first(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        app = mocker.MagicMock()
        SAMPLE = [1, 2, 3]
        app.collector.collection.get_windows_list.return_value = SAMPLE
        base.BaseController(app).prepare_view()
        assert view.return_value.windows.add_windows.call_count == 1
        calls = [mocker.call(SAMPLE[1:])]
        view.return_value.windows.add_windows.assert_has_calls(calls, any_order=True)

    ## BaseController.set_screenshot
    def test_BaseController_set_screenshot_calls_grab_window_screen(self, mocker):
        app = mocker.MagicMock()
        app.grab_window_screen.return_value = (None, (0, 0))
        controller = base.BaseController(app)
        controller.set_screenshot()
        app.grab_window_screen.assert_called_once()
        app.grab_window_screen.assert_called_with(controller.model)

    def test_BaseController_set_screenshot_sets_screenshot_reference_variable(
        self, mocker
    ):
        mocked_setup(mocker)
        app = mocker.MagicMock()
        SAMPLE = 50
        app.grab_window_screen.return_value = (SAMPLE, (0, 0))
        controller = base.BaseController(app)
        controller.set_screenshot()
        app.grab_window_screen.assert_called_once()
        app.grab_window_screen.assert_called_with(controller.model)
        assert controller.screenshot == 50

    def test_BaseController_set_screenshot_configures_screenshot_widget(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.get_screenshot_widget")
        app = mocker.MagicMock()
        SAMPLE = 50
        app.grab_window_screen.return_value = (SAMPLE, (0, 0))
        controller = base.BaseController(app)
        controller.set_screenshot()
        calls = [mocker.call(image=SAMPLE)]
        mocked.return_value.configure.assert_has_calls(calls, any_order=True)

    def test_BaseController_set_screenshot_places_screenshot_widget(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.get_screenshot_widget")
        app = mocker.MagicMock()
        SAMPLE = (8, 9)
        app.grab_window_screen.return_value = (None, SAMPLE)
        controller = base.BaseController(app)
        controller.set_screenshot()
        calls = [
            mocker.call(
                x=SAMPLE[0] + Settings.SCREENSHOT_SHIFT_PIXELS,
                y=SAMPLE[1] + Settings.SCREENSHOT_SHIFT_PIXELS,
            )
        ]
        mocked.return_value.place.assert_has_calls(calls, any_order=True)

    ## BaseController.check_positioning_snapping
    def test_BaseController_check_positioning_snapping_calls_get_snapping_sources_for(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocked = mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        x, y, w, h = 100, 200, 300, 400
        view.return_value.master.winfo_width.return_value = w
        view.return_value.master.winfo_height.return_value = h
        view.return_value.workspaces.active = 1001
        controller = controller_mocked_app(mocker)
        controller.snapping_targets = {1001: ["foo"]}
        controller.state = Settings.LOCATE
        controller.check_positioning_snapping(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(
            (x, y, w, h), Settings.SNAP_PIXELS, corner=controller.state
        )

    def test_BaseController_check_positioning_snapping_calls_check_intersection(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        root_rects = mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        mocked = mocker.patch("arrangeit.base.check_intersection")
        view.return_value.workspaces.active = 1001
        controller = controller_mocked_app(mocker)
        SAMPLE = ["foo"]
        controller.snapping_targets = {1001: SAMPLE}
        controller.check_positioning_snapping(100, 100)
        mocked.assert_called_once()
        mocked.assert_called_with(root_rects.return_value, SAMPLE)

    def test_BaseController_check_positioning_snapping_c_offset_for_intersecting_pair(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        mocked_check = mocker.patch("arrangeit.base.check_intersection")
        mocked = mocker.patch("arrangeit.base.offset_for_intersecting_pair")
        view.return_value.workspaces.active = 1001
        controller = controller_mocked_app(mocker)
        controller.snapping_targets = {1001: ["foo"]}
        controller.state = Settings.LOCATE
        controller.check_positioning_snapping(100, 100)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_check.return_value, Settings.SNAP_PIXELS)

    ## BaseController.change_position
    def test_BaseController_change_position_calls_check_positioning_snapping(
        self, mocker
    ):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.move_cursor")
        mocked_snap = mocker.patch("arrangeit.base.Settings")
        type(mocked_snap).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        mocked = mocker.patch(
            "arrangeit.base.BaseController.check_positioning_snapping"
        )
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        controller.change_position(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(x, y)

    def test_BaseController_change_position_snapping_is_on_false(self, mocker):
        view = mocked_setup_view(mocker)
        mocked = mocker.patch(
            "arrangeit.base.BaseController.check_positioning_snapping"
        )
        mocked_move_cursor = mocker.patch("arrangeit.base.move_cursor")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        mocked_snap = mocker.patch("arrangeit.base.Settings")
        type(mocked_snap).SNAPPING_IS_ON = mocker.PropertyMock(return_value=False)
        controller.change_position(x, y)
        mocked.assert_not_called()
        mocked_move_cursor.assert_not_called()
        view.return_value.master.geometry.assert_called_with("+{}+{}".format(x, y))

    def test_BaseController_change_position_calls_move_cursor(self, mocker):
        mocked_setup(mocker)
        mocked_snap = mocker.patch("arrangeit.base.Settings")
        type(mocked_snap).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        offset = (10, 12)
        mocker.patch(
            "arrangeit.base.BaseController.check_positioning_snapping",
            return_value=offset,
        )
        mocked = mocker.patch("arrangeit.base.move_cursor")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        controller.change_position(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(x + offset[0], y + offset[1])

    def test_BaseController_change_position_not_calling_set_geometry(self, mocker):
        view = mocked_setup_view(mocker)
        mocked_snap = mocker.patch("arrangeit.base.Settings")
        type(mocked_snap).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        offset = (10, 12)
        mocker.patch(
            "arrangeit.base.BaseController.check_positioning_snapping",
            return_value=offset,
        )
        mocker.patch("arrangeit.base.move_cursor")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        controller.change_position(x, y)
        view.return_value.master.geometry.assert_not_called()

    def test_BaseController_change_position_not_calling_move_cursor(self, mocker):
        view = mocked_setup_view(mocker)
        mocked_snap = mocker.patch("arrangeit.base.Settings")
        type(mocked_snap).SNAPPING_IS_ON = mocker.PropertyMock(return_value=True)
        mocker.patch(
            "arrangeit.base.BaseController.check_positioning_snapping",
            return_value=(0, 0),
        )
        mocked = mocker.patch("arrangeit.base.move_cursor")
        x, y = 105, 108
        controller = controller_mocked_app(mocker)
        controller.change_position(x, y)
        mocked.assert_not_called()
        assert view.return_value.master.geometry.call_count == 1
        view.return_value.master.geometry.assert_called_with("+{}+{}".format(x, y))

    ## BaseController.change_size
    def test_BaseController_change_size_valid_x_and_y(self, mocker):
        view = mocked_setup_view(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).changed_x = mocker.PropertyMock(return_value=100)
        type(model.return_value).changed_y = mocker.PropertyMock(return_value=200)
        x, y = 300, 400
        controller = controller_mocked_app(mocker)
        controller.change_size(x, y)
        assert view.return_value.master.geometry.call_count == 1
        view.return_value.master.geometry.assert_called_with(
            "{}x{}".format(
                x - 100 + Settings.WINDOW_SHIFT_PIXELS,
                y - 200 + Settings.WINDOW_SHIFT_PIXELS,
            )
        )

    @pytest.mark.parametrize(
        "x,y,changed",
        [
            (100, 200, (120, 120, 120, 120)),
            (200, 100, (120, 120, 120, 120)),
            (100, 100, (120, 120, 120, 120)),
        ],
    )
    def test_BaseController_change_size_invalid_xy(self, mocker, x, y, changed):
        view = mocked_setup_view(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).changed_x = mocker.PropertyMock(
            return_value=changed[0]
        )
        type(model.return_value).changed_y = mocker.PropertyMock(
            return_value=changed[1]
        )
        controller = controller_mocked_app(mocker)
        controller.change_size(x, y)
        assert view.return_value.master.geometry.call_count == 1
        view.return_value.master.geometry.assert_called_with(
            "{}x{}".format(Settings.WINDOW_MIN_WIDTH, Settings.WINDOW_MIN_HEIGHT)
        )

    ## BaseController.cycle_corners
    @pytest.mark.skip("not implemented yet")
    @pytest.mark.parametrize(
        "state,expected", [(0, 1), (1, 2), (4, 0), (14, 10), (11, 12), (104, 100)]
    )
    def test_BaseController_cycle_corners_functionality(self, mocker, state, expected):
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        controller.state = state
        controller.cycle_corners()
        assert controller.state == expected

    ## BaseController.listed_window_activated_by_digit
    def test_BaseController_listed_window_activated_by_digit_calls_winfo_children(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        view.return_value.windows.winfo_children.return_value = []
        controller = controller_mocked_app(mocker)
        controller.listed_window_activated_by_digit(2)
        view.return_value.windows.winfo_children.call_count == 1

    def test_BaseController_listed_window_activated_by_digit_calls_l_window_activated(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.listed_window_activated")
        mocked_children = [mocker.MagicMock(), mocker.MagicMock()]
        view.return_value.windows.winfo_children.return_value = mocked_children
        type(mocked_children[1]).wid = mocker.PropertyMock(return_value=70001)
        controller = controller_mocked_app(mocker)
        controller.listed_window_activated_by_digit(2)
        mocked.assert_called_with(70001)

    def test_BaseController_listed_window_activated_by_digit_not_calling_l_win_active(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.listed_window_activated")
        mocked_children = [mocker.MagicMock(), mocker.MagicMock()]
        view.return_value.windows.winfo_children.return_value = mocked_children
        type(mocked_children[1]).wid = mocker.PropertyMock(return_value=70001)
        controller = controller_mocked_app(mocker)
        controller.listed_window_activated_by_digit(3)
        mocked.assert_not_called()

    ## BaseController.place_on_top_left
    def test_BaseController_place_on_top_left_calls_cursor_config(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.move_cursor")
        mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        controller = controller_mocked_app(mocker)
        controller.place_on_top_left()
        calls = [mocker.call(cursor="ul_angle")]
        view.return_value.master.config.assert_has_calls(calls, any_order=True)

    def test_BaseController_place_on_top_left_calls_on_mouse_move(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.move_cursor")
        mocked = mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        x, y = 101, 202
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).x = mocker.PropertyMock(return_value=x)
        type(model.return_value).y = mocker.PropertyMock(return_value=y)
        controller = controller_mocked_app(mocker)
        controller.place_on_top_left()
        mocked.assert_called_with(x, y)

    def test_BaseController_place_on_top_left_calls_move_cursor(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        mocked = mocker.patch("arrangeit.base.move_cursor")
        x, y = 101, 202
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).x = mocker.PropertyMock(return_value=x)
        type(model.return_value).y = mocker.PropertyMock(return_value=y)
        controller = controller_mocked_app(mocker)
        controller.place_on_top_left()
        mocked.assert_called_with(x, y)

    ## BaseController.place_on_right_bottom
    def test_BaseController_place_on_right_bottom_calls_cursor_config(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.move_cursor")
        mocker.patch("arrangeit.base.WindowModel")
        controller = controller_mocked_app(mocker)
        controller.place_on_right_bottom()
        calls = [mocker.call(cursor="lr_angle")]
        view.return_value.master.config.assert_has_calls(calls, any_order=True)

    def test_BaseController_place_on_right_bottom_calls_move_cursor(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.move_cursor")
        x, y, w, h = 201, 202, 203, 204
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).changed_x = mocker.PropertyMock(return_value=x)
        type(model.return_value).changed_y = mocker.PropertyMock(return_value=y)
        type(model.return_value).w = mocker.PropertyMock(return_value=w)
        type(model.return_value).h = mocker.PropertyMock(return_value=h)
        controller = controller_mocked_app(mocker)
        controller.place_on_right_bottom()
        mocked.assert_called_with(x + w, y + h)

    ## BaseController.remove_listed_window
    def test_BaseController_remove_listed_window_calls_widget_destroy(self, mocker):
        view = mocked_setup_view(mocker)
        widget = mocker.MagicMock()
        type(widget).wid = mocker.PropertyMock(return_value=100)
        view.return_value.windows.winfo_children.return_value = [widget]
        controller = controller_mocked_app(mocker)
        controller.remove_listed_window(100)
        assert widget.destroy.call_count == 1

    def test_BaseController_remove_listed_window_not_calling_destroy_for_wrong_widget(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        widget = mocker.MagicMock()
        type(widget).wid = mocker.PropertyMock(return_value=100)
        view.return_value.windows.winfo_children.return_value = [widget]
        controller = controller_mocked_app(mocker)
        controller.remove_listed_window(201)
        assert widget.destroy.call_count == 0

    def test_BaseController_remove_listed_window_calls_place_children(self, mocker):
        view = mocked_setup_view(mocker)
        widget = mocker.MagicMock()
        type(widget).wid = mocker.PropertyMock(return_value=100)
        view.return_value.windows.winfo_children.return_value = [widget]
        controller = controller_mocked_app(mocker)
        controller.remove_listed_window(100)
        assert view.return_value.windows.place_children.call_count == 1

    ## BaseController.release_mouse
    def test_BaseController_release_mouse_calls_reset_bindings(self, mocker):
        view = mocked_setup_view(mocker)
        controller = controller_mocked_app(mocker)
        controller.listener = mocker.MagicMock()
        controller.release_mouse()
        assert view.return_value.reset_bindings.call_count == 1

    def test_BaseController_release_mouse_calls_cursor_config(self, mocker):
        view = mocked_setup_view(mocker)
        controller = controller_mocked_app(mocker)
        controller.listener = mocker.MagicMock()
        controller.release_mouse()
        calls = [mocker.call(cursor="left_ptr")]
        view.return_value.master.config.assert_has_calls(calls, any_order=True)

    def test_BaseController_release_mouse_changes_state_to_OTHER(self, mocker):
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        controller.listener = mocker.MagicMock()
        controller.state = 5
        controller.release_mouse()
        assert controller.state == Settings.OTHER

    def test_BaseController_release_mouse_stops_listener(self, mocker):
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        controller.listener = mocker.MagicMock()
        controller.release_mouse()
        assert controller.listener.stop.call_count == 1

    ## BaseController.recapture_mouse
    def test_BaseController_recapture_mouse_calls_view_setup_bindings(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        mocker.patch("arrangeit.base.move_cursor")
        mocker.patch("arrangeit.base.get_mouse_listener")
        controller = controller_mocked_app(mocker)
        controller.recapture_mouse()
        assert view.return_value.setup_bindings.call_count == 1

    def test_BaseController_recapture_mouse_calls_cursor_config(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        mocker.patch("arrangeit.base.move_cursor")
        mocker.patch("arrangeit.base.get_mouse_listener")
        controller = controller_mocked_app(mocker)
        controller.recapture_mouse()
        calls = [mocker.call(cursor="ul_angle")]
        view.return_value.master.config.assert_has_calls(calls, any_order=True)

    def test_BaseController_recapture_mouse_calls_set_default_geometry(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.move_cursor")
        mocker.patch("arrangeit.base.get_mouse_listener")
        mocked = mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        controller = controller_mocked_app(mocker)
        controller.recapture_mouse()
        mocked.assert_called_once()
        mocked.assert_called_with(view.return_value.master)

    def test_BaseController_recapture_mouse_changes_state_to_LOCATE(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        mocker.patch("arrangeit.base.move_cursor")
        mocker.patch("arrangeit.base.get_mouse_listener")
        controller = controller_mocked_app(mocker)
        controller.state = 5
        controller.recapture_mouse()
        assert controller.state == Settings.LOCATE

    def test_BaseController_recapture_mouse_calls_move_cursor(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        mocker.patch("arrangeit.base.get_mouse_listener")
        mocked = mocker.patch("arrangeit.base.move_cursor")
        controller = controller_mocked_app(mocker)
        controller.recapture_mouse()
        mocked.assert_called_once()
        mocked.assert_called_with(
            view.return_value.master.winfo_x.return_value,
            view.return_value.master.winfo_y.return_value,
        )

    def test_BaseController_recapture_mouse_calls_get_mouse_listener(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        mocker.patch("arrangeit.base.move_cursor")
        mocked = mocker.patch("arrangeit.base.get_mouse_listener")
        controller = controller_mocked_app(mocker)
        controller.recapture_mouse()
        mocked.assert_called_once()
        mocked.assert_called_with(controller.on_mouse_move)

    def test_BaseController_recapture_mouse_sets_listener_attribute(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        mocker.patch("arrangeit.base.move_cursor")
        listener = mocker.MagicMock()
        mocker.patch("arrangeit.base.get_mouse_listener", return_value=listener)
        controller = controller_mocked_app(mocker)
        controller.recapture_mouse()
        assert controller.listener == listener

    def test_BaseController_recapture_mouse_starts_listener(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        mocker.patch("arrangeit.base.move_cursor")
        mocked = mocker.patch("pynput.mouse.Listener")
        controller = controller_mocked_app(mocker)
        controller.recapture_mouse()
        assert mocked.return_value.start.call_count == 1

    ## BaseController.shutdown
    def test_BaseController_shutdown_stops_listener(self, mocker):
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        controller.listener = mocker.MagicMock()
        controller.shutdown()
        assert controller.listener.stop.call_count == 1

    def test_BaseController_shutdown_calls_master_destroy(self, mocker):
        view = mocked_setup_view(mocker)
        controller = controller_mocked_app(mocker)
        controller.listener = mocker.MagicMock()
        controller.shutdown()
        assert view.return_value.master.destroy.call_count == 1

    ## BaseController.skip_current_window
    def test_BaseController_skip_current_window_calls_model_clear_changed(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.next")
        mocked = mocker.patch("arrangeit.data.WindowModel.clear_changed")
        controller_mocked_app(mocker).skip_current_window()
        assert mocked.call_count == 1

    def test_BaseController_skip_current_window_calls_next(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller_mocked_app(mocker).skip_current_window()
        assert mocked.call_count == 1

    ## BaseController.switch_workspace
    def test_BaseController_switch_workspace_calls_winfo_id(self, mocker):
        view = mocked_setup_view(mocker)
        controller = controller_mocked_app(mocker)
        controller.switch_workspace()
        view.return_value.master.winfo_id.call_count == 1

    def test_BaseController_switch_workspace_calls_task_move_to_workspace(self, mocker):
        view = mocked_setup_view(mocker)
        number = 1051
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).workspace = mocker.PropertyMock(return_value=number)
        controller = controller_mocked_app(mocker)
        controller.switch_workspace()
        controller.app.run_task.assert_called_with(
            "move_to_workspace", view.return_value.master.winfo_id.return_value, number
        )

    ## BaseController.workspace_activated_by_digit
    def test_BaseController_workspace_activated_by_digit_calls_winfo_children(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        controller = controller_mocked_app(mocker)
        controller.workspace_activated_by_digit(1)
        view.return_value.workspaces.winfo_children.call_count == 1

    def test_BaseController_workspace_activated_by_digit_calls_workspace_activated(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocked_children = [mocker.MagicMock(), mocker.MagicMock()]
        view.return_value.workspaces.winfo_children.return_value = mocked_children
        number = 1052
        type(mocked_children[1]).number = mocker.PropertyMock(return_value=number)
        mocked = mocker.patch("arrangeit.base.BaseController.workspace_activated")
        controller = controller_mocked_app(mocker)
        controller.workspace_activated_by_digit(2)
        mocked.assert_called_with(number)

    def test_BaseController_workspace_activated_by_digit_not_calling_workspace_active(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocked_children = [mocker.MagicMock(), mocker.MagicMock()]
        view.return_value.workspaces.winfo_children.return_value = mocked_children
        mocked = mocker.patch("arrangeit.base.BaseController.workspace_activated")
        controller = controller_mocked_app(mocker)
        controller.workspace_activated_by_digit(3)
        mocked.assert_not_called()

    ## BaseController.on_key_pressed
    def test_BaseController_on_key_pressed_for_Escape_calls_shutdown(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.shutdown")
        controller_mocked_key_press(mocker, "Escape")
        assert mocked.call_count == 1

    @pytest.mark.parametrize("key", ["Return", "KP_Enter"])
    def test_BaseController_on_key_pressed_for_Enter_calls_update(self, mocker, key):
        view = mocked_setup_view(mocker)
        x, y = 204, 205
        view.return_value.master.winfo_pointerx.return_value = x
        view.return_value.master.winfo_pointery.return_value = y
        mocked = mocker.patch("arrangeit.base.BaseController.update")
        controller_mocked_key_press(mocker, key)
        mocked.assert_called_with(x, y)

    @pytest.mark.parametrize("key", ["Space", "Tab"])
    def test_BaseController_on_key_pressed_calls_skip_current_window(self, mocker, key):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.skip_current_window")
        controller_mocked_key_press(mocker, key)
        assert mocked.call_count == 1

    @pytest.mark.parametrize("key", ["Control_L"])
    def test_BaseController_on_key_pressed_calls_release_mouse(self, mocker, key):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.release_mouse")
        controller_mocked_key_press(mocker, key)
        assert mocked.call_count == 1

    @pytest.mark.parametrize("key", ["Alt_L"])
    def test_BaseController_on_key_pressed_calls_cycle_corners(self, mocker, key):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.cycle_corners")
        controller_mocked_key_press(mocker, key)
        assert mocked.call_count == 1

    @pytest.mark.parametrize("key", ["KP_1", "KP_4", "KP_9", "1", "5", "9"])
    def test_BaseController_on_key_pressed_for_digit_calls_workspace_activated_by_digit(
        self, mocker, key
    ):
        mocked_setup(mocker)
        mocked = mocker.patch(
            "arrangeit.base.BaseController.workspace_activated_by_digit"
        )
        controller_mocked_key_press(mocker, key)
        assert mocked.call_count == 1
        mocked.assert_called_with(int(key[-1]))

    @pytest.mark.parametrize("key", ["KP_0", "0"])
    def test_BaseController_on_key_pressed_for_digit_0_not_calling_workspace_activated_by_digit(
        self, mocker, key
    ):
        mocked_setup(mocker)
        mocked = mocker.patch(
            "arrangeit.base.BaseController.workspace_activated_by_digit"
        )
        controller_mocked_key_press(mocker, key)
        mocked.assert_not_called()

    @pytest.mark.parametrize("key", ["F1", "F4", "F9", "F12"])
    def test_BaseController_on_key_pressed_for_func_keys_c_listed_window_activated_by_d(
        self, mocker, key
    ):
        mocked_setup(mocker)
        mocked = mocker.patch(
            "arrangeit.base.BaseController.listed_window_activated_by_digit"
        )
        controller_mocked_key_press(mocker, key)
        assert mocked.call_count == 1
        mocked.assert_called_with(int(key[1:]))

    def test_BaseController_on_key_pressed_returns_break(self, mocker):
        mocked_setup(mocker)
        returned = base.BaseController(mocker.MagicMock()).on_key_pressed(
            mocker.MagicMock()
        )
        assert returned == "break"

    ## BaseController.on_mouse_move
    def test_BaseController_on_mouse_move_calls_change_position_for_None(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.change_position")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        controller.state = None
        controller.on_mouse_move(x, y)
        mocked.assert_called_with(x, y)

    def test_BaseController_on_mouse_move_calls_change_position_for_LOCATE(
        self, mocker
    ):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.change_position")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        controller.state = Settings.LOCATE
        controller.on_mouse_move(x, y)
        mocked.assert_called_with(x, y)

    def test_BaseController_on_mouse_move_calls_change_size_for_RESIZE(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.change_size")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        controller.state = Settings.RESIZE
        controller.on_mouse_move(x, y)
        mocked.assert_called_with(x, y)

    ## BaseController.on_mouse_left_down
    def test_BaseController_on_mouse_left_down_calls_update(self, mocker):
        view = mocked_setup_view(mocker)
        x, y = 507, 508
        view.return_value.master.winfo_pointerx.return_value = x
        view.return_value.master.winfo_pointery.return_value = y
        mocked = mocker.patch("arrangeit.base.BaseController.update")
        base.BaseController(mocker.MagicMock()).on_mouse_left_down(mocker.MagicMock())
        mocked.assert_called_with(x, y)

    def test_BaseController_on_mouse_left_down_returns_break(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.update")
        returned = base.BaseController(mocker.MagicMock()).on_mouse_left_down(
            mocker.MagicMock()
        )
        assert returned == "break"

    ## BaseController.on_mouse_middle_down
    def test_BaseController_on_mouse_middle_down_calls_release_mouse(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.release_mouse")
        base.BaseController(mocker.MagicMock()).on_mouse_middle_down(mocker.MagicMock())
        assert mocked.call_count == 1

    def test_BaseController_on_mouse_middle_down_returns_break(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.release_mouse")
        returned = base.BaseController(mocker.MagicMock()).on_mouse_middle_down(
            mocker.MagicMock()
        )
        assert returned == "break"

    ## BaseController.on_mouse_right_down
    def test_BaseController_on_mouse_right_down_calls_skip_current_window(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.skip_current_window")
        base.BaseController(mocker.MagicMock()).on_mouse_right_down(mocker.MagicMock())
        assert mocked.call_count == 1

    def test_BaseController_on_mouse_right_down_returns_break(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.skip_current_window")
        returned = base.BaseController(mocker.MagicMock()).on_mouse_right_down(
            mocker.MagicMock()
        )
        assert returned == "break"

    ## BaseController.on_continue
    def test_BaseController_on_continue_calls_recapture_mouse(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        base.BaseController(mocker.MagicMock()).on_continue(mocker.MagicMock())
        assert mocked.call_count == 1

    def test_BaseController_on_continue_returns_break(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        returned = base.BaseController(mocker.MagicMock()).on_continue(
            mocker.MagicMock()
        )
        assert returned == "break"

    ## BaseController.mainloop
    def test_BaseController_mainloop_calls_Tkinter_mainloop(self, mocker):
        view = mocked_setup_view(mocker)
        base.BaseController(mocker.MagicMock()).mainloop()
        assert view.return_value.mainloop.call_count == 1
