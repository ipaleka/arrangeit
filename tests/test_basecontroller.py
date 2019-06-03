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
            "default_size",
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
        mocked.reset_mock()
        controller.setup()
        assert mocked.call_count == 1

    def test_BaseController_setup_calls_get_screenshot_widget(self, mocker):
        root = mocked_setup_root(mocker)
        mocked = mocker.patch("arrangeit.base.get_screenshot_widget")
        controller = base.BaseController(None)
        mocked.reset_mock()
        controller.setup()
        assert mocked.call_count == 1
        mocked.assert_called_with(root.return_value)

    def test_BaseController_setup_calls_setup_root_window(self, mocker):
        root = mocked_setup_root(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.setup_root_window")
        controller = base.BaseController(None)
        mocked.reset_mock()
        controller.setup()
        assert mocked.call_count == 1
        mocked.assert_called_with(root.return_value)

    def test_BaseController_setup_initializes_ViewApplication(self, mocker):
        root = mocked_setup_root(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(None)
        mocked.reset_mock()
        controller.setup()
        assert mocked.call_count == 1
        mocked.assert_called_with(master=root.return_value, controller=controller)

    def test_BaseController_setup_withdraws_root_tk_window(self, mocker):
        root = mocked_setup_root(mocker)
        controller = base.BaseController(None)
        root.return_value.withdraw.reset_mock()
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

    def test_BaseController_setup_root_window_calls_config_background(self, mocker):
        root = mocker.MagicMock()
        base.BaseController(None).setup_root_window(root)
        calls = [mocker.call(background=Settings.MAIN_BG)]
        root.config.assert_has_calls(calls, any_order=True)

    ## BaseController.set_default_geometry
    def test_BaseController_set_default_geometry_calls_quarter_by_smaller(self, mocker):
        root = mocker.MagicMock()
        mocked = mocker.patch(
            "arrangeit.base.quarter_by_smaller", return_value=(100, 100)
        )
        w, h = 1001, 1002
        root.winfo_screenwidth.return_value = w
        root.winfo_screenheight.return_value = h
        controller = base.BaseController(None)
        controller.default_size = None
        controller.set_default_geometry(root)
        assert mocked.call_count == 1
        mocked.assert_called_with(w, h)

    def test_BaseController_set_default_geometry_sets_default_size(self, mocker):
        root = mocker.MagicMock()
        SAMPLE = (244, 145)
        mocker.patch("arrangeit.base.quarter_by_smaller", return_value=SAMPLE)
        w, h = 1001, 1002
        root.winfo_screenwidth.return_value = w
        root.winfo_screenheight.return_value = h
        controller = base.BaseController(None)
        controller.default_size = None
        controller.set_default_geometry(root)
        assert controller.default_size == SAMPLE

    def test_BaseController_set_default_geometry_not_calling_quarter_by_smaller(
        self, mocker
    ):
        root = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.base.quarter_by_smaller")
        controller = base.BaseController(None)
        controller.default_size = (1000, 1000)
        controller.set_default_geometry(root)
        mocked.assert_not_called()

    def test_BaseController_set_default_geometry_not_changing_default_size(
        self, mocker
    ):
        root = mocker.MagicMock()
        mocker.patch("arrangeit.base.quarter_by_smaller")
        controller = base.BaseController(None)
        SAMPLE = (1002, 1003)
        controller.default_size = SAMPLE
        controller.set_default_geometry(root)
        assert controller.default_size == SAMPLE

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
        mocked.return_value.config.assert_has_calls(calls, any_order=True)

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

    ## BaseController.resizing_state_counterpart
    @pytest.mark.parametrize("state,expected", [(0, 12), (1, 13), (2, 10), (3, 11)])
    def test_BaseController_resizing_state_counterpart(self, mocker, state, expected):
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        controller.state = state
        assert controller.resizing_state_counterpart == expected

    ## BaseController.change_position
    def test_BaseController_change_position_calls_check_snapping(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.check_snapping")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        controller.change_position(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(x, y)

    def test_BaseController_change_position_not_calling_set_geometry_and_root_rect(
        self, mocker
    ):
        view = mocked_setup_view(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.get_root_rect")
        mocker.patch("arrangeit.base.BaseController.check_snapping", return_value=True)
        controller = controller_mocked_app(mocker)
        controller.change_position(100, 100)
        view.return_value.master.geometry.assert_not_called()
        mocked.assert_not_called()

    def test_BaseController_change_position_calls_get_root_rect(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.check_snapping", return_value=False)
        mocked = mocker.patch(
            "arrangeit.base.BaseController.get_root_rect", return_value=(0, 0, 0, 0)
        )
        x, y = 101, 470
        controller = controller_mocked_app(mocker)
        controller.change_position(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(x, y)

    def test_BaseController_change_position_calls_master_geometry(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.check_snapping", return_value=False)
        SAMPLE = (0, 0)
        mocker.patch(
            "arrangeit.base.BaseController.get_root_rect", return_value=(*SAMPLE, 0, 0)
        )
        controller = controller_mocked_app(mocker)
        controller.change_position(100, 100)
        view.return_value.master.geometry.assert_called_once()
        view.return_value.master.geometry.assert_called_with("+{}+{}".format(*SAMPLE))

    ## BaseController.change_size
    def test_BaseController_change_size_calls_check_current_size(self, mocker):
        mocker.patch("arrangeit.base.BaseController.check_snapping", return_value=False)
        mocked = mocker.patch(
            "arrangeit.base.BaseController.check_current_size", return_value=(100, 100)
        )
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        controller.change_size(100, 100)
        mocked.assert_called_once()

    def test_BaseController_change_size_calls_set_minimum_size_and_returns_for_invalid(
        self, mocker
    ):
        SAMPLE = (120, 210)
        mocker.patch("arrangeit.base.BaseController.check_snapping", return_value=False)
        mocker.patch(
            "arrangeit.base.BaseController.check_current_size", return_value=SAMPLE
        )
        mocked = mocker.patch("arrangeit.base.BaseController.set_minimum_size")
        mocked_setup(mocker)
        controller = controller_mocked_app(mocker)
        returned = controller.change_size(100, 100)
        mocked.assert_called_once()
        mocked.assert_called_with(*SAMPLE)
        assert returned == mocked.return_value

    def test_BaseController_change_size_calls_check_snapping(self, mocker):
        mocked_setup(mocker)
        mocker.patch(
            "arrangeit.base.BaseController.check_current_size", return_value=False
        )
        mocked = mocker.patch("arrangeit.base.BaseController.check_snapping")
        x, y = 100, 200
        controller = controller_mocked_app(mocker)
        controller.change_size(x, y)
        mocked.assert_called_once()
        mocked.assert_called_with(x, y)

    def test_BaseController_change_size_not_calling_set_geometry(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch(
            "arrangeit.base.BaseController.check_current_size", return_value=False
        )
        mocker.patch("arrangeit.base.BaseController.check_snapping", return_value=True)
        controller = controller_mocked_app(mocker)
        controller.change_size(100, 100)
        view.return_value.master.geometry.assert_not_called()

    def test_BaseController_change_size_calls_master_geometry(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch(
            "arrangeit.base.BaseController.check_current_size", return_value=False
        )
        mocker.patch("arrangeit.base.BaseController.check_snapping", return_value=False)
        controller = controller_mocked_app(mocker)
        controller.state = Settings.RESIZE
        controller.model = base.WindowModel(rect=(100, 100, 100, 100))
        controller.change_size(100, 100)
        view.return_value.master.geometry.assert_called_once()

    @pytest.mark.parametrize(
        "state,x,y,changed_x,changed_y,expected",
        [
            (Settings.RESIZE, 300, 400, 700, 600, "410x210+290+390"),
            (Settings.RESIZE + 1, 300, 400, 100, 700, "210x310+100+390"),
            (Settings.RESIZE + 2, 300, 400, 100, 200, "210x210+100+200"),
            (Settings.RESIZE + 3, 300, 400, 550, 200, "260x210+290+200"),
        ],
    )
    def test_BaseController_change_size_valid_x_and_y(
        self, mocker, state, x, y, changed_x, changed_y, expected
    ):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.check_snapping", return_value=False)
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        screen_w, screen_h = 2000, 2000
        view.return_value.master.winfo_screenwidth.return_value = screen_w
        view.return_value.master.winfo_screenheight.return_value = screen_h
        SHIFT = 10
        type(mocked_settings).SHIFT_CURSOR = mocker.PropertyMock(return_value=SHIFT)
        type(mocked_settings).MIN_WIDTH = mocker.PropertyMock(return_value=100)
        type(mocked_settings).MIN_HEIGHT = mocker.PropertyMock(return_value=100)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        controller = controller_mocked_app(mocker)
        controller.state = state
        w, h = 400, 400
        controller.model = base.WindowModel(rect=(x, y, w, h))
        controller.model.set_changed(x=changed_x, y=changed_y)
        controller.change_size(x, y)
        assert view.return_value.master.geometry.call_count == 1
        view.return_value.master.geometry.assert_called_with(expected)

    @pytest.mark.parametrize(
        "state,x,y,changed_x,changed_y,expected",
        [
            (Settings.RESIZE, 10, 10, 420, 450, "420x450+0+0"),
            (Settings.RESIZE + 1, 1200, 10, 240, 250, "760x250+240+0"),
            (Settings.RESIZE + 2, 1200, 1200, 240, 250, "760x750+240+250"),
            (Settings.RESIZE + 3, 10, 1200, 240, 250, "240x750+0+250"),
        ],
    )
    def test_BaseController_change_size_with_min_valid_x_and_y(
        self, mocker, state, x, y, changed_x, changed_y, expected
    ):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.BaseController.check_snapping", return_value=False)
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        screen_w, screen_h = 1000, 1000
        view.return_value.master.winfo_screenwidth.return_value = screen_w
        view.return_value.master.winfo_screenheight.return_value = screen_h
        SHIFT = 10
        type(mocked_settings).SHIFT_CURSOR = mocker.PropertyMock(return_value=SHIFT)
        type(mocked_settings).MIN_WIDTH = mocker.PropertyMock(return_value=100)
        type(mocked_settings).MIN_HEIGHT = mocker.PropertyMock(return_value=100)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        controller = controller_mocked_app(mocker)
        controller.state = state
        w, h = 800, 800
        controller.model = base.WindowModel(rect=(x, y, w, h))
        controller.model.set_changed(x=changed_x, y=changed_y)
        controller.change_size(x, y)
        assert view.return_value.master.geometry.call_count == 1
        view.return_value.master.geometry.assert_called_with(expected)

    ## BaseController.check_current_size
    @pytest.mark.parametrize(
        "corner,x,y,changed",
        [
            (0, 25, 25, (120, 120, 120, 120)),
            (1, 220, 25, (120, 120, 120, 120)),
            (2, 220, 220, (120, 120, 120, 120)),
            (3, 25, 235, (120, 120, 120, 120)),
        ],
    )
    def test_BaseController_check_current_size_for_valid_xy_returns_False(
        self, mocker, corner, x, y, changed
    ):
        mocked_setup(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).changed_x = mocker.PropertyMock(
            return_value=changed[0]
        )
        type(model.return_value).changed_y = mocker.PropertyMock(
            return_value=changed[1]
        )
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        MIN_W, MIN_H = 100, 100
        type(mocked_settings).MIN_WIDTH = mocker.PropertyMock(return_value=MIN_W)
        type(mocked_settings).MIN_HEIGHT = mocker.PropertyMock(return_value=MIN_H)
        type(mocked_settings).SHIFT_CURSOR = mocker.PropertyMock(return_value=10)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        controller = controller_mocked_app(mocker)
        controller.state = Settings.RESIZE + corner
        assert controller.check_current_size(x, y) is False

    @pytest.mark.parametrize(
        "corner,x,y,changed,expected",
        [
            (0, 215, 205, (300, 300, 300, 300), (200, 200)),
            (0, 205, 215, (300, 300, 300, 300), (200, 200)),
            (0, 215, 215, (300, 300, 300, 300), (200, 200)),
            (1, 385, 205, (300, 300, 300, 300), (300, 200)),
            (1, 395, 215, (300, 300, 300, 300), (300, 200)),
            (1, 385, 215, (300, 300, 300, 300), (300, 200)),
            (2, 385, 395, (300, 300, 300, 300), (300, 300)),
            (2, 395, 385, (300, 300, 300, 300), (300, 300)),
            (2, 385, 385, (300, 300, 300, 300), (300, 300)),
            (3, 215, 395, (300, 300, 300, 300), (200, 300)),
            (3, 205, 385, (300, 300, 300, 300), (200, 300)),
            (3, 215, 395, (300, 300, 300, 300), (200, 300)),
        ],
    )
    def test_BaseController_check_current_size_for_invalid_xy_returns_position(
        self, mocker, corner, x, y, changed, expected
    ):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.set_minimum_size")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).changed_x = mocker.PropertyMock(
            return_value=changed[0]
        )
        type(model.return_value).changed_y = mocker.PropertyMock(
            return_value=changed[1]
        )
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        MIN_W, MIN_H = 100, 100
        type(mocked_settings).MIN_WIDTH = mocker.PropertyMock(return_value=MIN_W)
        type(mocked_settings).MIN_HEIGHT = mocker.PropertyMock(return_value=MIN_H)
        type(mocked_settings).SHIFT_CURSOR = mocker.PropertyMock(return_value=10)
        type(mocked_settings).RESIZE = mocker.PropertyMock(return_value=10)
        controller = controller_mocked_app(mocker)
        controller.state = Settings.RESIZE + corner
        assert controller.check_current_size(x, y) == expected

    ## BaseController.cycle_corners
    def test_BaseController_cycle_corners_calls_setup_corner(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.setup_corner")
        controller = controller_mocked_app(mocker)
        controller.state = Settings.LOCATE
        controller.cycle_corners()
        mocked.assert_called_once()

    def test_BaseController_cycle_corners_not_calling_setup_corner(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.setup_corner")
        controller = controller_mocked_app(mocker)
        controller.state = Settings.RESIZE
        controller.cycle_corners()
        mocked.assert_not_called()
        controller.state = Settings.OTHER
        controller.cycle_corners()
        mocked.assert_not_called()

    @pytest.mark.parametrize(
        "state,expected", [(0, 1), (1, 2), (3, 0), (14, 14), (11, 11), (104, 104)]
    )
    def test_BaseController_cycle_corners_counter_false_functionality(
        self, mocker, state, expected
    ):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.setup_corner")
        controller = controller_mocked_app(mocker)
        controller.state = state
        controller.cycle_corners(counter=False)
        assert controller.state == expected

    @pytest.mark.parametrize(
        "state,expected", [(0, 3), (1, 0), (3, 2), (14, 14), (11, 11), (104, 104)]
    )
    def test_BaseController_cycle_corners_counter_true_functionality(
        self, mocker, state, expected
    ):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.setup_corner")
        controller = controller_mocked_app(mocker)
        controller.state = state
        controller.cycle_corners(counter=True)
        assert controller.state == expected

    ## BaseController.get_root_rect
    @pytest.mark.parametrize(
        "state,expected",
        [
            (Settings.LOCATE, (190, 290, 100, 100)),
            (Settings.LOCATE + 1, (110, 290, 100, 100)),
            (Settings.LOCATE + 2, (110, 210, 100, 100)),
            (Settings.LOCATE + 3, (190, 210, 100, 100)),
            (Settings.RESIZE, (190, 290, 100, 100)),
            (Settings.RESIZE + 1, (110, 290, 100, 100)),
            (Settings.RESIZE + 2, (110, 210, 100, 100)),
            (Settings.RESIZE + 3, (190, 210, 100, 100)),
        ],
    )
    def test_BaseController_get_root_rect_functionality(self, mocker, state, expected):
        view = mocked_setup_view(mocker)
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        SHIFT = 10
        type(mocked_settings).SHIFT_CURSOR = mocker.PropertyMock(return_value=SHIFT)
        x, y, w, h = 200, 300, 100, 100
        view.return_value.master.winfo_width.return_value = w
        view.return_value.master.winfo_height.return_value = h
        controller = controller_mocked_app(mocker)
        controller.state = state
        assert controller.get_root_rect(x, y) == expected

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
        controller.model = base.WindowModel(rect=(50, 50, 100, 100))
        controller.place_on_top_left()
        calls = [mocker.call(cursor=Settings.CORNER_CURSOR[0])]
        view.return_value.master.config.assert_has_calls(calls, any_order=True)

    def test_BaseController_place_on_top_left_calls_move_cursor(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        mocked = mocker.patch("arrangeit.base.move_cursor")
        x, y = 101, 202
        mocked_settings = mocker.patch("arrangeit.base.Settings")
        SHIFT = 10
        type(mocked_settings).SHIFT_CURSOR = mocker.PropertyMock(return_value=SHIFT)
        controller = controller_mocked_app(mocker)
        controller.model = data.WindowModel(rect=(x, y, 100, 100))
        controller.place_on_top_left()
        mocked.assert_called_with(x + SHIFT, y + SHIFT)

    ## BaseController.place_on_opposite_corner
    def test_BaseController_place_on_opposite_corner_calls_cursor_config(self, mocker):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.move_cursor")
        mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        controller = controller_mocked_app(mocker)
        controller.default_size = (2000, 2000)
        controller.model = base.WindowModel(rect=(50, 50, 100, 100))
        controller.state = Settings.RESIZE
        controller.place_on_opposite_corner()
        calls = [mocker.call(cursor=Settings.CORNER_CURSOR[controller.state % 10])]
        view.return_value.master.config.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize(
        "state,x,y,w,h,expected_x,expected_y",
        [
            (Settings.RESIZE, 700, 550, 400, 300, 310, 260),
            (Settings.RESIZE + 1, 202, 580, 208, 300, 400, 290),
            (Settings.RESIZE + 2, 201, 202, 203, 204, 394, 396),
            (Settings.RESIZE + 3, 700, 300, 400, 500, 310, 790),
        ],
    )
    def test_BaseController_place_on_opposite_corner_calls_move_cursor(
        self, mocker, state, x, y, w, h, expected_x, expected_y
    ):
        view = mocked_setup_view(mocker)
        screen_w, screen_h = 2000, 2000
        view.return_value.master.winfo_screenwidth.return_value = screen_w
        view.return_value.master.winfo_screenheight.return_value = screen_h
        mocked = mocker.patch("arrangeit.base.move_cursor")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).changed_x = mocker.PropertyMock(return_value=x)
        type(model.return_value).changed_y = mocker.PropertyMock(return_value=y)
        type(model.return_value).w = mocker.PropertyMock(return_value=w)
        type(model.return_value).h = mocker.PropertyMock(return_value=h)
        mocked_setting = mocker.patch("arrangeit.base.Settings")
        SHIFT = 10
        type(mocked_setting).SHIFT_CURSOR = mocker.PropertyMock(return_value=SHIFT)
        type(mocked_setting).RESIZE = mocker.PropertyMock(return_value=10)
        controller = controller_mocked_app(mocker)
        controller.state = state
        controller.place_on_opposite_corner()
        mocked.assert_called_with(expected_x, expected_y)

    @pytest.mark.parametrize(
        "state,x,y,w,h,expected_x,expected_y",
        [
            (Settings.RESIZE, 201, 202, 1400, 1500, 10, 10),
            (Settings.RESIZE + 1, 201, 202, 1400, 1500, 990, 10),
            (Settings.RESIZE + 2, 201, 202, 1400, 1500, 990, 1000),
            (Settings.RESIZE + 3, 201, 202, 1400, 1500, 10, 1000),
        ],
    )
    def test_BaseController_place_on_opposite_corner_calls_min_move_cursor(
        self, mocker, state, x, y, w, h, expected_x, expected_y
    ):
        view = mocked_setup_view(mocker)
        screen_w, screen_h = 1000, 1010
        view.return_value.master.winfo_screenwidth.return_value = screen_w
        view.return_value.master.winfo_screenheight.return_value = screen_h
        mocked = mocker.patch("arrangeit.base.move_cursor")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).changed_x = mocker.PropertyMock(return_value=x)
        type(model.return_value).changed_y = mocker.PropertyMock(return_value=y)
        type(model.return_value).w = mocker.PropertyMock(return_value=w)
        type(model.return_value).h = mocker.PropertyMock(return_value=h)
        mocked_setting = mocker.patch("arrangeit.base.Settings")
        SHIFT = 10
        type(mocked_setting).SHIFT_CURSOR = mocker.PropertyMock(return_value=SHIFT)
        type(mocked_setting).RESIZE = mocker.PropertyMock(return_value=10)
        controller = controller_mocked_app(mocker)
        controller.state = state
        controller.place_on_opposite_corner()
        mocked.assert_called_with(expected_x, expected_y)

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
        calls = [mocker.call(cursor=Settings.CORNER_CURSOR[0])]
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
        mocked_setting = mocker.patch("arrangeit.base.Settings")
        SHIFT = 10
        type(mocked_setting).SHIFT_CURSOR = mocker.PropertyMock(return_value=SHIFT)
        controller = controller_mocked_app(mocker)
        controller.recapture_mouse()
        mocked.assert_called_once()
        mocked.assert_called_with(
            view.return_value.master.winfo_x.return_value + SHIFT,
            view.return_value.master.winfo_y.return_value + SHIFT,
        )

    def test_BaseController_recapture_mouse_calls_get_mouse_listener(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        mocker.patch("arrangeit.base.move_cursor")
        mocked = mocker.patch("arrangeit.base.get_mouse_listener")
        controller = controller_mocked_app(mocker)
        controller.recapture_mouse()
        mocked.assert_called_once()
        mocked.assert_called_with(controller.on_mouse_move, controller.on_mouse_scroll)

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

    ## BaseController.set_minimum_size
    def test_BaseController_set_minimum_size_functionality(self, mocker):
        view = mocked_setup_view(mocker)
        x, y = 505, 509
        controller = controller_mocked_app(mocker)
        controller.set_minimum_size(x, y)
        assert view.return_value.master.geometry.call_count == 1
        view.return_value.master.geometry.assert_called_with(
            "{}x{}+{}+{}".format(Settings.MIN_WIDTH, Settings.MIN_HEIGHT, x, y)
        )

    ## BaseController.setup_corner
    @pytest.mark.parametrize("state", [0, 1, 2, 3])
    def test_BaseController_setup_corner_calls_cursor_config(self, mocker, state):
        view = mocked_setup_view(mocker)
        mocker.patch("arrangeit.base.move_cursor")
        controller = controller_mocked_app(mocker)
        controller.state = state
        controller.setup_corner()
        calls = [mocker.call(cursor=Settings.CORNER_CURSOR[state])]
        view.return_value.master.config.assert_has_calls(calls, any_order=True)

    def test_BaseController_setup_corner_calls_move_cursor_state_0(self, mocker):
        view = mocked_setup_view(mocker)
        x, y = 170, 171
        view.return_value.master.winfo_x.return_value = x
        view.return_value.master.winfo_y.return_value = y
        controller = controller_mocked_app(mocker)
        mocked = mocker.patch("arrangeit.base.move_cursor")
        controller.state = 0
        controller.setup_corner()
        mocked.assert_called_once()
        mocked.assert_called_with(x + Settings.SHIFT_CURSOR, y + Settings.SHIFT_CURSOR)

    def test_BaseController_setup_corner_calls_move_cursor_state_1(self, mocker):
        view = mocked_setup_view(mocker)
        x, y, w = 172, 173, 405
        view.return_value.master.winfo_x.return_value = x
        view.return_value.master.winfo_y.return_value = y
        view.return_value.master.winfo_width.return_value = w
        controller = controller_mocked_app(mocker)
        mocked = mocker.patch("arrangeit.base.move_cursor")
        controller.state = 1
        controller.setup_corner()
        mocked.assert_called_once()
        mocked.assert_called_with(
            x + w - Settings.SHIFT_CURSOR, y + Settings.SHIFT_CURSOR
        )

    def test_BaseController_setup_corner_calls_move_cursor_state_2(self, mocker):
        view = mocked_setup_view(mocker)
        x, y, w, h = 174, 175, 406, 507
        view.return_value.master.winfo_x.return_value = x
        view.return_value.master.winfo_y.return_value = y
        view.return_value.master.winfo_width.return_value = w
        view.return_value.master.winfo_height.return_value = h
        controller = controller_mocked_app(mocker)
        mocked = mocker.patch("arrangeit.base.move_cursor")
        controller.state = 2
        controller.setup_corner()
        mocked.assert_called_once()
        mocked.assert_called_with(
            x + w - Settings.SHIFT_CURSOR, y + h - Settings.SHIFT_CURSOR
        )

    def test_BaseController_setup_corner_calls_move_cursor_state_3(self, mocker):
        view = mocked_setup_view(mocker)
        x, y, h = 176, 177, 508
        view.return_value.master.winfo_x.return_value = x
        view.return_value.master.winfo_y.return_value = y
        view.return_value.master.winfo_height.return_value = h
        controller = controller_mocked_app(mocker)
        mocked = mocker.patch("arrangeit.base.move_cursor")
        controller.state = 3
        controller.setup_corner()
        mocked.assert_called_once()
        mocked.assert_called_with(
            x + Settings.SHIFT_CURSOR, y + h - Settings.SHIFT_CURSOR
        )

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
        mocker.patch("arrangeit.base.cursor_position", return_value=(x, y))
        mocked = mocker.patch("arrangeit.base.BaseController.update")
        controller_mocked_key_press(mocker, key)
        mocked.assert_called_with(x, y)

    @pytest.mark.parametrize("key", ["Space", "Tab"])
    def test_BaseController_on_key_pressed_calls_skip_current_window(self, mocker, key):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.skip_current_window")
        controller_mocked_key_press(mocker, key)
        assert mocked.call_count == 1

    @pytest.mark.parametrize("key", ["Alt_L", "Alt_R", "Shift_L", "Shift_R"])
    def test_BaseController_on_key_pressed_calls_release_mouse(self, mocker, key):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.release_mouse")
        controller_mocked_key_press(mocker, key)
        assert mocked.call_count == 1

    @pytest.mark.parametrize("key", ["Control_L", "Control_R"])
    def test_BaseController_on_key_pressed_calls_cycle_corners(self, mocker, key):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.cycle_corners")
        controller_mocked_key_press(mocker, key)
        assert mocked.call_count == 1
        mocked.assert_called_with()

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
        mocker.patch("arrangeit.base.cursor_position", return_value=(x, y))
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

    ## BaseController.on_mouse_scroll
    def test_BaseController_on_mouse_scroll_calls_counter_true_cycle_corners(
        self, mocker
    ):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.cycle_corners")
        base.BaseController(mocker.MagicMock()).on_mouse_scroll(0, 0, 0, 1)
        assert mocked.call_count == 1
        mocked.assert_called_with(counter=True)

    def test_BaseController_on_mouse_scroll_calls_counter_false_cycle_corners(
        self, mocker
    ):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.cycle_corners")
        base.BaseController(mocker.MagicMock()).on_mouse_scroll(0, 0, 0, -1)
        assert mocked.call_count == 1
        mocked.assert_called_with(counter=False)

    def test_BaseController_on_mouse_scroll_returns_break(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.cycle_corners")
        returned = base.BaseController(mocker.MagicMock()).on_mouse_scroll(0, 0, 0, 1)
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

    ## BaseController.on_focus
    def test_BaseController_on_focus_calls_focus_get(self, mocker):
        view = mocked_setup_view(mocker)
        base.BaseController(mocker.MagicMock()).on_focus(mocker.MagicMock())
        assert view.return_value.focus_get.call_count == 1

    def test_BaseController_on_focus_calls_run_task_activate_root(self, mocker):
        view = mocked_setup_view(mocker)
        view.return_value.focus_get.return_value = None
        app = mocker.MagicMock()
        base.BaseController(app).on_focus(mocker.MagicMock())
        app.run_task.assert_called_once()
        app.run_task.assert_called_with(
            "activate_root", view.return_value.master.winfo_id.return_value
        )

    def test_BaseController_on_focus_returns_break(self, mocker):
        view = mocked_setup_view(mocker)
        view.return_value.focus_get.return_value = None
        app = mocker.MagicMock()
        returned = base.BaseController(app).on_focus(mocker.MagicMock())
        assert returned == "break"

    def test_BaseController_on_focus_not_calling_run_task(self, mocker):
        view = mocked_setup_view(mocker)
        view.return_value.focus_get.return_value = "foo"
        app = mocker.MagicMock()
        base.BaseController(app).on_focus(mocker.MagicMock())
        app.run_task.assert_not_called()

    def test_BaseController_on_focus_not_returns_break(self, mocker):
        view = mocked_setup_view(mocker)
        view.return_value.focus_get.return_value = "foo"
        app = mocker.MagicMock()
        returned = base.BaseController(app).on_focus(mocker.MagicMock())
        assert returned == None

    ## BaseController.mainloop
    def test_BaseController_mainloop_calls_Tkinter_mainloop(self, mocker):
        view = mocked_setup_view(mocker)
        base.BaseController(mocker.MagicMock()).mainloop()
        assert view.return_value.mainloop.call_count == 1
