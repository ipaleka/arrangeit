import pytest

from arrangeit import base, constants, data


def mock_main_loop(mocker):
    mocker.patch("arrangeit.base.get_tkinter_root")
    mocker.patch("arrangeit.base.ViewApplication")
    mocker.patch("arrangeit.base.BaseController.mainloop")
    mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
    mocker.patch("pynput.mouse.Listener")
    mocker.patch("pynput.mouse.Controller")
    mocker.patch("arrangeit.base.BaseApp.run_task")
    mocker.patch("arrangeit.base.BaseApp.grab_window_screen")


def get_mocked_root(mocker):
    mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
    mocker.patch("arrangeit.base.ViewApplication")
    return mocker.patch("arrangeit.base.get_tkinter_root")


def get_mocked_viewapp(mocker):
    mocker.patch("arrangeit.base.get_tkinter_root")
    mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
    return mocker.patch("arrangeit.base.ViewApplication")


def mocked_viewapp(mocker):
    mocker.patch("arrangeit.base.get_tkinter_root")
    mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
    mocker.patch("arrangeit.base.ViewApplication")


def mocked_next(mocker):
    mocker.patch("arrangeit.base.get_tkinter_root")
    mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
    mocker.patch("arrangeit.base.ViewApplication")
    mocker.patch("arrangeit.base.BaseController.next")


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
        ],
    )
    def test_BaseController_inits_attr_as_None(self, attr):
        assert getattr(base.BaseController, attr) is None

    ## BaseController.__init__
    def test_BaseController_init_sets_app_attribute(self, mocker):
        mock_main_loop(mocker)
        app = mocker.MagicMock()
        controller = base.BaseController(app)
        assert controller.app == app

    def test_BaseController_initialization_instantiates_WindowModel(self, mocker):
        controller = base.BaseController(mocker.MagicMock())
        assert getattr(controller, "model", None) is not None
        assert isinstance(getattr(controller, "model"), data.WindowModel)

    def test_BaseController_initialization_calls_setup(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseController.setup")
        base.BaseController(mocker.MagicMock())
        mocked.assert_called_once()

    ## BaseController.setup
    def test_BaseController_setup_calls_get_tkinter_root(self, mocker):
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
        mocked = mocker.patch("arrangeit.base.get_tkinter_root")
        controller = base.BaseController(mocker.MagicMock())
        mocked.call_count = 0
        controller.setup()
        assert mocked.call_count == 1

    def test_BaseController_setup_calls_get_screenshot_widget(self, mocker):
        root = get_mocked_root(mocker)
        mocked = mocker.patch("arrangeit.base.get_screenshot_widget")
        controller = base.BaseController(mocker.MagicMock())
        mocked.call_count = 0
        controller.setup()
        assert mocked.call_count == 1
        mocked.assert_called_with(root.return_value)

    def test_BaseController_setup_calls_setup_root_window(self, mocker):
        root = mocker.MagicMock()
        mocker.patch("arrangeit.base.get_tkinter_root", return_value=root)
        mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseController.setup_root_window")
        controller = base.BaseController(mocker.MagicMock())
        mocked.call_count = 0
        controller.setup()
        assert mocked.call_count == 1
        mocked.assert_called_with(root)

    def test_BaseController_setup_initializes_ViewApplication(self, mocker):
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        mocked.call_count = 0
        controller.setup()
        assert mocked.call_count == 1

    def test_BaseController_setup_initializes_ViewApplication_with_right_args(
        self, mocker
    ):
        root = mocker.MagicMock()
        mocker.patch("arrangeit.base.get_tkinter_root", return_value=root)
        mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        mocked.assert_called_with(master=root, controller=controller)

    def test_BaseController_setup_withdraws_root_tk_window(self, mocker):
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
        mocked = mocker.patch("arrangeit.view.tk.Tk")
        controller = base.BaseController(mocker.MagicMock())
        mocked.return_value.withdraw.call_count = 0
        controller.setup()
        assert mocked.return_value.withdraw.call_count == 1

    ## BaseController.setup_root_window
    def test_BaseController_setup_root_window_calls_wm_attributes(self, mocker):
        root = get_mocked_root(mocker)
        base.BaseController(mocker.MagicMock()).setup_root_window(root)
        assert root.wm_attributes.call_count == 2
        calls = [
            mocker.call("-alpha", constants.ROOT_ALPHA),
            mocker.call("-topmost", True),
        ]
        root.wm_attributes.assert_has_calls(calls, any_order=True)

    ## BaseController.set_default_geometry
    def test_BaseController_set_default_geometry_calls_quarter_by_smaller(self, mocker):
        root = mocker.patch("arrangeit.base.get_tkinter_root")
        mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch(
            "arrangeit.base.quarter_by_smaller", return_value=(100, 100)
        )
        width, height = 1200, 1000
        root.winfo_screenwidth.return_value = width
        root.winfo_screenheight.return_value = height
        controller = base.BaseController(mocker.MagicMock())
        controller.set_default_geometry(root)
        assert mocked.call_count == 1
        mocked.assert_called_with(width, height)

    def test_BaseController_set_default_geometry_calls_geometry(self, mocker):
        root = get_mocked_root(mocker)
        base.BaseController(mocker.MagicMock()).set_default_geometry(root)
        assert root.geometry.call_count == 1
        root.geometry.assert_called_with("100x100")

    ## BaseController.prepare_view
    def test_BaseController_prepare_view_calls_WorkspacesCollection_add_workspaces(
        self, mocker
    ):
        view = get_mocked_viewapp(mocker)
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
        view = get_mocked_viewapp(mocker)
        app = mocker.MagicMock()
        app.collector.collection.get_windows_list.return_value = [1, 2]
        base.BaseController(app).prepare_view()
        assert view.return_value.windows.add_windows.call_count == 1
        calls = [mocker.call([2])]
        view.return_value.windows.add_windows.assert_has_calls(calls, any_order=True)

    ## BaseController.change_position
    def test_BaseController_change_position(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        x, y = 100, 200
        controller = base.BaseController(mocker.MagicMock())
        controller.change_position(x, y)
        assert mocked.return_value.master.geometry.call_count == 1
        mocked.return_value.master.geometry.assert_called_with(
            "+{}+{}".format(
                x,
                y,
            )
        )

    ## BaseController.change_size
    def test_BaseController_change_size_valid_x_and_y(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).changed_x = mocker.PropertyMock(return_value=100)
        type(model.return_value).changed_y = mocker.PropertyMock(return_value=200)
        x, y = 300, 400
        controller = base.BaseController(mocker.MagicMock())
        controller.change_size(x, y)
        assert mocked.return_value.master.geometry.call_count == 1
        mocked.return_value.master.geometry.assert_called_with(
            "{}x{}".format(
                x - 100 + constants.WINDOW_SHIFT_PIXELS,
                y - 200 + constants.WINDOW_SHIFT_PIXELS,
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
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).changed_x = mocker.PropertyMock(
            return_value=changed[0]
        )
        type(model.return_value).changed_y = mocker.PropertyMock(
            return_value=changed[1]
        )
        controller = base.BaseController(mocker.MagicMock())
        controller.change_size(x, y)
        assert mocked.return_value.master.geometry.call_count == 1
        mocked.return_value.master.geometry.assert_called_with(
            "{}x{}".format(constants.WINDOW_MIN_WIDTH, constants.WINDOW_MIN_HEIGHT)
        )

    ## BaseController.listed_window_activated_by_digit
    def test_BaseController_listed_window_activated_by_digit_calls_winfo_children(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocker.patch("arrangeit.base.BaseApp.run_task")
        windows = mocker.patch("arrangeit.view.WindowsList")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel(wid=80001))
        collection.add(data.WindowModel(wid=80002))
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.listed_window_activated_by_digit(2)
        windows.return_value.winfo_children.call_count == 1

    def test_BaseController_listed_window_activated_by_digit_calls_l_window_activated(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        view = mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseController.listed_window_activated")
        mocked_children = [mocker.MagicMock(), mocker.MagicMock()]
        view.return_value.windows.winfo_children.return_value = mocked_children
        type(mocked_children[1]).wid = mocker.PropertyMock(return_value=70001)
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.listed_window_activated_by_digit(2)
        mocked.assert_called_with(70001)

    def test_BaseController_listed_window_activated_by_digit_not_calling_l_win_active(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseController.listed_window_activated")
        mocked_children = [mocker.MagicMock(), mocker.MagicMock()]
        mocker.patch(
            "arrangeit.view.WorkspacesCollection.winfo_children",
            return_value=mocked_children,
        )
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.listed_window_activated_by_digit(3)
        mocked.assert_not_called()

    ## BaseController.place_on_top_left
    def test_BaseController_place_on_top_left_calls_cursor_config(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        controller.place_on_top_left()
        calls = [mocker.call(cursor="ul_angle")]
        mocked.return_value.master.config.assert_has_calls(calls, any_order=True)

    def test_BaseController_place_on_top_left_calls_on_mouse_move(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        collection = data.WindowsCollection()
        rect = (101, 202, 303, 404)
        collection.add(data.WindowModel(rect=rect))
        collection.add(data.WindowModel(rect=rect))
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.place_on_top_left()
        mocked.assert_called_with(rect[0], rect[1])

    def test_BaseController_place_on_top_left_calls_move_cursor(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.move_cursor")
        collection = data.WindowsCollection()
        rect = (101, 202, 303, 404)
        collection.add(data.WindowModel(rect=rect))
        collection.add(data.WindowModel(rect=rect))
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.place_on_top_left()
        mocked.assert_called_with(rect[0], rect[1])

    ## BaseController.place_on_right_bottom
    def test_BaseController_place_on_right_bottom_calls_cursor_config(self, mocker):
        mocked = get_mocked_viewapp(mocker)
        mocker.patch("arrangeit.base.WindowModel.set_changed")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=True)
        model.return_value.wh_from_ending_xy.return_value = (100, 100)
        mocker.patch("arrangeit.base.BaseController.next")
        mocker.patch("arrangeit.base.BaseApp.run_task")
        mocker.patch("arrangeit.base.move_cursor")
        controller = base.BaseController(base.BaseApp())
        controller.place_on_right_bottom()
        calls = [mocker.call(cursor="lr_angle")]
        mocked.return_value.master.config.assert_has_calls(calls, any_order=True)

    def test_BaseController_place_on_right_bottom_calls_move_cursor(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocked = mocker.patch("arrangeit.base.move_cursor")
        collection = data.WindowsCollection()
        rect = (101, 202, 303, 404)
        model = data.WindowModel(rect=rect)
        collection.add(model)
        model.set_changed(rect=rect)
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.place_on_right_bottom()
        mocked.assert_called_with(rect[0] + rect[2], rect[1] + rect[3])

    ## BaseController.remove_listed_window
    def test_BaseController_remove_listed_window_calls_widget_destroy(self, mocker):
        view = get_mocked_viewapp(mocker)
        widget = mocker.MagicMock()
        type(widget).wid = 100
        view.return_value.windows.winfo_children.return_value = [widget]
        controller = base.BaseController(mocker.MagicMock())
        controller.remove_listed_window(100)
        assert widget.destroy.call_count == 1

    def test_BaseController_remove_listed_window_not_calling_destroy_for_wrong_widget(
        self, mocker
    ):
        view = get_mocked_viewapp(mocker)
        widget = mocker.MagicMock()
        type(widget).wid = 100
        view.return_value.windows.winfo_children.return_value = [widget]
        controller = base.BaseController(mocker.MagicMock())
        controller.remove_listed_window(201)
        assert widget.destroy.call_count == 0

    def test_BaseController_remove_listed_window_calls_place_children(self, mocker):
        view = get_mocked_viewapp(mocker)
        widget = mocker.MagicMock()
        type(widget).wid = 100
        view.return_value.windows.winfo_children.return_value = [widget]
        controller = base.BaseController(mocker.MagicMock())
        controller.remove_listed_window(100)
        assert view.return_value.windows.place_children.call_count == 1

    ## BaseController.release_mouse
    def test_BaseController_release_mouse_calls_unbind_events(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        controller.run(mocker.MagicMock())
        controller.release_mouse()
        assert mocked.return_value.unbind_events.call_count == 1

    def test_BaseController_release_mouse_calls_cursor_config(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        controller.run(mocker.MagicMock())
        controller.release_mouse()
        calls = [mocker.call(cursor="left_ptr")]
        mocked.return_value.master.config.assert_has_calls(calls, any_order=True)

    def test_BaseController_release_mouse_changes_state_to_OTHER(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.view.mouse.Listener")
        controller = base.BaseController(mocker.MagicMock())
        controller.run(mocker.MagicMock())
        controller.state = 5
        controller.release_mouse()
        assert controller.state == constants.OTHER

    def test_BaseController_release_mouse_stops_listener(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.view.mouse.Listener")
        controller = base.BaseController(mocker.MagicMock())
        controller.run(mocker.MagicMock())
        controller.release_mouse()
        assert mocked.return_value.stop.call_count == 1

    ## BaseController.recapture_mouse
    def test_BaseController_recapture_mouse_calls_view_setup_bindings(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        controller.recapture_mouse()
        assert mocked.return_value.setup_bindings.call_count == 1

    def test_BaseController_recapture_mouse_calls_cursor_config(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        controller.recapture_mouse()
        calls = [mocker.call(cursor="ul_angle")]
        mocked.return_value.master.config.assert_has_calls(calls, any_order=True)

    def test_BaseController_recapture_mouse_changes_state_to_LOCATE(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.view.mouse.Listener")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = 5
        controller.recapture_mouse()
        assert controller.state == constants.LOCATE

    def test_BaseController_recapture_mouse_calls_move_cursor(self, mocker):
        mock_main_loop(mocker)
        view = mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.move_cursor")
        controller = base.BaseController(mocker.MagicMock())
        controller.recapture_mouse()
        mocked.assert_called_once()
        mocked.assert_called_with(
            view.return_value.master.winfo_x.return_value,
            view.return_value.master.winfo_y.return_value,
        )

    def test_BaseController_recapture_mouse_calls_get_mouse_listener(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.get_mouse_listener")
        controller = base.BaseController(mocker.MagicMock())
        controller.recapture_mouse()
        mocked.assert_called_once()
        mocked.assert_called_with(controller.on_mouse_move)

    def test_BaseController_recapture_mouse_sets_listener_attribute(self, mocker):
        mock_main_loop(mocker)
        listener = mocker.MagicMock()
        mocker.patch("arrangeit.base.get_mouse_listener", return_value=listener)
        controller = base.BaseController(mocker.MagicMock())
        controller.recapture_mouse()
        assert controller.listener == listener

    def test_BaseController_recapture_mouse_starts_listener(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("pynput.mouse.Listener")
        controller = base.BaseController(mocker.MagicMock())
        controller.recapture_mouse()
        assert mocked.return_value.start.call_count == 1

    ## BaseController.shutdown
    def test_BaseController_shutdown_stops_listener(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.view.mouse.Listener")
        controller = base.BaseController(mocker.MagicMock())
        controller.run(mocker.MagicMock())
        controller.shutdown()
        assert mocked.return_value.stop.call_count == 1

    def test_BaseController_shutdown_calls_master_destroy(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        controller.run(mocker.MagicMock())
        controller.shutdown()
        assert mocked.return_value.master.destroy.call_count == 1

    ## BaseController.skip_current_window
    def test_BaseController_skip_current_window_calls_next(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        base.BaseController(mocker.MagicMock()).skip_current_window()
        assert mocked.call_count == 1

    ## BaseController.switch_workspace
    def test_BaseController_switch_workspace_calls_winfo_id(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocker.patch("arrangeit.base.BaseApp.run_task")
        view = mocker.patch("arrangeit.base.ViewApplication")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel(workspace=1001))
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.switch_workspace()
        view.return_value.master.winfo_id.call_count == 1

    def test_BaseController_switch_workspace_calls_task_move_to_workspace(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        view = mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseApp.run_task")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel(workspace=1001))
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.switch_workspace()
        mocked.assert_called_with(
            "move_to_workspace", view.return_value.master.winfo_id.return_value, 1001
        )

    ## BaseController.workspace_activated_by_digit
    def test_BaseController_workspace_activated_by_digit_calls_winfo_children(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocker.patch("arrangeit.base.BaseApp.run_task")
        workspaces = mocker.patch("arrangeit.view.WorkspacesCollection")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel(workspace=1001))
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.workspace_activated_by_digit(1)
        workspaces.return_value.winfo_children.call_count == 1

    def test_BaseController_workspace_activated_by_digit_calls_workspace_activated(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        view = mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseController.workspace_activated")
        mocked_children = [mocker.MagicMock(), mocker.MagicMock()]
        view.return_value.workspaces.winfo_children.return_value = mocked_children
        type(mocked_children[1]).number = mocker.PropertyMock(return_value=1002)
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.workspace_activated_by_digit(2)
        mocked.assert_called_with(1002)

    def test_BaseController_workspace_activated_by_digit_not_calling_workspace_active(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseController.workspace_activated")
        mocked_children = [mocker.MagicMock(), mocker.MagicMock()]
        mocker.patch(
            "arrangeit.view.WorkspacesCollection.winfo_children",
            return_value=mocked_children,
        )
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.workspace_activated_by_digit(3)
        mocked.assert_not_called()

    ## BaseController.on_key_pressed
    def test_BaseController_on_key_pressed_for_Escape_calls_shutdown(self, mocker):
        mocked_viewapp(mocker)
        event = mocker.MagicMock()
        type(event).keysym = mocker.PropertyMock(return_value="Escape")
        mocked = mocker.patch("arrangeit.base.BaseController.shutdown")
        base.BaseController(mocker.MagicMock()).on_key_pressed(event)
        assert mocked.call_count == 1
        mocked.assert_called_with()

    @pytest.mark.parametrize("key", ["Return", "KP_Enter"])
    def test_BaseController_on_key_pressed_for_Enter_calls_update(self, mocker, key):
        view = get_mocked_viewapp(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.update")
        view.return_value.master.winfo_pointerx.return_value = 101
        view.return_value.master.winfo_pointery.return_value = 202
        event = mocker.MagicMock()
        type(event).keysym = mocker.PropertyMock(return_value=key)
        base.BaseController(mocker.MagicMock()).on_key_pressed(event)
        mocked.assert_called_with(101, 202)

    @pytest.mark.parametrize("key", ["Space", "Tab"])
    def test_BaseController_on_key_pressed_calls_skip_current_window(self, mocker, key):
        mocked_viewapp(mocker)
        event = mocker.MagicMock()
        type(event).keysym = mocker.PropertyMock(return_value=key)
        mocked = mocker.patch("arrangeit.base.BaseController.skip_current_window")
        base.BaseController(mocker.MagicMock()).on_key_pressed(event)
        assert mocked.call_count == 1

    @pytest.mark.parametrize("key", ["Control_L"])
    def test_BaseController_on_key_pressed_calls_release_mouse(self, mocker, key):
        mocked_viewapp(mocker)
        event = mocker.MagicMock()
        type(event).keysym = mocker.PropertyMock(return_value=key)
        mocked = mocker.patch("arrangeit.base.BaseController.release_mouse")
        base.BaseController(mocker.MagicMock()).on_key_pressed(event)
        assert mocked.call_count == 1

    @pytest.mark.parametrize("key", ["KP_1", "KP_4", "KP_9", "1", "5", "9"])
    def test_BaseController_on_key_pressed_for_digit_calls_workspace_activated_by_digit(
        self, mocker, key
    ):
        mocked_viewapp(mocker)
        event = mocker.MagicMock()
        type(event).keysym = mocker.PropertyMock(return_value=key)
        mocked = mocker.patch(
            "arrangeit.base.BaseController.workspace_activated_by_digit"
        )
        base.BaseController(mocker.MagicMock()).on_key_pressed(event)
        assert mocked.call_count == 1
        mocked.assert_called_with(int(key[-1]))

    @pytest.mark.parametrize("key", ["KP_0", "0"])
    def test_BaseController_on_key_pressed_for_digit_0_not_calling_workspace_activated_by_digit(
        self, mocker, key
    ):
        mocked_viewapp(mocker)
        event = mocker.MagicMock()
        type(event).keysym = mocker.PropertyMock(return_value="0")
        mocked = mocker.patch(
            "arrangeit.base.BaseController.workspace_activated_by_digit"
        )
        base.BaseController(mocker.MagicMock()).on_key_pressed(event)
        mocked.assert_not_called()

    @pytest.mark.parametrize("key", ["F1", "F4", "F9", "F12"])
    def test_BaseController_on_key_pressed_for_func_keys_c_listed_window_activated_by_d(
        self, mocker, key
    ):
        mocked_viewapp(mocker)
        event = mocker.MagicMock()
        type(event).keysym = mocker.PropertyMock(return_value=key)
        mocked = mocker.patch(
            "arrangeit.base.BaseController.listed_window_activated_by_digit"
        )
        base.BaseController(mocker.MagicMock()).on_key_pressed(event)
        assert mocked.call_count == 1
        mocked.assert_called_with(int(key[1:]))

    def test_BaseController_on_key_pressed_returns_break(self, mocker):
        mocked_viewapp(mocker)
        returned = base.BaseController(mocker.MagicMock()).on_key_pressed(
            mocker.MagicMock()
        )
        assert returned == "break"

    ## BaseController.on_mouse_move
    def test_BaseController_on_mouse_move_calls_change_position_for_None(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.change_position")
        x, y = 100, 200
        controller = base.BaseController(mocker.MagicMock())
        controller.state = None
        controller.on_mouse_move(x, y)
        mocked.assert_called_with(x, y)

    def test_BaseController_on_mouse_move_calls_change_position_for_LOCATE(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.change_position")
        x, y = 100, 200
        controller = base.BaseController(mocker.MagicMock())
        controller.state = constants.LOCATE
        controller.on_mouse_move(x, y)
        mocked.assert_called_with(x, y)

    def test_BaseController_on_mouse_move_calls_change_size_for_RESIZE(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.change_size")
        x, y = 100, 200
        controller = base.BaseController(mocker.MagicMock())
        controller.state = constants.RESIZE
        controller.on_mouse_move(x, y)
        mocked.assert_called_with(x, y)

    ## BaseController.on_mouse_left_down
    def test_BaseController_on_mouse_left_down_calls_update(self, mocker):
        view = get_mocked_viewapp(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.update")
        view.return_value.master.winfo_pointerx.return_value = 101
        view.return_value.master.winfo_pointery.return_value = 202
        base.BaseController(mocker.MagicMock()).on_mouse_left_down(mocker.MagicMock())
        mocked.assert_called_with(101, 202)

    def test_BaseController_on_mouse_left_down_returns_break(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.next")
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        returned = base.BaseController(mocker.MagicMock()).on_mouse_left_down(
            mocker.MagicMock()
        )
        assert returned == "break"

    ## BaseController.on_mouse_middle_down
    def test_BaseController_on_mouse_middle_down_calls_release_mouse(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.release_mouse")
        event = mocker.MagicMock()
        base.BaseController(mocker.MagicMock()).on_mouse_middle_down(event)
        assert mocked.call_count == 1

    ## BaseController.on_mouse_right_down
    def test_BaseController_on_mouse_right_down_calls_skip_current_window(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.skip_current_window")
        base.BaseController(mocker.MagicMock()).on_mouse_right_down(mocker.MagicMock())
        assert mocked.call_count == 1

    def test_BaseController_on_mouse_right_down_returns_break(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.next")
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        returned = base.BaseController(mocker.MagicMock()).on_mouse_right_down(
            mocker.MagicMock()
        )
        assert returned == "break"

    ## BaseController.mainloop
    def test_BaseController_mainloop_calls_Tkinter_mainloop(self, mocker):
        mocked = get_mocked_viewapp(mocker)
        mocker.patch("pynput.mouse.Listener")
        base.BaseController(mocker.MagicMock()).mainloop()
        assert mocked.return_value.mainloop.call_count == 1
