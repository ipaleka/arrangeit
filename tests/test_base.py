import pytest

from arrangeit import base, data, utils

from .test_basecontroller import mock_main_loop, mocked_viewapp


class TestBaseApp(object):
    """Testing class for BaseApp class."""

    ## BaseApp
    @pytest.mark.parametrize("attr", ["controller", "collector"])
    def test_BaseApp_inits_attr_as_None(self, attr):
        assert getattr(base.BaseApp, attr) is None

    ## BaseApp.__init__.controller
    def test_BaseApp_initialization_calls_setup_controller(self, mocker):
        mocked_viewapp(mocker)
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        base.BaseApp()
        mocked.assert_called_once()

    def test_BaseApp_initialization_instantiates_controller(self, mocker):
        mocked_viewapp(mocker)
        mainapp = base.BaseApp()
        assert getattr(mainapp, "controller", None) is not None
        assert isinstance(getattr(mainapp, "controller"), base.BaseController)

    def test_BaseApp_initialization_instantiates_controller_with_app(self, mocker):
        mocked_viewapp(mocker)
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
        mocked_viewapp(mocker)
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
        mocked = mocker.patch("arrangeit.base.WindowsCollection")
        base.BaseApp().run()
        assert mocked.return_value.generator.call_count == 1

    def test_BaseApp_run_calls_controller_run(self, mocker):
        mocked_viewapp(mocker)
        mocked = mocker.patch(
            "arrangeit.{}.controller.Controller".format(utils.platform_path())
        )
        base.BaseApp().run()
        assert mocked.return_value.run.call_count == 1

    def test_BaseApp_run_calls_controller_run_with_valid_argument(self, mocker):
        mocked_viewapp(mocker)
        mocked = mocker.patch(
            "arrangeit.{}.controller.Controller".format(utils.platform_path())
        )
        generator = mocker.patch("arrangeit.data.WindowsCollection.generator")
        base.BaseApp().run()
        mocked.return_value.run.assert_called_with(generator.return_value)

    ## BaseApp.run_task
    @pytest.mark.parametrize(
        "task, args",
        [
            ("move", (50,)),
            ("move_and_resize", (100,)),
            ("move_to_workspace", (50001, 1001)),
            ("rerun_from_window", (20001,)),
            ("save_default", ()),
        ],
    )
    def test_BaseApp_run_task_calls_related_methods(self, mocker, task, args):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.get_tkinter_root")
        mocked = mocker.patch("arrangeit.base.BaseApp.{}".format(task))
        base.BaseApp().run_task(task, *args)
        mocked.assert_called_with(*args)

    ## BaseApp.grab_window_screen
    def test_BaseApp_grab_window_screen_raises_NotImplementedError(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        with pytest.raises(NotImplementedError):
            base.BaseApp().grab_window_screen(None)

    ## BaseApp.move_and_resize
    def test_BaseApp_move_and_resize_raises_NotImplementedError(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        with pytest.raises(NotImplementedError):
            base.BaseApp().move_and_resize()

    ## BaseApp.move
    def test_BaseApp_move_raises_NotImplementedError(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        with pytest.raises(NotImplementedError):
            base.BaseApp().move()

    ## BaseApp.move_to_workspace
    def test_BaseApp_move_to_workspace_raises_NotImplementedError(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        with pytest.raises(NotImplementedError):
            base.BaseApp().move_to_workspace()

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


class TestBaseCollector(object):
    """Testing class for base Collector class."""

    ## BaseCollector
    def test_BaseCollector_inits_collection_as_None(self):
        assert base.BaseCollector.collection is None

    ## BaseCollector.__init__
    def test_BaseCollector_initialization_instantiates_WindowsCollection(self, mocker):
        collector = base.BaseCollector()
        assert getattr(collector, "collection", None) is not None
        assert isinstance(getattr(collector, "collection"), data.WindowsCollection)

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
