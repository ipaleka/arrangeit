import pytest

from arrangeit import base, constants, data

from .test_basecontroller import (
    mock_main_loop,
    get_mocked_viewapp,
    mocked_viewapp,
    mocked_next,
)


class TestBaseControllerDomainLogic(object):
    """Testing class for base Controller class' domain logic methods."""

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

    def test_BaseController_next_calls_grab_window_screen(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        app = mocker.MagicMock()
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        model = data.WindowModel()
        collection.add(model)
        generator = collection.generator()
        controller = base.BaseController(app)
        controller.run(generator)
        controller.next()
        app.grab_window_screen.assert_called_with(model)

    def test_BaseController_next_sets_screenshot_reference_variable(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        app = mocker.MagicMock()
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        model = data.WindowModel()
        collection.add(model)
        generator = collection.generator()
        controller = base.BaseController(app)
        controller.run(generator)
        controller.next()
        assert controller.screenshot == app.grab_window_screen.return_value

    def test_BaseController_next_configures_screenshot_widget(self, mocker):
        mock_main_loop(mocker)
        mocker.patch("arrangeit.base.BaseController.on_mouse_move")
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.base.BaseController.set_default_geometry")
        mocked = mocker.patch("arrangeit.view.tk.Label.configure")
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        app = mocker.MagicMock()
        model = data.WindowModel()
        collection.add(model)
        generator = collection.generator()
        controller = base.BaseController(app)
        controller.run(generator)
        controller.next()
        calls = [mocker.call(image=app.grab_window_screen.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

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

    def test_BaseController_update_calls_update_positioning_for_LOCATE(self, mocker):
        mocked_next(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.update_positioning")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.LOCATE
        controller.update(100, 100)
        assert mocked.call_count == 1
        mocked.assert_called_with(100, 100)

    def test_BaseController_update_calls_update_resizing_for_RESIZE(self, mocker):
        mocked_next(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.update_resizing")
        controller = base.BaseController(base.BaseApp())
        controller.state = constants.RESIZE
        controller.update(100, 100)
        assert mocked.call_count == 1
        mocked.assert_called_with(100, 100)

    @pytest.mark.parametrize("state", [(constants.OTHER, 100, 5000)])
    def test_BaseController_update_not_calling_update_methods_for_other_states(
        self, mocker, state
    ):
        mocked_next(mocker)
        update1 = mocker.patch("arrangeit.base.BaseController.update_positioning")
        update2 = mocker.patch("arrangeit.base.BaseController.update_resizing")
        controller = base.BaseController(base.BaseApp())
        controller.state = state
        controller.update(100, 100)
        update1.assert_not_called()
        update2.assert_not_called()

    ## BaseController.update_positioning
    def test_BaseController_update_positioning_calls_set_changed(self, mocker):
        mocked_next(mocker)
        mocked = mocker.patch("arrangeit.data.WindowModel.set_changed")
        controller = base.BaseController(mocker.MagicMock())
        controller.update_positioning(101, 202)
        mocked.assert_called_with(x=101, y=202)

    def test_BaseController_update_positioning_calls_run_task_move_window_not_resizable(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=False)
        type(model.return_value).wid = mocker.PropertyMock(return_value=2002)
        type(model.return_value).changed = mocker.PropertyMock(return_value=(200, 200))
        mocked = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.update_positioning(101, 202)
        mocked.assert_called_with("move", 2002)

    def test_BaseController_update_positioning_calls_run_task_move_w_not_resizable_ws(
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
        controller.update_positioning(101, 202)
        mocked.assert_called_with("move", 2072)

    def test_BaseController_update_positioning_not_calling_run_task_move_w_not_resize(
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
        controller.update_positioning(101, 202)
        mocked.assert_not_called()

    def test_BaseController_update_positioning_calls_next_for_not_resizable(
        self, mocker
    ):
        mocked_viewapp(mocker)
        mocker.patch("arrangeit.base.BaseApp.run_task")
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=False)
        type(model.return_value).wid = mocker.PropertyMock(return_value=4004)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(base.BaseApp())
        controller.update_positioning(101, 202)
        mocked.assert_called()

    def test_BaseController_update_positioning_for_resizable(self, mocker):
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
        controller.update_positioning(101, 202)
        assert controller.state == constants.RESIZE
        mocked_next.assert_not_called()
        mocked_move.assert_not_called()

    def test_BaseController_update_positioning_for_resizable_calls_place_on_right(
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
        controller.update_positioning(101, 202)
        mocked.assert_called()

    ## BaseController.update_resizing
    def test_BaseController_update_resizing_calls_wh_from_ending_xy(self, mocker):
        mocked_next(mocker)
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        mocked = mocker.patch(
            "arrangeit.data.WindowModel.wh_from_ending_xy", return_value=(100, 100)
        )
        controller = base.BaseController(mocker.MagicMock())
        controller.update_resizing(304, 406)
        mocked.assert_called_with(304, 406)

    def test_BaseController_update_resizing_calls_set_changed(self, mocker):
        view = get_mocked_viewapp(mocker)
        mocker.patch("arrangeit.base.BaseController.next")
        view.return_value.master.winfo_pointerx.return_value = 304
        view.return_value.master.winfo_pointery.return_value = 406
        mocker.patch(
            "arrangeit.data.WindowModel.wh_from_ending_xy", return_value=(200, 300)
        )
        mocked = mocker.patch("arrangeit.data.WindowModel.set_changed")
        controller = base.BaseController(mocker.MagicMock())
        controller.update_resizing(101, 202)
        mocked.assert_called_with(w=200, h=300)

    def test_BaseController_update_resizing_calls_run_task_move_and_resize_window(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).wid = mocker.PropertyMock(return_value=5005)
        model.return_value.wh_from_ending_xy.return_value = (100, 100)
        type(model.return_value).changed = mocker.PropertyMock(return_value=(200, 200))
        method = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.update_resizing(101, 202)
        method.assert_called_with("move_and_resize", 5005)

    def test_BaseController_update_resizing_calls_run_task_move_and_resize_for_ws(
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
        controller.update_resizing(101, 202)
        method.assert_called_with("move_and_resize", 5105)

    def test_BaseController_update_resizing_skips_run_task_move_and_resize_window(
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
        controller.update_resizing(101, 202)
        method.assert_not_called()

    def test_BaseController_update_resizing_calls_next(self, mocker):
        mocked_viewapp(mocker)
        mocker.patch(
            "arrangeit.data.WindowModel.wh_from_ending_xy", return_value=(100, 100)
        )
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        model = mocker.patch("arrangeit.data.WindowModel")
        type(model.return_value).wid = mocker.PropertyMock(return_value=8008)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(mocker.MagicMock())
        controller.update_resizing(101, 202)
        mocked.assert_called()

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
        mocker.patch("arrangeit.base.ViewApplication")
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
