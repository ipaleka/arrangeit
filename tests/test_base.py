import pytest

from arrangeit import base, data, utils

from test_basecontroller import mock_main_loop


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
        mainapp = base.BaseApp()
        assert getattr(mainapp, "controller", None) is not None
        assert isinstance(getattr(mainapp, "controller"), base.BaseController)

    def test_BaseApp_initialization_instantiates_controller_with_app(self, mocker):
        mocked = mocker.patch(
            "arrangeit.{}.controller.Controller".format(utils.platform_path())
        )
        mainapp = base.BaseApp()
        calls = [mocker.call(mainapp),]
        mocked.assert_has_calls(calls, any_order=True)

    ## BaseApp.__init__.collector
    def test_BaseApp_initialization_calls_setup_collector(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        base.BaseApp()
        mocked.assert_called_once()

    def test_BaseApp_initialization_instantiates_collector(self, mocker):
        mainapp = base.BaseApp()
        assert getattr(mainapp, "collector", None) is not None
        assert isinstance(getattr(mainapp, "collector"), base.BaseCollector)

    ## BaseApp.setup_controller
    def test_BaseApp_setup_controller_calls_get_component_class_Controller(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.base.get_component_class")
        base.BaseApp().setup_controller()
        mocked.assert_called()
        mocked.assert_called_with("Controller")

    ## BaseApp.setup_collector
    def test_BaseApp_setup_collector_calls_get_component_class_Collector(self, mocker):
        mocked = mocker.patch("arrangeit.base.get_component_class")
        base.BaseApp().setup_collector()
        mocked.assert_called()
        mocked.assert_called_with("Collector")

    ## BaseApp.run
    def test_BaseApp_run_calls_collector_run(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch(
            "arrangeit.{}.collector.Collector".format(utils.platform_path())
        )
        base.BaseApp().run()
        assert mocked.return_value.run.call_count == 1

    def test_BaseApp_run_calls_WindowsCollection_generator(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.WindowsCollection")
        base.BaseApp().run()
        assert mocked.return_value.generator.call_count == 1

    def test_BaseApp_run_calls_controller_run(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch(
            "arrangeit.{}.controller.Controller".format(utils.platform_path())
        )
        base.BaseApp().run()
        assert mocked.return_value.run.call_count == 1

    def test_BaseApp_run_calls_controller_run_with_valid_argument(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch(
            "arrangeit.{}.controller.Controller".format(utils.platform_path())
        )
        generator = mocker.patch("arrangeit.data.WindowsCollection.generator")
        base.BaseApp().run()
        mocked.return_value.run.assert_called_with(generator.return_value)


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

    ## BaseCollector.run
    def test_BaseCollector_run_calls_get_windows(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseCollector.get_windows")
        base.BaseCollector().run()
        mocked.assert_called_once()

    def test_BaseCollector_run_calls_check_window(self, mocker):
        mocker.patch("arrangeit.base.BaseCollector.get_windows", return_value=(0,))
        mocked = mocker.patch("arrangeit.base.BaseCollector.check_window")
        mocker.patch("arrangeit.base.BaseCollector.add_window")
        base.BaseCollector().run()
        mocked.assert_called_once()

    @pytest.mark.parametrize("elements", [(), (5, 10, 15), (4,)])
    def test_BaseCollector__call___calls_add_window(self, mocker, elements):
        mocker.patch("arrangeit.base.BaseCollector.get_windows", return_value=elements)
        mocker.patch("arrangeit.base.BaseCollector.check_window")
        mocked = mocker.patch("arrangeit.base.BaseCollector.add_window")
        base.BaseCollector().run()
        if len(elements) > 0:
            mocked.assert_called()
        assert mocked.call_count == len(elements)
