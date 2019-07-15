import pytest

from arrangeit import __appname__
from arrangeit.darwin.collector import (Collector,
                                        NSApplicationActivationPolicyRegular,
                                        kCGNullWindowID,
                                        kCGWindowListExcludeDesktopElements)
from arrangeit.darwin.utils import (NSApplicationSupportDirectory,
                                    NSUserDomainMask, user_data_path)


class TestDarwinCollector(object):
    """Testing class for :py:class:`arrangeit.darwin.collector.Collector` class."""

    ## DarwinCollector._get_application_icon
    def test_DarwinCollector__get_application_icon_calls__running_apps_ids(
        self, mocker
    ):
        mocker.patch("arrangeit.darwin.collector.Image")
        mocker.patch("arrangeit.darwin.collector.io.BytesIO")
        mocked = mocker.patch("arrangeit.darwin.collector.Collector._running_apps_ids")
        Collector()._get_application_icon(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_DarwinCollector__get_application_icon_calls_io_BytesIO(self, mocker):
        mocker.patch("arrangeit.darwin.collector.Image.open")
        mocked = mocker.patch("arrangeit.darwin.collector.io.BytesIO")
        APP = mocker.MagicMock()
        SAMPLE = 10
        mocked_win = mocker.MagicMock()
        mocked_win.valueForKey_.return_value = SAMPLE
        mocker.patch(
            "arrangeit.darwin.collector.Collector._running_apps_ids",
            return_value={SAMPLE: APP},
        )
        Collector()._get_application_icon(mocked_win)
        mocked.assert_called_once()
        mocked.assert_called_with(APP.icon.return_value.TIFFRepresentation.return_value)

    def test_DarwinCollector__get_application_icon_calls_Image_open(self, mocker):
        mocked_bytes = mocker.patch("arrangeit.darwin.collector.io.BytesIO")
        mocked = mocker.patch("arrangeit.darwin.collector.Image.open")
        APP = mocker.MagicMock()
        SAMPLE = 10
        mocked_win = mocker.MagicMock()
        mocked_win.valueForKey_.return_value = SAMPLE
        mocker.patch(
            "arrangeit.darwin.collector.Collector._running_apps_ids",
            return_value={SAMPLE: APP},
        )
        Collector()._get_application_icon(mocked_win)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_bytes.return_value)

    def test_DarwinCollector__get_application_icon_returns_Image(self, mocker):
        mocker.patch("arrangeit.darwin.collector.io.BytesIO")
        mocked = mocker.patch("arrangeit.darwin.collector.Image.open")
        APP = mocker.MagicMock()
        SAMPLE = 10
        mocked_win = mocker.MagicMock()
        mocked_win.valueForKey_.return_value = SAMPLE
        mocker.patch(
            "arrangeit.darwin.collector.Collector._running_apps_ids",
            return_value={SAMPLE: APP},
        )
        returned = Collector()._get_application_icon(mocked_win)
        assert returned == mocked.return_value

    ## DarwinCollector.get_application_name
    def test_DarwinCollector_get_application_name_calls_valueForKey_(self, mocker):
        mocked_win = mocker.MagicMock()
        Collector().get_application_name(mocked_win)
        mocked_win.valueForKey_.assert_called_once()
        mocked_win.valueForKey_.assert_called_with("kCGWindowOwnerName")

    ## DarwinCollector._get_window_geometry
    def test_DarwinCollector__get_window_geometry_calls_valueForKey_for_bounds(
        self, mocker
    ):
        mocked_win = mocker.MagicMock()
        Collector()._get_window_geometry(mocked_win)
        mocked_win.valueForKey_.assert_called_once()
        mocked_win.valueForKey_.assert_called_with("kCGWindowBounds")

    @pytest.mark.parametrize("element", ["X", "Y", "Width", "Height"])
    def test_DarwinCollector__get_window_geometry_calls_valueForKey_element(
        self, mocker, element
    ):
        mocked_win = mocker.MagicMock()
        Collector()._get_window_geometry(mocked_win)
        calls = [mocker.call(element)]
        mocked_win.valueForKey_.return_value.valueForKey_.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize("element", ["X", "Y", "Width", "Height"])
    def test_DarwinCollector__get_window_geometry_returns_tuple_of_ints(
        self, mocker, element
    ):
        mocked_win = mocker.MagicMock()
        mocked_win.valueForKey_.return_value.valueForKey_.return_value = 50
        returned = Collector()._get_window_geometry(mocked_win)
        assert len(returned) == 4
        assert all(isinstance(returned[i], int) for i in range(4))

    ## DarwinCollector._get_window_id
    def test_DarwinCollector__get_window_id_calls_valueForKey_(self, mocker):
        mocked_win = mocker.MagicMock()
        Collector()._get_window_id(mocked_win)
        mocked_win.valueForKey_.assert_called_once()
        mocked_win.valueForKey_.assert_called_with("kCGWindowNumber")

    ## DarwinCollector._get_window_title
    def test_DarwinCollector__get_window_title_calls_valueForKey_(self, mocker):
        mocked_win = mocker.MagicMock()
        Collector()._get_window_title(mocked_win)
        mocked_win.valueForKey_.assert_called_once()
        mocked_win.valueForKey_.assert_called_with("kCGWindowName")

    ## DarwinCollector._running_apps_ids
    def test_DarwinCollector__running_apps_ids_calls_sharedWorkspace(self, mocker):
        mocked = mocker.patch("arrangeit.darwin.collector.NSWorkspace")
        Collector()._running_apps_ids()
        mocked.sharedWorkspace.assert_called_once()
        mocked.sharedWorkspace.assert_called_with()

    def test_DarwinCollector__running_apps_ids_calls_runningApplications(self, mocker):
        mocked = mocker.patch("arrangeit.darwin.collector.NSWorkspace")
        Collector()._running_apps_ids()
        mocked.sharedWorkspace.return_value.runningApplications.assert_called_once()
        mocked.sharedWorkspace.return_value.runningApplications.assert_called_with()

    def test_DarwinCollector__running_apps_ids_functionality(self, mocker):
        APP1 = mocker.MagicMock()
        APP2 = mocker.MagicMock()
        APP3 = mocker.MagicMock()
        APP1.activationPolicy.return_value = NSApplicationActivationPolicyRegular
        APP1.processIdentifier.return_value = 1
        APP2.activationPolicy.return_value = mocker.PropertyMock(return_value=500)
        APP3.activationPolicy.return_value = NSApplicationActivationPolicyRegular
        APP3.processIdentifier.return_value = 3
        mocked = mocker.patch("arrangeit.darwin.collector.NSWorkspace")
        mocked.sharedWorkspace.return_value.runningApplications.return_value = [APP1, APP2, APP3]
        returned = Collector()._running_apps_ids()
        assert returned == {1: APP1, 3: APP3}

    ## DarwinCollector.add_window
    def test_DarwinCollector_add_window_calls_WindowsCollection_add(self, mocker):
        mocked = mocker.patch("arrangeit.data.WindowsCollection.add")
        mocker.patch("arrangeit.darwin.collector.Collector._get_window_id")
        mocker.patch("arrangeit.darwin.collector.Collector._get_window_geometry")
        mocker.patch("arrangeit.darwin.collector.Collector.is_resizable")
        mocker.patch("arrangeit.darwin.collector.Collector.is_restored")
        mocker.patch("arrangeit.darwin.collector.Collector._get_window_title")
        mocker.patch("arrangeit.darwin.collector.Collector.get_application_name")
        mocker.patch("arrangeit.darwin.collector.Collector._get_application_icon")
        mocker.patch(
            "arrangeit.darwin.collector.Collector.get_workspace_number_for_window"
        )
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    def test_DarwinCollector_add_window_inits_WindowModel(self, mocker):
        mocker.patch("arrangeit.data.WindowsCollection.add")
        mocked_id = mocker.patch("arrangeit.darwin.collector.Collector._get_window_id")
        mocked_rect = mocker.patch(
            "arrangeit.darwin.collector.Collector._get_window_geometry"
        )
        mocked_resizable = mocker.patch(
            "arrangeit.darwin.collector.Collector.is_resizable"
        )
        mocked_restored = mocker.patch(
            "arrangeit.darwin.collector.Collector.is_restored"
        )
        mocked_title = mocker.patch(
            "arrangeit.darwin.collector.Collector._get_window_title"
        )
        mocked_name = mocker.patch(
            "arrangeit.darwin.collector.Collector.get_application_name"
        )
        mocked_icon = mocker.patch(
            "arrangeit.darwin.collector.Collector._get_application_icon"
        )
        mocked_ws = mocker.patch(
            "arrangeit.darwin.collector.Collector.get_workspace_number_for_window"
        )
        mocked = mocker.patch("arrangeit.darwin.collector.WindowModel")
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with(
            wid=mocked_id.return_value,
            rect=mocked_rect.return_value,
            resizable=mocked_resizable.return_value,
            restored=mocked_restored.return_value,
            title=mocked_title.return_value,
            name=mocked_name.return_value,
            icon=mocked_icon.return_value,
            workspace=mocked_ws.return_value,
        )

    @pytest.mark.parametrize(
        "method",
        [
            "_get_window_id",
            "_get_window_geometry",
            "is_resizable",
            "is_restored",
            "_get_window_title",
            "get_application_name",
            "_get_application_icon",
            "get_workspace_number_for_window",
        ],
    )
    def test_DarwinCollector_add_window_calls_methods(self, mocker, method):
        mocker.patch("arrangeit.darwin.collector.Collector._get_window_id")
        mocker.patch("arrangeit.darwin.collector.Collector._get_window_geometry")
        mocker.patch("arrangeit.darwin.collector.Collector.is_resizable")
        mocker.patch("arrangeit.darwin.collector.Collector.is_restored")
        mocker.patch("arrangeit.darwin.collector.Collector._get_window_title")
        mocker.patch("arrangeit.darwin.collector.Collector.get_application_name")
        mocker.patch("arrangeit.darwin.collector.Collector._get_application_icon")
        mocker.patch(
            "arrangeit.darwin.collector.Collector.get_workspace_number_for_window"
        )
        mocked = mocker.patch("arrangeit.darwin.collector.Collector.{}".format(method))
        WIN = mocker.MagicMock()
        Collector().add_window(WIN)
        mocked.assert_called_once()
        mocked.assert_called_with(WIN)

    ## DarwinCollector.check_window
    @pytest.mark.parametrize("method", ["is_applicable", "is_valid_state"])
    def test_DarwinCollector_check_window_calls(self, mocker, method):
        mocker.patch(
            "arrangeit.darwin.collector.Collector.is_applicable", return_value=True
        )
        mocked = mocker.patch("arrangeit.darwin.collector.Collector.{}".format(method))
        Collector().check_window(mocker.MagicMock())
        mocked.assert_called_once()

    ## DarwinCollector.get_available_workspaces
    @pytest.mark.skip("Research how to deal with workspaces in Mac OS X")
    def test_DarwinCollector_get_available_workspaces_(self, mocker):
        pass

    ## DarwinCollector.get_monitors_rects
    def test_DarwinCollector_get_monitors_rects_calls_NSScreen_screens(self, mocker):
        mocked = mocker.patch("arrangeit.darwin.collector.NSScreen")
        Collector().get_monitors_rects()
        mocked.screens.assert_called_once()
        mocked.screens.assert_called_with()

    def test_DarwinCollector_get_monitors_rects_returns_list_of_rect_parts(
        self, mocker
    ):
        RECT1, RECT2 = (0.0, 0.0, 1920.0, 1280.0), (1920.0, 0.0, 1280.0, 1080.0)
        screen1 = mocker.MagicMock()
        screen1.frame.return_value.origin.x = RECT1[0]
        screen1.frame.return_value.origin.y = RECT1[1]
        screen1.frame.return_value.size.width = RECT1[2]
        screen1.frame.return_value.size.height = RECT1[3]
        screen2 = mocker.MagicMock()
        screen2.frame.return_value.origin.x = RECT2[0]
        screen2.frame.return_value.origin.y = RECT2[1]
        screen2.frame.return_value.size.width = RECT2[2]
        screen2.frame.return_value.size.height = RECT2[3]
        mocked = mocker.patch("arrangeit.darwin.collector.NSScreen")
        mocked.screens.return_value = [screen1, screen2]

        returned = Collector().get_monitors_rects()
        assert returned == [
            tuple([int(el) for el in RECT1]),
            tuple([int(el) for el in RECT2]),
        ]

    ## DarwinCollector.get_windows
    def test_DarwinCollector_get_windows_calls_CGWindowListCopyWindowInfo(self, mocker):
        mocked = mocker.patch("arrangeit.darwin.collector.CGWindowListCopyWindowInfo")
        Collector().get_windows()
        mocked.assert_called_once()
        mocked.assert_called_with(
            kCGWindowListExcludeDesktopElements, kCGNullWindowID
        )

    def test_DarwinCollector_get_windows_returns_list(self, mocker):
        SAMPLE = (mocker.MagicMock(), mocker.MagicMock())
        mocker.patch(
            "arrangeit.darwin.collector.CGWindowListCopyWindowInfo", return_value=SAMPLE
        )
        returned = Collector().get_windows()
        assert returned == [SAMPLE[0], SAMPLE[1]]

    ## DarwinCollector.get_workspace_number_for_window
    @pytest.mark.skip("Research how to deal with workspaces in Mac OS X")
    def test_DarwinCollector_get_workspace_number_for_window(self, mocker):
        pass

    ## DarwinCollector.is_applicable
    def test_DarwinCollector_is_applicable_calls__running_apps_ids(self, mocker):
        mocked = mocker.patch("arrangeit.darwin.collector.Collector._running_apps_ids")
        Collector().is_applicable(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_DarwinCollector_is_applicable_functionality_for_owner(self, mocker):
        VALUE = (10,)
        mocker.patch(
            "arrangeit.darwin.collector.Collector._running_apps_ids", return_value=VALUE
        )
        mocked_win = mocker.MagicMock()
        mocked_win.valueForKey_.side_effect = [10, "something"]
        assert Collector().is_applicable(mocked_win) is True

    def test_DarwinCollector_is_applicable_functionality_for_not_owner(self, mocker):
        VALUE = (10,)
        mocker.patch(
            "arrangeit.darwin.collector.Collector._running_apps_ids", return_value=VALUE
        )
        mocked_win = mocker.MagicMock()
        mocked_win.valueForKey_.side_effect = [30, "something"]
        assert Collector().is_applicable(mocked_win) is False

    def test_DarwinCollector_is_applicable_functionality_for_name_None(self, mocker):
        VALUE = (10,)
        mocker.patch(
            "arrangeit.darwin.collector.Collector._running_apps_ids", return_value=VALUE
        )
        mocked_win = mocker.MagicMock()
        mocked_win.valueForKey_.side_effect = [10, None]
        assert Collector().is_applicable(mocked_win) is False

    def test_DarwinCollector_is_applicable_functionality_for_empty_name(self, mocker):
        VALUE = (10,)
        mocker.patch(
            "arrangeit.darwin.collector.Collector._running_apps_ids", return_value=VALUE
        )
        mocked_win = mocker.MagicMock()
        mocked_win.valueForKey_.side_effect = [10, ""]
        assert Collector().is_applicable(mocked_win) is False

    def test_DarwinCollector_is_applicable_functionality_for_non_empty_name(
        self, mocker
    ):
        VALUE = (10,)
        mocker.patch(
            "arrangeit.darwin.collector.Collector._running_apps_ids", return_value=VALUE
        )
        mocked_win = mocker.MagicMock()
        mocked_win.valueForKey_.side_effect = [10, "something"]
        assert Collector().is_applicable(mocked_win) is True

    ## DarwinCollector.is_resizable
    @pytest.mark.skip("Research how to deal with resizable windows in Mac OS X")
    def test_DarwinCollector_is_resizable(self, mocker):
        pass

    ## DarwinCollector.is_restored
    @pytest.mark.skip("Research how to deal with minimized windows in Mac OS X")
    def test_DarwinCollector_is_restored(self, mocker):
        pass

    ## DarwinCollector.is_valid_state
    @pytest.mark.skip("Research what makes window with a valid state in Mac OS X")
    def test_DarwinCollector_is_valid_state(self, mocker):
        pass


## arrangeit.darwin.utils
class TestDarwinUtils(object):
    """Testing class for `arrangeit.darwin.utils` module."""

    ## DarwinUtils.user_data_path
    def test_darwin_utils_user_data_path_calls_NSSearchPathForDirectoriesInDomains(
        self, mocker
    ):
        mocked = mocker.patch(
            "arrangeit.darwin.utils.NSSearchPathForDirectoriesInDomains"
        )
        mocker.patch("arrangeit.darwin.utils.os.path.join")
        user_data_path()
        mocked.assert_called_once()
        mocked.assert_called_with(NSApplicationSupportDirectory, NSUserDomainMask, True)

    def test_darwin_utils_user_data_path_calls_os_path_join(self, mocker):
        SAMPLE = ("foo", 0)
        mocked_search = mocker.patch(
            "arrangeit.darwin.utils.NSSearchPathForDirectoriesInDomains",
            return_value=SAMPLE,
        )
        mocked = mocker.patch("arrangeit.darwin.utils.os.path.join")
        user_data_path()
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_search.return_value[0], __appname__)
