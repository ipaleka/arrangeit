import pytest

from arrangeit import base
from arrangeit.settings import Settings

from .mock_helpers import (
    controller_mocked_for_run,
    controller_mocked_for_next,
    mocked_setup,
    controller_mocked_next,
)


class TestBaseControllerDomainLogic(object):
    """Testing class for base Controller class' domain logic methods."""

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

    def test_BaseController_run_calls_get_mouse_listener(self, mocker):
        controller = controller_mocked_for_run(mocker)
        mocked = mocker.patch("arrangeit.base.get_mouse_listener")
        controller.run(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with(controller.on_mouse_move)

    def test_BaseController_run_sets_listener_attribute(self, mocker):
        controller = controller_mocked_for_run(mocker)
        listener = mocker.MagicMock()
        mocker.patch("arrangeit.base.get_mouse_listener", return_value=listener)
        controller.run(mocker.MagicMock())
        assert controller.listener == listener

    def test_BaseController_run_starts_listener(self, mocker):
        controller = controller_mocked_for_run(mocker)
        controller.run(mocker.MagicMock())
        assert controller.listener.start.call_count == 1

    def test_BaseController_run_calls_click_left(self, mocker):
        controller = controller_mocked_for_run(mocker)
        mocked = mocker.patch("arrangeit.base.click_left")
        controller.run(mocker.MagicMock())
        mocked.assert_called_once()

    def test_BaseController_run_calls_mainloop(self, mocker):
        controller = controller_mocked_for_run(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.mainloop")
        controller.run(mocker.MagicMock())
        mocked.assert_called_once()

    ## BaseController.next
    def test_BaseController_next_runs_generator(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.next(True)
        controller.generator.__next__.assert_called_once()

    def test_BaseController_next_calls_run_task_save_default_on_StopIteration(
        self, mocker
    ):
        controller = controller_mocked_for_next(mocker)
        controller.generator.__next__.side_effect = StopIteration()
        mocker.patch("arrangeit.base.BaseController.shutdown")
        controller.next()
        controller.app.run_task.assert_called_once()
        controller.app.run_task.assert_called_with("save_default")

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

    def test_BaseController_next_sets_state_to_LOCATE(self, mocker):
        controller = controller_mocked_for_next(mocker)
        controller.state = 5
        controller.next()
        assert controller.state == Settings.LOCATE

    def test_BaseController_next_calls_remove_listed_window(self, mocker):
        controller = controller_mocked_for_next(mocker)
        SAMPLE = 4800
        controller.generator.__next__.return_value = base.WindowModel(wid=SAMPLE)
        mocked = mocker.patch("arrangeit.base.BaseController.remove_listed_window")
        mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.next()
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    def test_BaseController_next_calls_switch_workspace(self, mocker):
        controller = controller_mocked_for_next(mocker)
        mocker.patch("arrangeit.base.BaseController.remove_listed_window")
        mocked = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.next()
        mocked.assert_called_once()

    def test_BaseController_next_not_calling_remove_listed_and_switch_workspace_first(
        self, mocker
    ):
        controller = controller_mocked_for_next(mocker)
        mocked_lw = mocker.patch("arrangeit.base.BaseController.remove_listed_window")
        mocked_ws = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.next(True)
        mocked_lw.assert_not_called()
        mocked_ws.assert_not_called()

    def test_BaseController_next_not_calling_switch_workspace(self, mocker):
        controller = controller_mocked_for_next(mocker)
        mocked_lw = mocker.patch("arrangeit.base.BaseController.remove_listed_window")
        mocked_ws = mocker.patch("arrangeit.base.BaseController.switch_workspace")
        controller.generator.__next__.return_value = base.WindowModel(workspace=1)
        controller.next()
        mocked_lw.assert_called()
        mocked_ws.assert_not_called()

    def test_BaseController_next_calls_set_screenshot(self, mocker):
        controller = controller_mocked_for_next(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.set_screenshot")
        controller.next(True)
        mocked.assert_called_once()

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

    def test_BaseController_next_returns_False(self, mocker):
        controller = controller_mocked_for_next(mocker)
        returned = controller.next(True)
        assert not returned

    ## BaseController.update
    def test_BaseController_update_sets_state_to_LOCATE_for_None(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseController.update_positioning")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = None
        controller.update(100, 100)
        assert controller.state == Settings.LOCATE

    def test_BaseController_update_calls_update_positioning_for_LOCATE(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.update_positioning")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.LOCATE
        x, y = 400, 500
        controller.update(x, y)
        assert mocked.call_count == 1
        mocked.assert_called_with(x, y)

    def test_BaseController_update_calls_update_resizing_for_RESIZE(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.BaseController.update_resizing")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.RESIZE
        x, y = 500, 600
        controller.update(x, y)
        assert mocked.call_count == 1
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
    def test_BaseController_update_positioning_calls_set_changed(self, mocker):
        controller = controller_mocked_next(mocker)
        x, y = 440, 441
        controller.state = Settings.LOCATE
        controller.update_positioning(x, y)
        controller.model.set_changed.assert_called_with(
            x=x - Settings.WINDOW_SHIFT_PIXELS, y=y - Settings.WINDOW_SHIFT_PIXELS
        )

    def test_BaseController_update_positioning_calls_run_task_move_window_not_resizable(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        SAMPLE = 2002
        type(controller.model).resizable = mocker.PropertyMock(return_value=False)
        type(controller.model).wid = mocker.PropertyMock(return_value=SAMPLE)
        type(controller.model).changed = mocker.PropertyMock(return_value=(200, 200))
        controller = base.BaseController(mocker.MagicMock())
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
        controller = base.BaseController(mocker.MagicMock())
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
        controller = base.BaseController(mocker.MagicMock())
        controller.update_positioning(101, 202)
        controller.app.run_task.assert_not_called()

    def test_BaseController_update_positioning_calls_next_for_not_resizable(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        controller.model.resizable = False
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(mocker.MagicMock())
        controller.update_positioning(101, 202)
        mocked.assert_called_once()

    def test_BaseController_update_positioning_for_resizable_sets_state(self, mocker):
        controller = controller_mocked_next(mocker)
        controller.model.resizable = True
        mocker.patch("arrangeit.base.BaseController.place_on_right_bottom")
        mocked_next = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.LOCATE
        new_state = controller.resizing_state_counterpart
        controller.update_positioning(101, 202)
        assert controller.state == new_state
        mocked_next.assert_not_called()
        controller.app.run_task.assert_not_called()

    def test_BaseController_update_positioning_for_resizable_calls_place_on_right(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        controller.model.resizable = True
        mocked = mocker.patch("arrangeit.base.BaseController.place_on_right_bottom")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.LOCATE
        controller.update_positioning(101, 202)
        mocked.assert_called_once()

    ## BaseController.update_resizing
    def test_BaseController_update_resizing_calls_wh_from_ending_xy(self, mocker):
        controller = controller_mocked_next(mocker)
        controller = base.BaseController(mocker.MagicMock())
        x, y = 304, 406
        controller.model.wh_from_ending_xy.return_value = (100, 100)
        controller.update_resizing(x, y)
        controller.model.wh_from_ending_xy.assert_called_with(x, y)

    def test_BaseController_update_resizing_calls_set_changed(self, mocker):
        controller = controller_mocked_next(mocker)
        w, h = 400, 505
        controller.model.wh_from_ending_xy.return_value = (w, h)
        controller = base.BaseController(mocker.MagicMock())
        controller.update_resizing(101, 202)
        controller.model.wh_from_ending_xy.set_changed(w=w, h=h)

    def test_BaseController_update_resizing_calls_run_task_move_and_resize_window(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        SAMPLE = 5005
        controller.model.wid = SAMPLE
        controller.model.wh_from_ending_xy.return_value = (10, 10)
        controller.model.changed = (200, 200)
        controller = base.BaseController(mocker.MagicMock())
        controller.update_resizing(101, 202)
        controller.app.run_task.assert_called_with("move_and_resize", SAMPLE)

    def test_BaseController_update_resizing_calls_run_task_move_and_resize_for_ws(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        SAMPLE = 5005
        controller.model.wid = SAMPLE
        controller.model.wh_from_ending_xy.return_value = (10, 10)
        controller.model.changed = ()
        controller.model.is_ws_changed = True
        controller = base.BaseController(mocker.MagicMock())
        controller.update_resizing(101, 202)
        controller.app.run_task.assert_called_with("move_and_resize", SAMPLE)

    def test_BaseController_update_resizing_skips_run_task_move_and_resize_window(
        self, mocker
    ):
        controller = controller_mocked_next(mocker)
        controller.model.wid = 5412
        controller.model.wh_from_ending_xy.return_value = (10, 10)
        controller.model.changed = ()
        controller.model.is_ws_changed = False
        controller = base.BaseController(mocker.MagicMock())
        controller.update_resizing(101, 202)
        controller.app.run_task.assert_not_called()

    def test_BaseController_update_resizing_calls_next(self, mocker):
        controller = controller_mocked_next(mocker)
        controller.model.wh_from_ending_xy.return_value = (100, 100)
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        controller = base.BaseController(mocker.MagicMock())
        controller.update_resizing(100, 100)
        mocked.assert_called_once()

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
        mocker.patch("arrangeit.base.BaseController.next")
        view = mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        controller.listed_window_activated(90192)
        assert view.return_value.windows.clear_list.call_count == 1

    def test_BaseController_listed_window_activated_calls_windowslist_add_windows(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseController.next")
        view = mocker.patch("arrangeit.base.ViewApplication")
        windows_list = [0, 1, 2]
        controller = base.BaseController(mocker.MagicMock())
        controller.app.collector.collection.get_windows_list.return_value = windows_list
        controller.listed_window_activated(90108)
        view.return_value.windows.add_windows.assert_called_once()
        view.return_value.windows.add_windows.assert_called_with(windows_list[1:])

    def test_BaseController_listed_window_activated_calls_recapture_mouse_for_OTHER(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseController.next")
        mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.OTHER
        controller.listed_window_activated(90103)
        mocked.assert_called_once()

    @pytest.mark.parametrize("state", [Settings.LOCATE, Settings.RESIZE])
    def test_BaseController_listed_window_activated_not_calling_recapture_not_OTHER(
        self, mocker, state
    ):
        mocker.patch("arrangeit.base.BaseController.next")
        mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = state
        controller.listed_window_activated(90104)
        mocked.assert_not_called()

    def test_BaseController_listed_window_activated_initializes_generator(self, mocker):
        mocker.patch("arrangeit.base.BaseController.next")
        mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        controller.listed_window_activated(90147)
        controller.app.collector.collection.generator.assert_called()

    def test_BaseController_listed_window_activated_sets_generator_attr(self, mocker):
        mocker.patch("arrangeit.base.BaseController.next")
        mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        controller.listed_window_activated(90152)
        assert (
            controller.generator
            == controller.app.collector.collection.generator.return_value
        )

    def test_BaseController_listed_window_activated_calls_next(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseController.next")
        mocker.patch("arrangeit.base.ViewApplication")
        controller = base.BaseController(mocker.MagicMock())
        controller.listed_window_activated(90423)
        mocked.assert_called_once()
        mocked.assert_called_with(first_time=True)

    ## BaseController.workspace_activated
    def test_BaseController_workspace_activated_calls_task_move_to_workspace(
        self, mocker
    ):
        view = mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        controller = base.BaseController(mocker.MagicMock())
        SAMPLE = 1003
        controller.workspace_activated(SAMPLE)
        controller.app.run_task.assert_called_with(
            "move_to_workspace", view.return_value.master.winfo_id.return_value, SAMPLE
        )

    def test_BaseController_workspace_activated_calls_set_changed(self, mocker):
        mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.data.WindowModel.set_changed")
        controller = base.BaseController(mocker.MagicMock())
        SAMPLE = 1044
        controller.workspace_activated(SAMPLE)
        mocked.assert_called_with(ws=SAMPLE)

    def test_BaseController_workspace_activated_calls_recapture_mouse_for_OTHER(
        self, mocker
    ):
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = Settings.OTHER
        controller.workspace_activated(1074)
        mocked.assert_called_once()

    @pytest.mark.parametrize("state", [Settings.LOCATE, Settings.RESIZE])
    def test_BaseController_workspace_activated_not_calling_recapture_mouse_not_OTHER(
        self, mocker, state
    ):
        mocker.patch("arrangeit.base.ViewApplication")
        mocker.patch("arrangeit.data.WindowModel.set_changed")
        mocked = mocker.patch("arrangeit.base.BaseController.recapture_mouse")
        controller = base.BaseController(mocker.MagicMock())
        controller.state = state
        controller.workspace_activated(1074)
        mocked.assert_not_called()
