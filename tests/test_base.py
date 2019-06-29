import copy
from json import JSONDecodeError

import pytest

from arrangeit import base, utils
from arrangeit.data import WindowModel, WindowsCollection
from arrangeit.settings import Settings

from .fixtures import (
    SAMPLE_RECT,
    WIN_COLLECTION_SNAP_CHANGED,
    WIN_COLLECTION_SNAP_SAMPLES,
    WIN_COLLECTION_SNAP_SAMPLES_EXCLUDING,
)

from .mock_helpers import mocked_setup


class TestBaseApp(object):
    """Testing class for BaseApp class."""

    ## BaseApp
    @pytest.mark.parametrize("attr", ["controller", "collector"])
    def test_BaseApp_inits_attr_as_None(self, attr):
        assert getattr(base.BaseApp, attr) is None

    ## BaseApp.__init__.controller
    def test_BaseApp_initialization_calls_setup_controller(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        base.BaseApp()
        mocked.assert_called_once()

    def test_BaseApp_initialization_instantiates_controller(self, mocker):
        mocked_setup(mocker)
        mainapp = base.BaseApp()
        assert getattr(mainapp, "controller", None) is not None
        assert isinstance(getattr(mainapp, "controller"), base.BaseController)

    def test_BaseApp_initialization_instantiates_controller_with_app(self, mocker):
        mocked_setup(mocker)
        mocked = mocker.patch(
            "arrangeit.{}.controller.Controller".format(utils.platform_path())
        )
        mainapp = base.BaseApp()
        calls = [mocker.call(mainapp)]
        mocked.assert_has_calls(calls, any_order=True)

    ## BaseApp.__init__.collector
    def test_BaseApp_initialization_calls_setup_collector(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        base.BaseApp()
        mocked.assert_called_once()

    def test_BaseApp_initialization_instantiates_collector(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mainapp = base.BaseApp()
        assert getattr(mainapp, "collector", None) is not None
        assert isinstance(getattr(mainapp, "collector"), base.BaseCollector)

    ## BaseApp.setup_controller
    def test_BaseApp_setup_controller_calls_get_component_class_Controller(
        self, mocker
    ):
        mocked_setup(mocker)
        mocked = mocker.patch("arrangeit.base.get_component_class")
        base.BaseApp().setup_controller()
        mocked.assert_called()
        mocked.assert_called_with("Controller")

    ## BaseApp.setup_collector
    def test_BaseApp_setup_collector_calls_get_component_class_Collector(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.get_component_class")
        base.BaseApp().setup_collector()
        mocked.assert_called()
        mocked.assert_called_with("Collector")

    ## BaseApp.grab_window_screen
    def test_BaseApp_grab_window_screen_raises_NotImplementedError(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        with pytest.raises(NotImplementedError):
            base.BaseApp().grab_window_screen(None)

    ## BaseApp.run
    def test_BaseApp_run_calls_collector_run(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch(
            "arrangeit.{}.collector.Collector".format(utils.platform_path())
        )
        base.BaseApp().run()
        assert mocked.return_value.run.call_count == 1

    def test_BaseApp_run_calls_WindowsCollection_generator(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch(
            "arrangeit.{}.collector.Collector.add_window".format(utils.platform_path())
        )
        mocked = mocker.patch("arrangeit.base.WindowsCollection")
        base.BaseApp().run()
        assert mocked.return_value.generator.call_count == 1

    def test_BaseApp_run_calls_controller_run(self, mocker):
        mocked_setup(mocker)
        mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocked = mocker.patch(
            "arrangeit.{}.controller.Controller".format(utils.platform_path())
        )
        base.BaseApp().run()
        assert mocked.return_value.run.call_count == 1

    def test_BaseApp_run_calls_controller_run_with_valid_argument(self, mocker):
        mocked_setup(mocker)
        path = utils.platform_path()
        mocker.patch("arrangeit.{}.collector.Collector.add_window".format(path))
        mocked = mocker.patch("arrangeit.{}.controller.Controller".format(path))
        generator = mocker.patch("arrangeit.data.WindowsCollection.generator")
        base.BaseApp().run()
        mocked.return_value.run.assert_called_with(generator.return_value)

    ## BaseApp.run_task
    @pytest.mark.parametrize(
        "task, args",
        [
            ("activate_root", (100,)),
            ("change_setting", ("ROOT_ALPHA", 0.95)),
            ("move", (50,)),
            ("move_and_resize", (100,)),
            ("move_to_workspace", (50001, 1001)),
            ("rerun_from_window", (20001,)),
            ("save_default", ()),
        ],
    )
    def test_BaseApp_run_task_calls_related_methods(self, mocker, task, args):
        mocker.patch("arrangeit.base.BaseApp.change_setting")  # to not change the value
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.BaseApp.{}".format(task))
        base.BaseApp().run_task(task, *args)
        mocked.assert_called_with(*args)

    ## BaseApp.activate_root
    def test_BaseApp_activate_root_raises_NotImplementedError(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        with pytest.raises(NotImplementedError):
            base.BaseApp().activate_root()

    ## BaseApp.change_setting
    def test_BaseApp_change_setting_returns_change_settings_color_group_BG(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.BaseApp.change_settings_color_group")
        mocked_is_setting = mocker.patch("arrangeit.base.Settings.is_setting")
        returned = base.BaseApp().change_setting("_BG", "white")
        mocked.assert_called_once()
        mocked.assert_called_with("_BG", "white")
        assert returned == mocked.return_value
        mocked_is_setting.assert_not_called()

    def test_BaseApp_change_setting_returns_change_settings_color_group_FG(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.BaseApp.change_settings_color_group")
        mocked_is_setting = mocker.patch("arrangeit.base.Settings.is_setting")
        returned = base.BaseApp().change_setting("_FG", "black")
        mocked.assert_called_once()
        mocked.assert_called_with("_FG", "black")
        assert returned == mocked.return_value
        mocked_is_setting.assert_not_called()

    def test_BaseApp_change_setting_calls_is_setting(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.Settings.is_setting")
        returned = base.BaseApp().change_setting("ROOT_ALPHA", 0.95)
        mocked.assert_called_once()
        mocked.assert_called_with("ROOT_ALPHA", 0.95)
        assert returned is not True

    def test_BaseApp_change_setting_calls_is_setting_invalid(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.Settings.is_setting", return_value=False)
        returned = base.BaseApp().change_setting("ROOT_ALPHA1", 0.95)
        mocked.assert_called_once()
        mocked.assert_called_with("ROOT_ALPHA1", 0.95)
        assert returned is True

    def test_BaseApp_change_setting_changes_valid_setting(self, mocker):
        import time
        from random import seed, random

        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        alpha = int(Settings.ROOT_ALPHA * 10000)
        seed(int(time.time()))
        SAMPLE = random()
        base.BaseApp().change_setting("ROOT_ALPHA", SAMPLE)
        assert int(Settings.ROOT_ALPHA * 10000) != alpha
        assert int(Settings.ROOT_ALPHA * 10000) == int(SAMPLE * 10000)
        base.BaseApp().change_setting("ROOT_ALPHA", alpha / 10000)

    def test_BaseApp_change_setting_calls__save_setting(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.BaseApp._save_setting")
        base.BaseApp().change_setting("ROOT_ALPHA", 0.95)
        mocked.assert_called_once()
        mocked.assert_called_with(["ROOT_ALPHA"], 0.95)

    ## BaseApp.change_settings_color_group
    def test_BaseApp_change_settings_color_group_calls_Settings_color_group(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.BaseApp._save_setting")
        mocker.patch("arrangeit.base.setattr")
        mocked = mocker.patch("arrangeit.base.Settings.color_group")
        GROUP = "_BG"
        base.BaseApp().change_settings_color_group(GROUP, "white")
        mocked.assert_called_once()
        mocked.assert_called_with(GROUP)

    def test_BaseApp_change_settings_color_group_calls_Settings_setattr(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.BaseApp._save_setting")
        mocked = mocker.patch("arrangeit.base.setattr")
        GROUP, VALUE = "_BG", "white"
        base.BaseApp().change_settings_color_group(GROUP, VALUE)
        for name in Settings.color_group(GROUP):
            calls = [mocker.call(Settings, name, VALUE)]
            mocked.assert_has_calls(calls, any_order=True)

    def test_BaseApp_change_settings_color_group_calls__save_setting(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.BaseApp._save_setting")
        mocker.patch("arrangeit.base.setattr")
        GROUP, VALUE = "_BG", "white"
        base.BaseApp().change_settings_color_group(GROUP, VALUE)
        calls = [mocker.call(Settings.color_group(GROUP), VALUE)]
        mocked.assert_has_calls(calls, any_order=True)

    ## BaseApp.move
    def test_BaseApp_move_raises_NotImplementedError(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        with pytest.raises(NotImplementedError):
            base.BaseApp().move()

    ## BaseApp.move_and_resize
    def test_BaseApp_move_and_resize_raises_NotImplementedError(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        with pytest.raises(NotImplementedError):
            base.BaseApp().move_and_resize()

    ## BaseApp.move_to_workspace
    def test_BaseApp_move_to_workspace_raises_NotImplementedError(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        with pytest.raises(NotImplementedError):
            base.BaseApp().move_to_workspace()

    ## BaseApp.rerun_from_window
    def test_BaseApp_rerun_from_window_calls_repopulate_for_wid(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.data.WindowsCollection.repopulate_for_wid")
        app = base.BaseApp()
        app.rerun_from_window(45221, 75300)
        mocked.assert_called()
        mocked.assert_called_with(45221, 75300)

    ## BaseApp.save_default
    def test_BaseApp_save_default_calls_platform_user_data_path(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.os")
        mocked = mocker.patch("arrangeit.base.platform_user_data_path")
        base.BaseApp().save_default()
        mocked.assert_called_once()

    def test_BaseApp_save_default_checks_if_directory_exists(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.platform_user_data_path")
        mocker.patch("arrangeit.base.json")
        mocker.patch("arrangeit.base.os")
        mocked = mocker.patch("arrangeit.base.os.path.exists")
        base.BaseApp().save_default()
        mocked.assert_called_once()

    def test_BaseApp_save_default_creates_directory(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        path = mocker.patch("arrangeit.base.platform_user_data_path")
        mocker.patch("arrangeit.base.json")
        mocker.patch("arrangeit.base.os")
        mocker.patch("arrangeit.base.os.path.exists", return_value=False)
        mocked = mocker.patch("arrangeit.base.os.mkdir")
        base.BaseApp().save_default()
        mocked.assert_called_once()
        mocked.assert_called_once_with(path.return_value)

    def test_BaseApp_save_default_calls_collection_export(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.os")
        mocker.patch("arrangeit.base.platform_user_data_path")
        mocker.patch("arrangeit.base.json")
        mocked = mocker.patch("arrangeit.data.WindowsCollection.export")
        base.BaseApp().save_default()
        mocked.assert_called_once()

    def test_BaseApp_save_default_calls_json_dump(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.os")
        mocker.patch("arrangeit.base.platform_user_data_path")
        mocked = mocker.patch("arrangeit.base.json.dump")
        mocker.patch("arrangeit.data.WindowsCollection.export")
        base.BaseApp().save_default()
        mocked.assert_called_once()

    ## BaseApp._save_setting
    def test_BaseApp__save_setting_calls_platform_user_data_path(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.os")
        mocker.patch("arrangeit.base.open")
        mocker.patch("arrangeit.base.json")
        mocked = mocker.patch("arrangeit.base.platform_user_data_path")
        base.BaseApp()._save_setting(["ROOT_ALPHA"], 0.9)
        mocked.assert_called_once()

    def test_BaseApp__save_setting_checks_if_directory_exists(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.platform_user_data_path")
        mocker.patch("arrangeit.base.json")
        mocker.patch("arrangeit.base.os")
        mocker.patch("arrangeit.base.open")
        SAMPLE = "foo"
        mocker.patch("arrangeit.base.platform_user_data_path", return_value=SAMPLE)
        mocked = mocker.patch("arrangeit.base.os.path.exists")
        base.BaseApp()._save_setting(["ROOT_ALPHA"], 0.9)
        calls = [mocker.call(SAMPLE)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_BaseApp__save_setting_creates_directory(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        path = mocker.patch("arrangeit.base.platform_user_data_path")
        mocker.patch("arrangeit.base.json")
        mocker.patch("arrangeit.base.os")
        mocker.patch("arrangeit.base.os.path.exists", return_value=False)
        mocked = mocker.patch("arrangeit.base.os.mkdir")
        base.BaseApp()._save_setting(["ROOT_ALPHA"], 0.9)
        mocked.assert_called_once()
        mocked.assert_called_once_with(path.return_value)

    def test_BaseApp__save_setting_checks_if_file_exists(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.platform_user_data_path")
        mocker.patch("arrangeit.base.json")
        mocker.patch("arrangeit.base.open")
        SAMPLE = "foobar"
        mocker.patch("arrangeit.base.os.path.join", return_value=SAMPLE)
        mocked = mocker.patch("arrangeit.base.os.path.exists")
        base.BaseApp()._save_setting(["ROOT_ALPHA"], 0.9)
        calls = [mocker.call(SAMPLE)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_BaseApp__save_setting_calls_json_load_once(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.os.path.join", return_value="foo")
        mocker.patch("arrangeit.base.os.path.exists", return_value=True)
        mocker.patch("arrangeit.base.open")
        mocker.patch("arrangeit.base.json.load")
        mocked = mocker.patch("arrangeit.base.json.dump")
        base.BaseApp()._save_setting(["MAIN_BG", "ICON_LABEL_BG"], "white")
        mocked.assert_called_once()

    def test_BaseApp__save_setting_catches_exception_and_continues(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        SAMPLE = "barfoo"
        mocker.patch("arrangeit.base.os.path.join", return_value=SAMPLE)
        mocker.patch("arrangeit.base.os.path.exists", return_value=True)
        mocker.patch("arrangeit.base.open")
        mocker.patch("arrangeit.base.json.load", side_effect=JSONDecodeError("", "", 0))
        returned = base.BaseApp()._save_setting(["ROOT_ALPHA"], 0.97)
        assert returned is False

    def test_BaseApp__save_setting_writes_to_settings_file(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        SAMPLE = "barfoo"
        mocker.patch("arrangeit.base.json.load", return_value={})
        mocker.patch("arrangeit.base.os.path.join", return_value=SAMPLE)
        mocker.patch("arrangeit.base.os.path.exists", return_value=True)
        mocked_open = mocker.patch("arrangeit.base.open")
        mocked = mocker.patch("arrangeit.base.json.dump")
        VALUES = {"ROOT_ALPHA": 0.97}
        base.BaseApp()._save_setting(["ROOT_ALPHA"], 0.97)
        calls_open = [mocker.call(SAMPLE, "w")]
        mocked_open.assert_has_calls(calls_open, any_order=True)
        calls = [mocker.call(VALUES, mocked_open.return_value.__enter__.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_BaseApp__save_setting_updates_settings_file(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        SAMPLE = "barfoo"
        VALUES = {"MAIN_FG": "white", "MAIN_BG": "black"}
        mocker.patch("arrangeit.base.json.load", return_value=copy.deepcopy(VALUES))
        mocker.patch("arrangeit.base.os.path.join", return_value=SAMPLE)
        mocker.patch("arrangeit.base.os.path.exists", return_value=True)
        mocked_open = mocker.patch("arrangeit.base.open")
        mocked = mocker.patch("arrangeit.base.json.dump")
        base.BaseApp()._save_setting(["ROOT_ALPHA"], 0.97)
        VALUES.update(ROOT_ALPHA=0.97)
        calls = [mocker.call(VALUES, mocked_open.return_value.__enter__.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_BaseApp__save_setting_overwrites_settings_file_values(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        SAMPLE = "barfoo"
        VALUES = {"MAIN_FG": "white", "MAIN_BG": "black"}
        mocker.patch("arrangeit.base.json.load", return_value=copy.deepcopy(VALUES))
        mocker.patch("arrangeit.base.os.path.join", return_value=SAMPLE)
        mocker.patch("arrangeit.base.os.path.exists", return_value=True)
        mocked_open = mocker.patch("arrangeit.base.open")
        mocked = mocker.patch("arrangeit.base.json.dump")
        base.BaseApp()._save_setting(["MAIN_FG", "MAIN_BG"], "red")
        VALUES = {"MAIN_FG": "red", "MAIN_BG": "red"}
        calls = [mocker.call(VALUES, mocked_open.return_value.__enter__.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    ## BaseApp._initialize_snapping_sources
    def test_BaseApp__initialize_snapping_sources_calls_collector_get_monitors_rects(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch(
            "arrangeit.{}.collector.Collector.get_monitors_rects".format(
                utils.platform_path()
            )
        )
        base.BaseApp()._initialize_snapping_sources()
        assert mocked.call_count == 1

    def test_BaseApp__initialize_snapping_sources_calls_get_snapping_sources_for_rect(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch(
            "arrangeit.{}.collector.Collector.get_monitors_rects".format(
                utils.platform_path()
            ),
            return_value=[(0, 0, 640, 480), (500, 0, 800, 600)],
        )
        mocked = mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        base.BaseApp()._initialize_snapping_sources()
        assert mocked.call_count == 2

    def test_BaseApp__initialize_snapping_sources_calls_get_available_workspaces(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch(
            "arrangeit.{}.collector.Collector.get_monitors_rects".format(
                utils.platform_path()
            ),
            return_value=[(0, 0, 640, 480), (500, 0, 800, 600)],
        )
        mocked = mocker.patch(
            "arrangeit.{}.collector.Collector.get_available_workspaces".format(
                utils.platform_path()
            ),
            return_value=[(0, ""), (1, ""), (2, "")],
        )
        mocked = mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        base.BaseApp()._initialize_snapping_sources()
        assert mocked.call_count == 2

    def test_BaseApp__initialize_snapping_sources_functionality(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch(
            "arrangeit.{}.collector.Collector.get_available_workspaces".format(
                utils.platform_path()
            ),
            return_value=[(0, ""), (1, ""), (2, "")],
        )
        mocker.patch(
            "arrangeit.{}.collector.Collector.get_monitors_rects".format(
                utils.platform_path()
            ),
            return_value=[(0, 0, 640, 480), (500, 0, 800, 600)],
        )
        mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        sources = base.BaseApp()._initialize_snapping_sources()
        assert len(sources) == 3
        assert sources.get(0) is not None
        assert sources.get(1) is not None
        assert sources.get(2) is not None

    ## BaseApp.create_snapping_sources
    def test_BaseApp_create_snapping_sources_calls__initialize_snapping_sources(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.BaseApp._initialize_snapping_sources")
        base.BaseApp().create_snapping_sources(WindowModel())
        mocked.assert_called_once()

    def test_BaseApp_create_snapping_sources_calls_collection_generator(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.WindowsCollection.generator")
        base.BaseApp().create_snapping_sources(WindowModel())
        mocked.assert_called_once()

    def test_BaseApp_create_snapping_sources_calls_utils_get_snapping_sources_for_rect(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.get_snapping_sources_for_rect")
        collection = WindowsCollection()
        collection.add(WindowModel(rect=SAMPLE_RECT, workspace=0))
        mocker.patch("arrangeit.base.WindowsCollection", return_value=collection)
        base.BaseApp().create_snapping_sources(WindowModel())
        mocked.assert_called()

    def test_BaseApp_create_snapping_sources_returns_dict(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch(
            "arrangeit.base.BaseApp._initialize_snapping_sources",
            return_value={1001: [], 1002: []},
        )
        rects = base.BaseApp().create_snapping_sources(WindowModel())
        assert isinstance(rects, dict)
        assert rects == {1001: [], 1002: []}

    @pytest.mark.parametrize("windows,expected", WIN_COLLECTION_SNAP_CHANGED)
    def test_BaseApp_create_snapping_sources_uses_changed_values_if_available(
        self, mocker, windows, expected
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        collection = WindowsCollection()
        for window in windows:
            model = WindowModel(rect=window[1], workspace=1005)
            model.set_changed(rect=window[2], ws=window[0])
            collection.add(model)
        mocker.patch("arrangeit.base.WindowsCollection", return_value=collection)
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch(
            "arrangeit.base.BaseApp._initialize_snapping_sources",
            return_value={1001: [], 1002: []},
        )
        mocked = mocker.patch("arrangeit.base.Settings")
        type(mocked).SNAP_PIXELS = mocker.PropertyMock(return_value=10)
        rects = base.BaseApp().create_snapping_sources(model)
        for ws, snaps in rects.items():
            assert snaps == expected[ws]

    @pytest.mark.parametrize("windows,expected", WIN_COLLECTION_SNAP_SAMPLES)
    def test_BaseApp_create_snapping_sources_functionality(
        self, mocker, windows, expected
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        collection = WindowsCollection()
        for window in windows:
            model = WindowModel(rect=SAMPLE_RECT, workspace=1005)
            model.set_changed(ws=window[0], rect=window[1:])
            collection.add(model)
        mocker.patch("arrangeit.base.WindowsCollection", return_value=collection)
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch(
            "arrangeit.base.BaseApp._initialize_snapping_sources",
            return_value={1001: [], 1002: []},
        )
        mocked = mocker.patch("arrangeit.base.Settings")
        type(mocked).SNAP_PIXELS = mocker.PropertyMock(return_value=10)
        rects = base.BaseApp().create_snapping_sources(WindowModel())
        for ws, snaps in rects.items():
            assert snaps == expected[ws]

    @pytest.mark.parametrize("windows,expected", WIN_COLLECTION_SNAP_SAMPLES_EXCLUDING)
    def test_BaseApp_create_snapping_sources_excludes_provided_model(
        self, mocker, windows, expected
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch(
            "arrangeit.{}.collector.Collector.get_monitors_rects".format(
                utils.platform_path()
            ),
            return_value=[],
        )
        collection = WindowsCollection()
        model0 = WindowModel(rect=SAMPLE_RECT, workspace=1005, wid=5000)
        model0.set_changed(ws=windows[0][0], rect=windows[0][1:])
        collection.add(model0)
        model1 = WindowModel(rect=SAMPLE_RECT, workspace=1005, wid=9000)
        model1.set_changed(ws=windows[1][0], rect=windows[1][1:])
        collection.add(model1)
        mocker.patch("arrangeit.base.WindowsCollection", return_value=collection)
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch(
            "arrangeit.base.BaseApp._initialize_snapping_sources",
            return_value={1001: [], 1002: []},
        )
        mocked = mocker.patch("arrangeit.base.Settings")
        type(mocked).SNAP_PIXELS = mocker.PropertyMock(return_value=10)
        type(mocked).SNAP_INCLUDE_SELF = mocker.PropertyMock(return_value=False)
        sources = base.BaseApp().create_snapping_sources(model1)
        assert sources[1001] == expected[1001][:1]

    @pytest.mark.parametrize("windows,expected", WIN_COLLECTION_SNAP_SAMPLES_EXCLUDING)
    def test_BaseApp_create_snapping_sources_includes_provided_model(
        self, mocker, windows, expected
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch(
            "arrangeit.{}.collector.Collector.get_monitors_rects".format(
                utils.platform_path()
            ),
            return_value=[],
        )
        collection = WindowsCollection()
        model0 = WindowModel(rect=SAMPLE_RECT, workspace=1005, wid=5000)
        model0.set_changed(ws=windows[0][0], rect=windows[0][1:])
        collection.add(model0)
        model1 = WindowModel(rect=SAMPLE_RECT, workspace=1005, wid=9000)
        model1.set_changed(ws=windows[1][0], rect=windows[1][1:])
        collection.add(model1)
        mocker.patch(
            "arrangeit.base.BaseApp._initialize_snapping_sources",
            return_value={1001: [], 1002: []},
        )
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.WindowsCollection", return_value=collection)
        mocked = mocker.patch("arrangeit.base.Settings")
        type(mocked).SNAP_PIXELS = mocker.PropertyMock(return_value=10)
        type(mocked).SNAP_INCLUDE_SELF = mocker.PropertyMock(return_value=True)
        sources = base.BaseApp().create_snapping_sources(model1)
        assert sources[1001] == expected[1001]


class TestBaseCollector(object):
    """Testing class for base Collector class."""

    ## BaseCollector
    def test_BaseCollector_inits_collection_as_None(self):
        assert base.BaseCollector.collection is None

    ## BaseCollector.__init__
    def test_BaseCollector_initialization_instantiates_WindowsCollection(self, mocker):
        collector = base.BaseCollector()
        assert getattr(collector, "collection", None) is not None
        assert isinstance(getattr(collector, "collection"), WindowsCollection)

    ## BaseCollector.is_applicable
    def test_BaseCollector_is_applicable_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().is_applicable(0)

    ## BaseCollector.is_valid_state
    def test_BaseCollector_is_valid_state_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().is_valid_state(0, 0)

    ## BaseCollector.is_resizable
    def test_BaseCollector_is_resizable_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().is_resizable(0)

    ## BaseCollector.get_windows
    def test_BaseCollector_get_windows_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().get_windows()

    ## BaseCollector.check_window
    def test_BaseCollector_check_window_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().check_window(None)

    ## BaseCollector.add_window
    def test_BaseCollector_add_window_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().add_window(None)

    ## BaseCollector.get_workspace_number
    def test_BaseCollector_get_workspace_number_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().get_workspace_number(None)

    ## BaseCollector.get_workspace_number_for_window
    def test_BaseCollector_get_workspace_number_for_window_raises_NotImplementedError(
        self
    ):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().get_workspace_number_for_window(None)

    ## BaseCollector.get_available_workspaces
    def test_BaseCollector_get_available_workspaces_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().get_available_workspaces()

    ## BaseCollector.get_monitors_rects
    def test_BaseCollector_get_monitors_rects_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().get_monitors_rects()

    ## BaseCollector.get_smallest_monitor_size
    def test_BaseCollector_get_smallest_monitor_size_calls_get_monitors_rects(
        self, mocker
    ):
        mocked = mocker.patch(
            "arrangeit.base.BaseCollector.get_monitors_rects",
            return_value=[(0, 0, 1920, 1280)],
        )
        base.BaseCollector().get_smallest_monitor_size()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_BaseCollector_get_smallest_monitor_size_returns_two_tuple(self, mocker):
        RECT1, RECT2 = (0, 0, 1920, 1280), (1920, 0, 1280, 1080)
        SAMPLE = [RECT1, RECT2]
        mocker.patch(
            "arrangeit.base.BaseCollector.get_monitors_rects", return_value=SAMPLE
        )
        returned = base.BaseCollector().get_smallest_monitor_size()
        assert returned == (RECT2[2], RECT2[3])

    ## BaseCollector.run
    def test_BaseCollector_run_calls_get_windows(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseCollector.get_windows")
        mocker.patch("arrangeit.data.WindowsCollection.sort")
        base.BaseCollector().run()
        mocked.assert_called_once()

    def test_BaseCollector_run_calls_check_window(self, mocker):
        mocker.patch("arrangeit.base.BaseCollector.get_windows", return_value=(0,))
        mocked = mocker.patch("arrangeit.base.BaseCollector.check_window")
        mocker.patch("arrangeit.base.BaseCollector.add_window")
        mocker.patch("arrangeit.data.WindowsCollection.sort")
        base.BaseCollector().run()
        mocked.assert_called_once()

    @pytest.mark.parametrize("elements", [(), (5, 10, 15), (4,)])
    def test_BaseCollector_run_calls_add_window(self, mocker, elements):
        mocker.patch("arrangeit.base.BaseCollector.get_windows", return_value=elements)
        mocker.patch("arrangeit.base.BaseCollector.check_window")
        mocker.patch("arrangeit.data.WindowsCollection.sort")
        mocked = mocker.patch("arrangeit.base.BaseCollector.add_window")
        base.BaseCollector().run()
        if len(elements) > 0:
            mocked.assert_called()
        assert mocked.call_count == len(elements)

    def test_BaseCollector_run_calls_collection_sort(self, mocker):
        mocker.patch("arrangeit.base.BaseCollector.get_windows", return_value=(0,))
        mocked = mocker.patch("arrangeit.base.BaseCollector.check_window")
        mocker.patch("arrangeit.base.BaseCollector.add_window")
        mocked = mocker.patch("arrangeit.data.WindowsCollection.sort")
        base.BaseCollector().run()
        mocked.assert_called_once()


class TestBaseMouse(object):
    """Testing class for Mouse class methods."""

    ## BaseMouse
    @pytest.mark.parametrize("attr", ["queue", "listener", "control"])
    def test_BaseMouse_inits_attr_as_None(self, attr):
        assert getattr(base.BaseMouse, attr) is None

    ## BaseMouse.__init__
    def test_BaseMouse_init_instantiates_Queue(self, mocker):
        mocked = mocker.patch("arrangeit.base.queue.Queue")
        base.BaseMouse()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_BaseMouse_init_sets_queue_attribute(self, mocker):
        mocked = mocker.patch("arrangeit.base.queue.Queue")
        assert base.BaseMouse().queue == mocked.return_value

    def test_BaseMouse_init_instantiates_Controller(self, mocker):
        mocked = mocker.patch("pynput.mouse.Controller")
        base.BaseMouse()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_BaseMouse_init_sets_control_attribute(self, mocker):
        mocked = mocker.patch("pynput.mouse.Controller")
        assert base.BaseMouse().control == mocked.return_value

    ## BaseMouse.cursor_position
    def test_BaseMouse_cursor_position_calls_Controller_position(self, mocker):
        mocked = mocker.patch("pynput.mouse.Controller")
        SAMPLE = (10, 20)
        type(mocked.return_value).position = mocker.PropertyMock(return_value=SAMPLE)
        returned = base.BaseMouse().cursor_position()
        assert returned == SAMPLE

    def test_BaseMouse_cursor_position_returns_position(self, mocker):
        mocked = mocker.patch("pynput.mouse.Controller")
        returned = base.BaseMouse().cursor_position()
        assert returned == mocked.return_value.position

    ## BaseMouse.get_item
    def test_BaseMouse_get_item_calls_queue_get(self, mocker):
        mocked = mocker.patch("arrangeit.base.queue.Queue.get")
        base.BaseMouse().get_item()
        mocked.assert_called_once()
        mocked.assert_called_with(block=False)

    def test_BaseMouse_get_item_returns_item(self, mocker):
        mocked = mocker.patch("arrangeit.base.queue.Queue.get")
        returned = base.BaseMouse().get_item()
        assert returned == mocked.return_value

    def test_BaseMouse_get_item_returns_None_for_Empty(self, mocker):
        assert base.BaseMouse().get_item() is None

    ## BaseMouse.move_cursor
    def test_BaseMouse_move_cursor_calls_Controller_position(self, mocker):
        mocked = mocker.patch("pynput.mouse.Controller")
        SAMPLE = (11, 22)
        type(mocked.return_value).position = mocker.PropertyMock(return_value=SAMPLE)
        base.BaseMouse().move_cursor(*SAMPLE)
        mocked.return_value.position == SAMPLE

    def test_BaseMouse_move_cursor_calls_position_with_provided_x_and_y(self, mocker):
        mocked = mocker.patch("pynput.mouse.Controller")
        xy = (101, 202)
        base.BaseMouse().move_cursor(*xy)
        assert mocked.return_value.position == xy

    ## BaseMouse.on_move
    def test_BaseMouse_on_move_puts_in_queue(self, mocker):
        mocked = mocker.patch("arrangeit.base.queue.Queue.put")
        mouse = base.BaseMouse()
        SAMPLE = (10.0, 20.0)
        mouse.on_move(*SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with((int(SAMPLE[0]), int(SAMPLE[1])))

    ## BaseMouse.on_scroll
    @pytest.mark.parametrize("dy,expected", [(-1, False), (1, True)])
    def test_BaseMouse_on_scroll_puts_in_queue(self, mocker, dy, expected):
        mocked = mocker.patch("arrangeit.base.queue.Queue.put")
        mouse = base.BaseMouse()
        mouse.on_scroll(0, 0, 0, dy)
        mocked.assert_called_once()
        mocked.assert_called_with(expected)

    ## BaseMouse.start
    def test_BaseMouse_start_instantiates_Listener(self, mocker):
        mocked = mocker.patch("pynput.mouse.Listener")
        mouse = base.BaseMouse()
        mouse.start()
        mocked.assert_called_once()
        mocked.assert_called_with(on_move=mouse.on_move, on_scroll=mouse.on_scroll)

    def test_BaseMouse_start_sets_listener_attribute(self, mocker):
        mocked = mocker.patch("pynput.mouse.Listener")
        mouse = base.BaseMouse()
        mouse.start()
        assert mouse.listener == mocked.return_value

    def test_BaseMouse_start_starts_listener(self, mocker):
        mocked = mocker.patch("pynput.mouse.Listener")
        mouse = base.BaseMouse()
        mouse.start()
        mocked.return_value.start.assert_called_once()
        mocked.return_value.start.assert_called_with()

    ## BaseMouse.stop
    @pytest.mark.skip("Find a way to test if raise keyword is invoked")
    def test_BaseMouse_stop_stops_listener(self, mocker):
        mouse = base.BaseMouse()
        mouse.stop()