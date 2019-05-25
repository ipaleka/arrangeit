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
        "attr", ["app", "model", "generator", "view", "listener", "state"]
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

    ## BaseController.run
    def test_BaseController_run_calls_prepare_view(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.prepare_view")
        base.BaseController(mocker.MagicMock()).run(mocker.MagicMock())
        mocked.assert_called_once()

    def test_BaseController_run_sets_generator_attr_from_provided_attr(self, mocker):
        mock_main_loop(mocker)
        generator = mocker.MagicMock()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        assert controller.generator == generator

    def test_BaseController_run_calls_next(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        base.BaseController(mocker.MagicMock()).run(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with(first_time=True)

    def test_BaseController_run_calls_get_mouse_listener(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.get_mouse_listener")
        controller = base.BaseController(mocker.MagicMock())
        controller.run(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with(controller.on_mouse_move)

    def test_BaseController_run_sets_listener_attribute(self, mocker):
        mock_main_loop(mocker)
        listener = mocker.MagicMock()
        mocker.patch("arrangeit.base.get_mouse_listener", return_value=listener)
        controller = base.BaseController(mocker.MagicMock())
        controller.run(mocker.MagicMock())
        assert controller.listener == listener

    def test_BaseController_run_starts_listener(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("pynput.mouse.Listener")
        base.BaseController(mocker.MagicMock()).run(mocker.MagicMock())
        assert mocked.return_value.start.call_count == 1

    def test_BaseController_run_calls_click_left(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.click_left")
        base.BaseController(mocker.MagicMock()).run(mocker.MagicMock())
        mocked.assert_called_once()

    def test_BaseController_run_calls_mainloop(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.mainloop")
        base.BaseController(mocker.MagicMock()).run(mocker.MagicMock())
        mocked.assert_called_once()

    ## BaseController.next
    def test_BaseController_next_runs_generator(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        collection = data.WindowsCollection()
        model_instance1 = data.WindowModel()
        model_instance2 = data.WindowModel()
        collection.add(data.WindowModel())
        collection.add(model_instance1)
        collection.add(data.WindowModel())
        collection.add(model_instance2)
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        next_value = next(generator)
        assert next_value == model_instance1
        controller.next()
        next_value = next(generator)
        assert next_value == model_instance2

    def test_BaseController_next_sets_state_to_LOCATE(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.state = 5
        controller.next()
        assert controller.state == constants.LOCATE

    def test_BaseController_next_calls_switch_workspace(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocked = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel(workspace=1001))
        collection.add(data.WindowModel(workspace=1002))
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.next()
        assert mocked.call_count == 1

    def test_BaseController_next_not_calling_switch_workspace(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocked = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        collection = data.WindowsCollection()
        model = data.WindowModel(workspace=1005)
        collection.add(model)
        model.set_changed(ws=1006)
        collection.add(data.WindowModel(workspace=1006))
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.next()
        mocked.assert_not_called()

    def test_BaseController_next_calls_set_default_geometry(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        view = mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.next()
        mocked.assert_called_with(view.return_value.master)

    def test_BaseController_next_calls_place_on_top_left(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.next()
        mocked.assert_called()

    def test_BaseController_next_calls_update_widgets(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        model = data.WindowModel()
        collection.add(model)
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.next()
        mocked.return_value.update_widgets.assert_called_with(model)

    def test_BaseController_next_calls_run_task_save_default_on_StopIteration(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocked = mocker.patch("arrangeit.base.BaseApp.run_task")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.next()
        mocked.assert_not_called()
        controller.next()
        mocked.assert_called_once()
        mocked.assert_called_with("save_default")

    def test_BaseController_next_calls_shutdown_on_StopIteration(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocked = mocker.patch("arrangeit.base.BaseController.shutdown")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.next()
        mocked.assert_not_called()
        controller.next()
        mocked.assert_called_once()

    def test_BaseController_next_returns_True_on_StopIteration(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocker.patch("arrangeit.base.BaseController.shutdown")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        returned = controller.next()
        assert not returned
        returned = controller.next()
        assert returned

    ## BaseController.update
    def test_BaseController_update_sets_state_to_LOCATE_for_None(self, mocker):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        model.return_value.wh_from_ending_xy.return_value = (100, 100)
        controller = base.BaseController(base.BaseApp())
        controller.state = None
        controller.update(100, 100)
        assert controller.state == constants.LOCATE

    @pytest.mark.parametrize(
        "state,expected",
        [
            (constants.LOCATE, True),
            (constants.RESIZE, True),
            (constants.OTHER, False),
            (None, False),
            (100, False),
        ],
    )
    def test_BaseController_update_not_calling_set_changed_for_other_states(
        self, mocker, state, expected
    ):
        mocked_next(mocker)
        mocker.patch("arrangeit.base.BaseApp.run_task")
        model = mocker.patch("arrangeit.base.WindowModel")
        mocker.patch("arrangeit.base.move_cursor")
        mocker.patch("arrangeit.base.BaseController.place_on_right_bottom")
        model.return_value.wh_from_ending_xy.return_value = (100, 100)
        controller = base.BaseController(base.BaseApp())
        controller.state = state
        controller.update(100, 100)
        if expected:
            model.return_value.set_changed.assert_called()
        else:
            model.return_value.set_changed.assert_not_called()

    def test_BaseController_update_calls_set_changed_for_LOCATE(self, mocker):
        mocked_next(mocker)
        mocked = mocker.patch("arrangeit.data.WindowModel.set_changed")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = constants.LOCATE
        controller.update(101, 202)
        mocked.assert_called_with(x=101, y=202)

    def test_BaseController_update_calls_run_task_move_window_LOCATE_and_not_resizable(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=False)
        type(model.return_value).wid = mocker.PropertyMock(return_value=2002)
        type(model.return_value).changed = mocker.PropertyMock(return_value=(200, 200))
        mocked = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.LOCATE
        controller.update(101, 202)
        mocked.assert_called_with("move", 2002)

    def test_BaseController_update_calls_run_task_move_window_LOCATE_not_resizable_ws(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=False)
        type(model.return_value).wid = mocker.PropertyMock(return_value=2072)
        type(model.return_value).changed = mocker.PropertyMock(return_value=())
        type(model.return_value).is_ws_changed = mocker.PropertyMock(return_value=True)
        mocked = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.LOCATE
        controller.update(101, 202)
        mocked.assert_called_with("move", 2072)

    def test_BaseController_update_not_calling_run_task_move_window_LOCATE_not_resize(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=False)
        type(model.return_value).wid = mocker.PropertyMock(return_value=2073)
        type(model.return_value).changed = mocker.PropertyMock(return_value=())
        type(model.return_value).is_ws_changed = mocker.PropertyMock(return_value=False)
        mocked = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.LOCATE
        controller.update(101, 202)
        mocked.assert_not_called()

    def test_BaseController_update_calls_next_for_LOCATE_and_not_resizable(
        self, mocker
    ):
        mocked_viewapp(mocker)
        mocker.patch("arrangeit.base.BaseApp.run_task")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=False)
        type(model.return_value).wid = mocker.PropertyMock(return_value=4004)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.LOCATE
        controller.update(101, 202)
        mocked.assert_called()

    def test_BaseController_update_for_LOCATE_and_resizable(self, mocker):
        mocked_viewapp(mocker)
        mocker.patch("arrangeit.base.WindowModel.set_changed")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=True)
        model.return_value.wh_from_ending_xy.return_value = (100, 100)
        mocker.patch("arrangeit.base.move_cursor")
        mocked_next = mocker.patch("arrangeit.base.BaseController.next")
        mocked_move = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.LOCATE
        controller.update(101, 202)
        assert controller.state == constants.RESIZE
        mocked_next.assert_not_called()
        mocked_move.assert_not_called()

    def test_BaseController_update_for_LOCATE_and_resizable_calls_place_on_right_bottom(
        self, mocker
    ):
        mocked = get_mocked_viewapp(mocker)
        mocker.patch("arrangeit.base.WindowModel.set_changed")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=True)
        model.return_value.wh_from_ending_xy.return_value = (100, 100)
        mocker.patch("arrangeit.base.BaseController.next")
        mocked = mocker.patch("arrangeit.base.BaseController.place_on_right_bottom")
        mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.LOCATE
        controller.update(101, 202)
        mocked.assert_called()

    def test_BaseController_update_calls_wh_from_ending_xy_for_RESIZE(self, mocker):
        mocked_next(mocker)
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        mocked = mocker.patch(
            "arrangeit.data.WindowModel.wh_from_ending_xy", return_value=(100, 100)
        )
        controller = base.BaseController(mocker.MagicMock())
        controller.state = constants.RESIZE
        controller.update(304, 406)
        mocked.assert_called_with(304, 406)

    def test_BaseController_update_calls_set_changed_for_RESIZE(self, mocker):
        view = get_mocked_viewapp(mocker)
        mocker.patch("arrangeit.base.BaseController.next")
        view.return_value.master.winfo_pointerx.return_value = 304
        view.return_value.master.winfo_pointery.return_value = 406
        mocker.patch(
            "arrangeit.data.WindowModel.wh_from_ending_xy", return_value=(200, 300)
        )
        mocked = mocker.patch("arrangeit.data.WindowModel.set_changed")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = constants.RESIZE
        controller.update(101, 202)
        mocked.assert_called_with(w=200, h=300)

    def test_BaseController_update_calls_run_task_move_and_resize_window_for_RESIZE(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).wid = mocker.PropertyMock(return_value=5005)
        model.return_value.wh_from_ending_xy.return_value = (100, 100)
        type(model.return_value).changed = mocker.PropertyMock(return_value=(200, 200))
        method = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.RESIZE
        controller.update(101, 202)
        method.assert_called_with("move_and_resize", 5005)

    def test_BaseController_update_calls_run_task_move_and_resize_for_RESIZE_ws(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).wid = mocker.PropertyMock(return_value=5105)
        model.return_value.wh_from_ending_xy.return_value = (None, None)
        type(model.return_value).changed = mocker.PropertyMock(return_value=())
        type(model.return_value).is_ws_changed = mocker.PropertyMock(return_value=True)
        method = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.RESIZE
        controller.update(101, 202)
        method.assert_called_with("move_and_resize", 5105)

    def test_BaseController_update_skips_run_task_move_and_resize_window_for_RESIZE(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).wid = mocker.PropertyMock(return_value=7007)
        model.return_value.wh_from_ending_xy.return_value = (None, None)
        type(model.return_value).changed = mocker.PropertyMock(return_value=())
        type(model.return_value).is_ws_changed = mocker.PropertyMock(return_value=False)
        method = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.RESIZE
        controller.update(101, 202)
        method.assert_not_called()

    def test_BaseController_update_calls_next_for_RESIZE(self, mocker):
        mocked_viewapp(mocker)
        mocker.patch(
            "arrangeit.data.WindowModel.wh_from_ending_xy", return_value=(100, 100)
        )
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        model = mocker.patch("arrangeit.data.WindowModel")
        type(model.return_value).wid = mocker.PropertyMock(return_value=8008)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = constants.RESIZE
        controller.update(101, 202)
        mocked.assert_called()

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
                x - constants.WINDOW_SHIFT_PIXELS, y - constants.WINDOW_SHIFT_PIXELS
            )
        )

    ## BaseController.change_size
    def test_BaseController_change_size_valid_x_and_y(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).changed = mocker.PropertyMock(
            return_value=(100, 200, 300, 400)
        )
        x, y = 300, 400
        controller = base.BaseController(mocker.MagicMock())
        controller.change_size(x, y)
        assert mocked.return_value.master.geometry.call_count == 1
        mocked.return_value.master.geometry.assert_called_with(
            "{}x{}".format(
                x - 100 + constants.WINDOW_SHIFT_PIXELS * 2,
                y - 200 + constants.WINDOW_SHIFT_PIXELS * 2,
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
        type(model.return_value).changed = mocker.PropertyMock(return_value=changed)
        controller = base.BaseController(mocker.MagicMock())
        controller.change_size(x, y)
        assert mocked.return_value.master.geometry.call_count == 1
        mocked.return_value.master.geometry.assert_called_with(
            "{}x{}".format(
                constants.WINDOW_MIN_WIDTH + constants.WINDOW_SHIFT_PIXELS * 2,
                constants.WINDOW_MIN_HEIGHT + constants.WINDOW_SHIFT_PIXELS * 2,
            )
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

    ## BaseController.listed_window_activated
    def test_BaseController_listed_window_activated_calls_task_rerun_from_window(
        self, mocker
    ):
        mocked_next(mocker)
        mocked = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.model.wid = 91405
        controller.listed_window_activated(90102)
        mocked.assert_called_with("rerun_from_window", 90102, 91405)

    def test_BaseController_listed_window_activated_calls_windows_clear_list(
        self, mocker
    ):
        mocked_next(mocker)
        mocker.patch("arrangeit.base.BaseApp.run_task")
        view = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(base.BaseApp())
        controller.listed_window_activated(90108)
        view.return_value.windows.clear_list.assert_called_once()

    def test_BaseController_listed_window_activated_calls_windowslist_add_windows(
        self, mocker
    ):
        mocked_next(mocker)
        mocker.patch("arrangeit.base.BaseApp.run_task")
        view = mocker.patch("arrangeit.base.ViewApplication")
        windows_list = [0, 1, 2]
        mocker.patch(
            "arrangeit.data.WindowsCollection.get_windows_list",
            return_value=windows_list,
        )
        controller = base.BaseController(base.BaseApp())
        controller.listed_window_activated(90209)
        view.return_value.windows.add_windows.assert_called_once()
        view.return_value.windows.add_windows.assert_called_with(windows_list[1:])

    def test_BaseController_listed_window_activated_initializes_generator(self, mocker):
        mocked_next(mocker)
        mocker.patch("arrangeit.base.BaseApp.run_task")
        generator = mocker.patch("arrangeit.data.WindowsCollection.generator")
        controller = base.BaseController(base.BaseApp())
        controller.listed_window_activated(90108)
        generator.assert_called()

    def test_BaseController_listed_window_activated_sets_generator_attr(self, mocker):
        mocked_next(mocker)
        mocker.patch("arrangeit.base.BaseApp.run_task")
        generator = mocker.patch("arrangeit.data.WindowsCollection.generator")
        controller = base.BaseController(base.BaseApp())
        controller.listed_window_activated(90108)
        assert controller.generator == generator.return_value

    def test_BaseController_listed_window_activated_calls_next(self, mocker):
        mocked_viewapp(mocker)
        mocker.patch("arrangeit.base.BaseApp.run_task")
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(mocker.MagicMock())
        controller.listed_window_activated(90423)
        mocked.assert_called_once()
        mocked.assert_called_with(first_time=True)

    def test_BaseController_listed_window_activated_calls_recapture_mouse_for_OTHER(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.BaseApp.run_task")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.state = constants.OTHER
        controller.listed_window_activated(90103)
        mocked.assert_called_once()

    @pytest.mark.parametrize("state", [constants.LOCATE, constants.RESIZE])
    def test_BaseController_listed_window_activated_not_calling_recapture_not_OTHER(
        self, mocker, state
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.BaseApp.run_task")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.state = state
        controller.listed_window_activated(90104)
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
        # mocked = mocker.patch("arrangeit.view.WindowsList.place_children")
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

    ## BaseController.workspace_activated
    def test_BaseController_workspace_activated_calls_task_move_to_workspace(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        view = mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseApp.run_task")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.workspace_activated(1002)
        mocked.assert_called_with(
            "move_to_workspace", view.return_value.master.winfo_id.return_value, 1002
        )

    def test_BaseController_workspace_activated_calls_set_changed(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        view = mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.BaseApp.run_task")
        mocked = mocker.patch("arrangeit.data.WindowModel.set_changed")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.workspace_activated(1503)
        mocked.assert_called_with(ws=1503)

    def test_BaseController_workspace_activated_calls_recapture_mouse_for_OTHER(
        self, mocker
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.BaseApp.run_task")
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.state = constants.OTHER
        controller.workspace_activated(1502)
        mocked.assert_called_once()

    @pytest.mark.parametrize("state", [constants.LOCATE, constants.RESIZE])
    def test_BaseController_workspace_activated_not_calling_recapture_mouse_not_OTHER(
        self, mocker, state
    ):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.BaseApp.run_task")
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(data.WindowModel())
        generator = collection.generator()
        controller = base.BaseController(base.BaseApp())
        controller.run(generator)
        controller.state = state
        controller.workspace_activated(1207)
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

    def test_BaseController_on_key_pressed_for_Enter_calls_update(self, mocker):
        view = get_mocked_viewapp(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.update")
        view.return_value.master.winfo_pointerx.return_value = 101
        view.return_value.master.winfo_pointery.return_value = 202
        event = mocker.MagicMock()
        type(event).keysym = mocker.PropertyMock(return_value="Return")
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
