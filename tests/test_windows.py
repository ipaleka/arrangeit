import ctypes

from win32con import (
    STATE_SYSTEM_INVISIBLE,
    WS_EX_TOOLWINDOW,
    WS_EX_NOACTIVATE,
    WS_THICKFRAME,
)

import pytest

from arrangeit.windows.collector import TITLEBARINFO, WINDOWINFO, Collector

SAMPLE_HWND = 1001


class TestTITLEBARINFO(object):
    """Testing class for :py:class:`arrangeit.windows.collector.TITLEBARINFO` class."""

    def test_TITLEBARINFO_inits__fields_(self):
        assert getattr(TITLEBARINFO, "_fields_", None) is not None
        assert isinstance(TITLEBARINFO._fields_, list)
        for elem in TITLEBARINFO._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize(
        "field,typ",
        [
            ("cbSize", ctypes.wintypes.DWORD),
            ("rcTitleBar", ctypes.wintypes.RECT),
            ("rgstate", ctypes.wintypes.DWORD),
        ],
    )
    def test_TITLEBARINFO_has_field_with_type(self, field, typ):
        assert getattr(TITLEBARINFO, field, None) is not None
        assert isinstance(getattr(TITLEBARINFO, field), typ)


class TestWINDOWINFO(object):
    """Testing class for :py:class:`arrangeit.windows.collector.WINDOWINFO` class."""

    def test_WINDOWINFO_inits__fields_(self):
        assert getattr(WINDOWINFO, "_fields_", None) is not None
        assert isinstance(WINDOWINFO._fields_, list)
        for elem in WINDOWINFO._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize(
        "field,typ",
        [
            ("cbSize", ctypes.wintypes.DWORD),
            ("rcWindow", ctypes.wintypes.RECT),
            ("rcClient", ctypes.wintypes.RECT),
            ("dwStyle", ctypes.wintypes.DWORD),
            ("dwExStyle", ctypes.wintypes.DWORD),
            ("dwWindowStatus", ctypes.wintypes.DWORD),
            ("cxWindowBorders", ctypes.wintypes.UINT),
            ("cyWindowBorders", ctypes.wintypes.UINT),
            ("atomWindowType", ctypes.wintypes.ATOM),
            ("win32conreatorVersion", ctypes.wintypes.DWORD),
        ],
    )
    def test_WINDOWINFO_has_field_with_type(self, field, typ):
        assert getattr(WINDOWINFO, field, None) is not None
        assert isinstance(getattr(WINDOWINFO, field), typ)


class TestWindowsCollector(object):
    """Testing class for :py:class:`arrangeit.windows.collector.Collector` class."""

    ## WindowsCollector._is_tray_window
    @pytest.mark.parametrize(
        "method",
        [
            "arrangeit.windows.collector.TITLEBARINFO",
            "ctypes.windll.user32.GetTitleBarInfo",
            "ctypes.sizeof",
            "ctypes.byref",
        ],
    )
    def test_WindowsCollector__is_tray_window_calls(self, mocker, method):
        mocked = mocker.patch(method)
        Collector()._is_tray_window(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "rgstate,expected", [(1024 + STATE_SYSTEM_INVISIBLE, True), (1023, False)]
    )
    def test_WindowsCollector__is_tray_window_return(self, mocker, rgstate, expected):
        mocked = mocker.patch("arrangeit.windows.collector.TITLEBARINFO")
        type(mocked.return_value).rgstate = mocker.PropertyMock(return_value=rgstate)
        assert Collector()._is_tray_window(SAMPLE_HWND) == expected

    ## WindowsCollector._is_alt_tab_applicable
    @pytest.mark.parametrize(
        "method",
        [
            "ctypes.windll.user32.GetAncestor",
            "ctypes.windll.user32.GetLastActivePopup",
            "arrangeit.windows.collector.IsWindowVisible",
        ],
    )
    def test_WindowsCollector__is_alt_tab_applicable_calls(self, mocker, method):
        mocked = mocker.patch(method)
        Collector()._is_alt_tab_applicable(SAMPLE_HWND)
        mocked.assert_called_once()

    def test_WindowsCollector__is_alt_tab_applicable_return_True(self, mocker):
        VALUE = 500
        mocker.patch(
            "ctypes.windll.user32.GetAncestor",
            return_value=VALUE,
        )
        mocker.patch(
            "ctypes.windll.user32.GetLastActivePopup",
            return_value=VALUE,
        )
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        assert Collector()._is_alt_tab_applicable(SAMPLE_HWND)

    def test_WindowsCollector__is_alt_tab_applicable_return_False(self, mocker):
        mocker.patch(
            "ctypes.windll.user32.GetAncestor",
            return_value=500,
        )
        mocker.patch(
            "ctypes.windll.user32.GetLastActivePopup",
            return_value=499,
        )
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        assert not Collector()._is_alt_tab_applicable(SAMPLE_HWND)

    ## WindowsCollector._is_tool_window
    @pytest.mark.parametrize("method", ["GetWindowLong"])
    def test_WindowsCollector__is_tool_window_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector()._is_tool_window(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "value,expected", [(1024 + WS_EX_TOOLWINDOW, True), (1023, False)]
    )
    def test_WindowsCollector__is_tool_window_return(self, mocker, value, expected):
        mocker.patch("arrangeit.windows.collector.GetWindowLong", return_value=value)
        assert Collector()._is_tool_window(SAMPLE_HWND) == expected

    ## WindowsCollector.is_applicable
    @pytest.mark.parametrize(
        "method",
        [
            "IsWindow",
            "IsWindowEnabled",
            "IsWindowVisible",
            "Collector._is_alt_tab_applicable",
            "Collector._is_tray_window",
            "Collector._is_tool_window",
        ],
    )
    def test_WindowsCollector_is_applicable_calls(self, mocker, method):
        mocker.patch("arrangeit.windows.collector.IsWindow", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowEnabled", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_alt_tab_applicable",
            return_value=True,
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_tray_window", return_value=False
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_tool_window", return_value=False
        )
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector().is_applicable(SAMPLE_HWND)
        mocked.assert_called_once()

    ## WindowsCollector._is_activable
    @pytest.mark.parametrize(
        "method", ["arrangeit.windows.collector.WINDOWINFO", "ctypes.windll.user32.GetWindowInfo", "ctypes.byref"]
    )
    def test_WindowsCollector__is_activable_calls(self, mocker, method):
        mocked = mocker.patch(method)
        Collector()._is_activable(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "dwExStyle,expected", [(1024 + WS_EX_NOACTIVATE, True), (1023, False)]
    )
    def test_WindowsCollector__is_activable_return(self, mocker, dwExStyle, expected):
        mocked = mocker.patch("arrangeit.windows.collector.WINDOWINFO")
        type(mocked.return_value).dwExStyle = mocker.PropertyMock(
            return_value=dwExStyle
        )
        assert Collector()._is_activable(SAMPLE_HWND) == expected

    ## WindowsCollector.is_valid_state
    @pytest.mark.parametrize("method", ["_is_activable"])
    def test_WindowsCollector_is_valid_state_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.Collector.{}".format(method))
        Collector().is_valid_state(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "method,value,expected",
        [("_is_activable", True, True), ("_is_activable", False, False)],
    )
    def test_WindowsCollector_is_valid_state_return_value(
        self, mocker, method, value, expected
    ):
        mocker.patch(
            "arrangeit.windows.collector.Collector.{}".format(method),
            return_value=value,
        )
        assert Collector().is_valid_state(SAMPLE_HWND) == expected

    ## WindowsCollector.is_resizable
    @pytest.mark.parametrize("method", ["GetWindowLong"])
    def test_WindowsCollector_is_resizable_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector().is_resizable(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "value,expected", [(1024 + WS_THICKFRAME, True), (1023, False)]
    )
    def test_WindowsCollector_is_resizable_return(self, mocker, value, expected):
        mocker.patch("arrangeit.windows.collector.GetWindowLong", return_value=value)
        assert Collector().is_resizable(SAMPLE_HWND) == expected

    ## WindowsCollector.get_windows
    def test_WindowsCollector_get_windows_calls_EnumWindows(self, mocker):
        mocked = mocker.patch("arrangeit.windows.collector.EnumWindows")
        Collector().get_windows()
        mocked.assert_called_once()

    ## WindowsCollector.get_windows
    def test_WindowsCollector_get_windows_calls_append_to_collection(self, mocker):
        mocked = mocker.patch("arrangeit.windows.collector.append_to_collection")
        Collector().get_windows()
        mocked.assert_called()

    def test_WindowsCollector_get_windows_returns_non_empty_list(self):
        returned = Collector().get_windows()
        assert isinstance(returned, list)
        assert len(returned) > 0

    ## WindowsCollector.check_window
    @pytest.mark.parametrize("method", ["is_applicable", "is_valid_state"])
    def test_WindowsCollector_check_window_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.Collector.{}".format(method))
        Collector().check_window(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "is_applicable,is_valid_state,expected",
        [
            (True, True, True),
            (False, True, False),
            (True, False, False),
            (False, False, False),
        ],
    )
    def test_WindowsCollector_check_window_functionality(
        self, mocker, is_applicable, is_valid_state, expected
    ):
        mocker.patch(
            "arrangeit.windows.collector.is_applicable", return_value=is_applicable
        )
        mocker.patch(
            "arrangeit.windows.collector.is_valid_state", return_value=is_valid_state
        )
        assert Collector().check_window(SAMPLE_HWND) == expected

    ## WindowsCollector._get_window_geometry
    @pytest.mark.parametrize("method", ["GetWindowRect"])
    def test_WindowsCollector__get_window_geometry_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.Collector.{}".format(method))
        Collector()._get_window_geometry(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "rect,expected",
        [
            ((0, 0, 200, 300), (0, 0, 200, 300)),
            ((100, 200, 200, 300), (100, 200, 100, 100)),
            ((500, 400, 700, 500), (500, 400, 200, 100)),
            ((200, 200, 200, 300), (200, 200, 0, 100)),
        ],
    )
    def test_WindowsCollector__get_window_geometry_functionality(
        self, mocker, rect, expected
    ):
        mocker.patch("arrangeit.windows.collector.GetWindowRect", return_value=rect)
        assert Collector()._get_window_geometry(SAMPLE_HWND) == expected

    ## WindowsCollector._get_window_title
    @pytest.mark.parametrize("method", ["GetWindowText"])
    def test_WindowsCollector__get_window_title_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector()._get_window_title(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize("value", ["foo", "bar", ""])
    def test_WindowsCollector__get_window_title_functionality(self, mocker, value):
        mocker.patch("arrangeit.windows.collector.GetWindowText", return_value=value)
        assert Collector()._get_window_title(SAMPLE_HWND) == value

    ## WindowsCollector._get_class_name
    @pytest.mark.parametrize("method", ["GetClassName"])
    def test_WindowsCollector__get_class_name_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector()._get_class_name(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize("value", ["foo", "bar", ""])
    def test_WindowsCollector__get_class_name_functionality(self, mocker, value):
        mocker.patch("arrangeit.windows.collector.GetClassName", return_value=value)
        assert Collector()._get_class_name(SAMPLE_HWND) == value

    ## WindowsCollector.add_window
    def test_WindowsCollector_add_window_calls_WindowsCollection_add(self, mocker):
        mocked = mocker.patch("arrangeit.data.WindowsCollection.add")
        Collector().add_window(SAMPLE_HWND)
        mocked.assert_called_once()

    def test_WindowsCollector_add_window_inits_WindowModel(self, mocker):
        mocker.patch("arrangeit.data.WindowsCollection.add")
        mocked = mocker.patch("arrangeit.windows.collector.WindowModel")
        Collector().add_window(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "method",
        [
            "_get_window_geometry",
            "is_resizable",
            "_get_window_title",
            "_get_class_name",
        ],
    )
    def test_WindowsCollector_add_window_calls_methods(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.Collector.{}".format(method))
        Collector().add_window(SAMPLE_HWND)
        mocked.assert_called_once()

    ## WindowsCollector.__call__
    @pytest.mark.parametrize(
        "is_applicable,is_valid_state,value",
        [
            ((True, True), (True, True), 2),
            ((True, True), (True, False), 1),
            ((False, True), (True, True), 1),
            ((True, False), (False, True), 0),
            ((False, False), (False, False), 0),
        ],
    )
    def test_WindowsCollector___call___functionality(
        self, mocker, is_applicable, is_valid_state, value
    ):
        mocker.patch(
            "arrangeit.windows.collector.Collector.get_windows",
            return_value=(mocker.MagicMock(), mocker.MagicMock()),
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector.is_applicable",
            side_effect=is_applicable,
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector.is_valid_state",
            side_effect=is_valid_state,
        )
        collector = Collector()
        collector()
        assert collector.collection.size == value

