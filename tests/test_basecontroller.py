import tkinter as tk

import pytest

from arrangeit import base, data
from arrangeit.constants import (
    ROOT_ALPHA,
    WINDOW_SHIFT_PIXELS,
    LOCATE,
    RESIZE,
    OTHER,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
)


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
        mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
        mocked = mocker.patch("arrangeit.base.get_tkinter_root")
        base.BaseController(mocker.MagicMock()).setup()
        assert mocked.call_count == 2

    def test_BaseController_setup_calls_setup_root_window(self, mocker):
        root = mocker.MagicMock()
        mocker.patch("arrangeit.base.get_tkinter_root", return_value=root)
        mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseController.setup_root_window")
        base.BaseController(mocker.MagicMock()).setup()
        assert mocked.call_count == 2
        mocked.assert_called_with(root)

    def test_BaseController_setup_initializes_ViewApplication(self, mocker):
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        base.BaseController(mocker.MagicMock()).setup()
        assert mocked.call_count == 2

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
        mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
        mocked = mocker.patch("arrangeit.view.tk.Tk")
        base.BaseController(mocker.MagicMock()).setup()
        assert mocked.return_value.withdraw.call_count == 2

    ## BaseController.set_geometry
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

    ## BaseController.setup_root_window
    def test_BaseController_setup_root_window_calls_wm_attributes(self, mocker):
        root = get_mocked_root(mocker)
        base.BaseController(mocker.MagicMock()).setup_root_window(root)
        assert root.wm_attributes.call_count == 2
        calls = [mocker.call("-alpha", ROOT_ALPHA), mocker.call("-topmost", True)]
        root.wm_attributes.assert_has_calls(calls, any_order=True)

    ## BaseController.run
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

    @pytest.mark.parametrize("method", ["update", "deiconify"])
    def test_BaseController_run_calls_master_showing_up_method(self, mocker, method):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        base.BaseController(mocker.MagicMock()).run(mocker.MagicMock())
        instance = mocked.return_value.master
        assert getattr(instance, method).call_count == 1

    def test_BaseController_run_calls_focus_set_on_view_frame(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        base.BaseController(mocker.MagicMock()).run(mocker.MagicMock())
        mocked.return_value.focus_set.assert_called_once()

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

    @pytest.mark.parametrize("attr,val,typ", [("title", "foo", tk.StringVar)])
    def test_BaseController_next_sets_attributes_from_gen(self, mocker, attr, val, typ):
        mocker.patch("arrangeit.base.BaseController.mainloop")
        mocker.patch("pynput.mouse.Listener")
        mocker.patch("pynput.mouse.Controller")
        mocker.patch("arrangeit.view.tk.Tk.update")
        mocker.patch("arrangeit.base.BaseController.place_on_top_left")
        model = data.WindowModel(**{attr: val})
        collection = data.WindowsCollection()
        collection.add(data.WindowModel())
        collection.add(model)
        generator = collection.generator()
        controller = base.BaseController(mocker.MagicMock())
        controller.run(generator)
        controller.next()
        instance = getattr(controller.view, attr)
        assert instance.get() == getattr(model, attr)
        assert isinstance(instance, typ)

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
        assert controller.state == LOCATE

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
        assert controller.state == LOCATE

    @pytest.mark.parametrize(
        "state,expected",
        [(LOCATE, True), (RESIZE, True), (OTHER, False), (None, False), (100, False)],
    )
    def test_BaseController_update_not_calling_set_changed_for_other_states(
        self, mocker, state, expected
    ):
        mocked_next(mocker)
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
        controller.state = LOCATE
        controller.update(101, 202)
        mocked.assert_called_with(x=101, y=202)

    def test_BaseController_update_calls_run_task_move_window_LOCATE_and_not_resizable(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=False)
        type(model.return_value).wid = mocker.PropertyMock(return_value=1001)
        mocked = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = LOCATE
        controller.update(101, 202)
        mocked.assert_called_with("move", 1001)

    def test_BaseController_update_calls_next_for_LOCATE_and_not_resizable(
        self, mocker
    ):
        mocked_viewapp(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).resizable = mocker.PropertyMock(return_value=False)
        type(model.return_value).wid = mocker.PropertyMock(return_value=1001)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(base.BaseApp())
        controller.state = LOCATE
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
        controller.state = LOCATE
        controller.update(101, 202)
        assert controller.state == RESIZE
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
        controller.state = LOCATE
        controller.update(101, 202)
        mocked.assert_called()

    def test_BaseController_update_calls_wh_from_ending_xy_for_RESIZE(self, mocker):
        mocked_next(mocker)
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        mocked = mocker.patch(
            "arrangeit.data.WindowModel.wh_from_ending_xy", return_value=(100, 100)
        )
        controller = base.BaseController(mocker.MagicMock())
        controller.state = RESIZE
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
        controller.state = RESIZE
        controller.update(101, 202)
        mocked.assert_called_with(w=200, h=300)

    def test_BaseController_update_calls_run_task_move_and_resize_window_for_RESIZE(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).wid = mocker.PropertyMock(return_value=1001)
        model.return_value.wh_from_ending_xy.return_value = (100, 100)
        type(model.return_value).changed = mocker.PropertyMock(return_value=(200, 200))
        method = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = RESIZE
        controller.update(101, 202)
        method.assert_called_with("move_and_resize", 1001)

    def test_BaseController_update_skips_run_task_move_and_resize_window_for_RESIZE(
        self, mocker
    ):
        mocked_next(mocker)
        model = mocker.patch("arrangeit.base.WindowModel")
        type(model.return_value).wid = mocker.PropertyMock(return_value=1001)
        model.return_value.wh_from_ending_xy.return_value = (None, None)
        type(model.return_value).changed = mocker.PropertyMock(return_value=())
        method = mocker.patch("arrangeit.base.BaseApp.run_task")
        controller = base.BaseController(base.BaseApp())
        controller.state = RESIZE
        controller.update(101, 202)
        method.assert_not_called()

    def test_BaseController_update_calls_next_for_RESIZE(self, mocker):
        mocked_viewapp(mocker)
        mocker.patch(
            "arrangeit.data.WindowModel.wh_from_ending_xy", return_value=(100, 100)
        )
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        model = mocker.patch("arrangeit.data.WindowModel")
        type(model.return_value).wid = mocker.PropertyMock(return_value=1001)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = RESIZE
        controller.update(101, 202)
        mocked.assert_called()

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

    ## BaseController.change_position
    def test_BaseController_change_position(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.ViewApplication")
        x, y = 100, 200
        controller = base.BaseController(mocker.MagicMock())
        controller.change_position(x, y)
        assert mocked.return_value.master.geometry.call_count == 1
        mocked.return_value.master.geometry.assert_called_with(
            "+{}+{}".format(x - WINDOW_SHIFT_PIXELS, y - WINDOW_SHIFT_PIXELS)
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
                x - 100 + WINDOW_SHIFT_PIXELS * 2, y - 200 + WINDOW_SHIFT_PIXELS * 2
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
                WINDOW_MIN_WIDTH + WINDOW_SHIFT_PIXELS * 2,
                WINDOW_MIN_HEIGHT + WINDOW_SHIFT_PIXELS * 2,
            )
        )

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
        controller.state = LOCATE
        controller.on_mouse_move(x, y)
        mocked.assert_called_with(x, y)

    def test_BaseController_on_mouse_move_calls_change_size_for_RESIZE(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.change_size")
        x, y = 100, 200
        controller = base.BaseController(mocker.MagicMock())
        controller.state = RESIZE
        controller.on_mouse_move(x, y)
        mocked.assert_called_with(x, y)

    ## BaseController.on_escape_key_pressed
    def test_BaseController_on_escape_key_pressed_calls_shutdown(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.shutdown")
        base.BaseController(mocker.MagicMock()).on_escape_key_pressed(
            mocker.MagicMock()
        )
        assert mocked.call_count == 1

    ## BaseController.on_mouse_left_down
    def test_BaseController_on_mouse_left_down_calls_update(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.update")
        view = mocker.patch("arrangeit.base.ViewApplication")
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
    def test_BaseController_on_mouse_middle_down_calls_on_mouse_left_down(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.on_mouse_left_down")
        event = mocker.MagicMock()
        base.BaseController(mocker.MagicMock()).on_mouse_middle_down(event)
        assert mocked.call_count == 1
        mocked.assert_called_with(event)

    ## BaseController.on_mouse_right_down
    def test_BaseController_on_mouse_right_down_calls_next(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
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

    ## BaseController.mainloop
    def test_BaseController_mainloop_calls_Tkinter_mainloop(self, mocker):
        mocked = get_mocked_viewapp(mocker)
        mocker.patch("pynput.mouse.Listener")
        base.BaseController(mocker.MagicMock()).mainloop()
        assert mocked.return_value.mainloop.call_count == 1

