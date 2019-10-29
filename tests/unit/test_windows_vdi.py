# arrangeit - cross-platform desktop utility for easy windows management
# Copyright (C) 1999-2019 Ivica Paleka

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>

import ctypes
import ctypes.wintypes

import comtypes
import pytest
from comtypes.GUID import GUID

from arrangeit.windows import vdi
from arrangeit.windows.api import platform_supports_virtual_desktops
from arrangeit.windows.vdi import VirtualDesktopsWin10


## UIDS
class TestWindowsVdiModuleUids(object):
    """Testing class for :py:mod:`arrangeit.windows.vdi` module level attributes."""

    @pytest.mark.parametrize(
        "attr, uid",
        [
            ("CLSID_ImmersiveShell", "C2F03A33-21F5-47FA-B4BB-156362A2F239"),
            ("CLSID_VirtualDesktopManager", "AA509086-5CA9-4C25-8F95-589D3C07B48A"),
            (
                "CLSID_VirtualDesktopManagerInternal",
                "C5E0CDCA-7B6E-41B2-9FC4-D93975CC467B",
            ),
        ],
    )
    def test_windows_vdi_module_instantiates_clsid_attribute(self, attr, uid):
        assert hasattr(vdi, attr)
        assert isinstance(getattr(vdi, attr), GUID)
        assert uid in str(getattr(vdi, attr))

    @pytest.mark.parametrize(
        "attr, uid",
        [
            ("IID_IServiceProvider", "6D5140C1-7436-11CE-8034-00AA006009FA"),
            ("IID_IInspectable", "AF86E2E0-B12D-4C6A-9C5A-D7AA65101E90"),
            (
                "IID_IApplicationViewConsolidatedEventArgs",
                "514449EC-7EA2-4DE7-A6A6-7DFBAAEBB6FB",
            ),
            ("IID_IApplicationView", "D222D519-4361-451E-96C4-60F4F9742DB0"),
            ("IID_IApplicationViewCollection", "1841C6D7-4F9D-42C0-AF41-8747538F10E5"),
            ("IID_IVirtualDesktop", "FF72FFDD-BE7E-43FC-9C03-AD81681E88E4"),
            ("IID_IVirtualDesktopManager", "A5CD92FF-29BE-454C-8D04-D82879FB3F1B"),
            (
                "IID_IVirtualDesktopManagerInternal",
                "F31574D6-B682-4CDC-BD56-1827860ABEC6",
            ),
        ],
    )
    def test_windows_vdi_module_instantiates_iid_attribute(self, attr, uid):
        assert hasattr(vdi, attr)
        assert isinstance(getattr(vdi, attr), GUID)
        assert uid in str(getattr(vdi, attr))


## STRUCTURES
class TestWindowsVdiHSTRING__(object):
    """Testing class for :class:`arrangeit.windows.vdi.HSTRING__` class."""

    def test_windows_vdi_HSTRING___is_Structure_subclass(self):
        assert issubclass(vdi.HSTRING__, ctypes.Structure)

    def test_windows_api_HSTRING___inits__fields_(self):
        assert getattr(vdi.HSTRING__, "_fields_", None) is not None
        assert isinstance(vdi.HSTRING__._fields_, list)
        for elem in vdi.HSTRING__._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize("field,typ", [("unused", ctypes.wintypes.INT)])
    def test_windows_api_HSTRING___field_and_type(self, field, typ):
        assert (field, typ) in vdi.HSTRING__._fields_


class TestWindowsVdiEventRegistrationToken(object):
    """Testing class for :class:`arrangeit.windows.vdi.EventRegistrationToken` class."""

    def test_windows_vdi_EventRegistrationToken_is_Structure_subclass(self):
        assert issubclass(vdi.EventRegistrationToken, ctypes.Structure)

    def test_windows_api_EventRegistrationToken_inits__fields_(self):
        assert getattr(vdi.EventRegistrationToken, "_fields_", None) is not None
        assert isinstance(vdi.EventRegistrationToken._fields_, list)
        for elem in vdi.EventRegistrationToken._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize("field,typ", [("value", ctypes.c_int64)])
    def test_windows_api_EventRegistrationToken_field_and_type(self, field, typ):
        assert (field, typ) in vdi.EventRegistrationToken._fields_


## ENUMS
class TestWindowsVdiTrustLevel(object):
    """Testing class for :class:`arrangeit.windows.vdi.TrustLevel` class."""

    def test_windows_vdi_TrustLevel_is_INT_subclass(self):
        assert issubclass(vdi.TrustLevel, ctypes.wintypes.INT)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("BaseTrust", 0),
            ("PartialTrust", vdi.TrustLevel.BaseTrust + 1),
            ("FullTrust", vdi.TrustLevel.PartialTrust + 1),
        ],
    )
    def test_windows_vdi_TrustLevel_field_and_value(self, field, value):
        assert hasattr(vdi.TrustLevel, field)
        assert getattr(vdi.TrustLevel, field) == value


class TestWindowsVdiApplicationViewOrientation(object):
    """Testing class for :class:`arrangeit.windows.vdi.ApplicationViewOrientation` class."""

    def test_windows_vdi_ApplicationViewOrientation_is_INT_subclass(self):
        assert issubclass(vdi.ApplicationViewOrientation, ctypes.wintypes.INT)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("ApplicationViewOrientation_Landscape", 0),
            ("ApplicationViewOrientation_Portrait", 1),
        ],
    )
    def test_windows_vdi_ApplicationViewOrientation_field_and_value(self, field, value):
        assert hasattr(vdi.ApplicationViewOrientation, field)
        assert getattr(vdi.ApplicationViewOrientation, field) == value


class TestWindowsVdiAdjacentDesktop(object):
    """Testing class for :class:`arrangeit.windows.vdi.AdjacentDesktop` class."""

    def test_windows_vdi_AdjacentDesktop_is_INT_subclass(self):
        assert issubclass(vdi.AdjacentDesktop, ctypes.wintypes.INT)

    @pytest.mark.parametrize(
        "field,value", [("LeftDirection", 3), ("RightDirection", 4)]
    )
    def test_windows_vdi_AdjacentDesktop_field_and_value(self, field, value):
        assert hasattr(vdi.AdjacentDesktop, field)
        assert getattr(vdi.AdjacentDesktop, field) == value


## INTERFACES
class TestWindowsVdiIServiceProvider(object):
    """Testing class for :class:`arrangeit.windows.vdi.IServiceProvider` class."""

    def test_windows_vdi_IServiceProvider_is_IUnknown_subclass(self):
        assert issubclass(vdi.IServiceProvider, comtypes.IUnknown)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("_case_insensitive_", True),
            ("_iid_", vdi.IID_IServiceProvider),
            ("_idlflags_", []),
        ],
    )
    def test_windows_vdi_IServiceProvider_field_and_value(self, field, value):
        assert hasattr(vdi.IServiceProvider, field)
        assert getattr(vdi.IServiceProvider, field) == value

    def test_windows_vdi_IServiceProvider_method_QueryService(self):
        method = (
            ctypes.HRESULT,
            "QueryService",
            (
                ctypes.POINTER(GUID),
                ctypes.POINTER(GUID),
                ctypes.POINTER(ctypes.wintypes.LPVOID),
            ),
            ((1, "guidService"), (1, "riid"), (2, "ppvObject")),
            ("Method QueryService", "local", "in"),
            "Method QueryService",
        )
        assert method == vdi.IServiceProvider._methods_[0]


class TestWindowsVdiIObjectArray(object):
    """Testing class for :class:`arrangeit.windows.vdi.IObjectArray` class."""

    def test_windows_vdi_IObjectArray_is_IUnknown_subclass(self):
        assert issubclass(vdi.IObjectArray, comtypes.IUnknown)

    @pytest.mark.parametrize(
        "field,value",
        [("_case_insensitive_", True), ("_iid_", None), ("_idlflags_", [])],
    )
    def test_windows_vdi_IObjectArray_field_and_value(self, field, value):
        assert hasattr(vdi.IObjectArray, field)
        assert getattr(vdi.IObjectArray, field) == value

    def test_windows_vdi_IObjectArray_method_GetCount(self):
        method = (
            ctypes.HRESULT,
            "GetCount",
            (ctypes.POINTER(ctypes.wintypes.UINT),),
            ((2, "pcObjects"),),
            ("Method GetCount",),
            "Method GetCount",
        )
        assert method == vdi.IObjectArray._methods_[0]

    def test_windows_vdi_IObjectArray_method_GetAt(self):
        method = (
            ctypes.HRESULT,
            "GetAt",
            (
                ctypes.wintypes.UINT,
                ctypes.POINTER(GUID),
                ctypes.POINTER(ctypes.wintypes.LPVOID),
            ),
            ((1, "uiIndex"), (1, "riid"), (1, "ppv")),
            ("Method GetAt",),
            "Method GetAt",
        )
        assert method == vdi.IObjectArray._methods_[1]


class TestWindowsVdiIInspectable(object):
    """Testing class for :class:`arrangeit.windows.vdi.IInspectable` class."""

    def test_windows_vdi_IInspectable_is_IUnknown_subclass(self):
        assert issubclass(vdi.IInspectable, comtypes.IUnknown)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("_case_insensitive_", True),
            ("_iid_", vdi.IID_IInspectable),
            ("_idlflags_", []),
        ],
    )
    def test_windows_vdi_IInspectable_field_and_value(self, field, value):
        assert hasattr(vdi.IInspectable, field)
        assert getattr(vdi.IInspectable, field) == value

    def test_windows_vdi_IInspectable_method_GetIids(self):
        method = (
            ctypes.HRESULT,
            "GetIids",
            (
                ctypes.POINTER(ctypes.wintypes.ULONG),
                ctypes.POINTER(ctypes.POINTER(GUID)),
            ),
            ((2, "iidCount"), (2, "iids")),
            ("Method GetIids",),
            "Method GetIids",
        )
        assert method == vdi.IInspectable._methods_[0]

    def test_windows_vdi_IInspectable_method_GetRuntimeClassName(self):
        method = (
            ctypes.HRESULT,
            "GetRuntimeClassName",
            (ctypes.POINTER(ctypes.POINTER(vdi.HSTRING__)),),
            ((2, "className"),),
            ("Method GetRuntimeClassName",),
            "Method GetRuntimeClassName",
        )
        assert method == vdi.IInspectable._methods_[1]

    def test_windows_vdi_IInspectable_method_GetTrustLevel(self):
        method = (
            ctypes.HRESULT,
            "GetTrustLevel",
            (ctypes.POINTER(vdi.TrustLevel),),
            ((2, "trustLevel"),),
            ("Method GetTrustLevel",),
            "Method GetTrustLevel",
        )
        assert method == vdi.IInspectable._methods_[2]


class TestWindowsVdiIApplicationViewConsolidatedEventArgs(object):
    """Testing class for :class:`arrangeit.windows.vdi.IApplicationViewConsolidatedEventArgs` class."""

    def test_windows_vdi_IApplicationViewConsolidatedEventArgs_is_IInspectable_subclass(
        self,
    ):
        assert issubclass(vdi.IApplicationViewConsolidatedEventArgs, vdi.IInspectable)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("_case_insensitive_", True),
            ("_iid_", vdi.IID_IApplicationViewConsolidatedEventArgs),
            ("_idlflags_", []),
        ],
    )
    def test_windows_vdi_IApplicationViewConsolidatedEventArgs_field_and_value(
        self, field, value
    ):
        assert hasattr(vdi.IApplicationViewConsolidatedEventArgs, field)
        assert getattr(vdi.IApplicationViewConsolidatedEventArgs, field) == value

    def test_windows_vdi_IApplicationViewConsolidatedEventArgs_m_get_IsUserInitiated(
        self,
    ):
        method = (
            ctypes.HRESULT,
            "get_IsUserInitiated",
            (ctypes.POINTER(ctypes.wintypes.BOOL),),
            ((10, "value"),),
            ("Method get_IsUserInitiated",),
            "Method get_IsUserInitiated",
        )
        assert method == vdi.IApplicationViewConsolidatedEventArgs._methods_[0]


class TestWindowsVdiIApplicationView(object):
    """Testing class for :class:`arrangeit.windows.vdi.IApplicationView` class."""

    def test_windows_vdi_IApplicationView_is_IInspectable_subclass(self):
        assert issubclass(vdi.IApplicationView, vdi.IInspectable)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("_case_insensitive_", True),
            ("_iid_", vdi.IID_IApplicationView),
            ("_idlflags_", []),
        ],
    )
    def test_windows_vdi_IApplicationView_field_and_value(self, field, value):
        assert hasattr(vdi.IApplicationView, field)
        assert getattr(vdi.IApplicationView, field) == value

    def test_windows_vdi_IApplicationView_method_get_Orientation(self):
        method = (
            ctypes.HRESULT,
            "get_Orientation",
            (ctypes.POINTER(vdi.ApplicationViewOrientation),),
            ((10, "value"),),
            ("Method get_Orientation",),
            "Method get_Orientation",
        )
        assert method == vdi.IApplicationView._methods_[0]

    def test_windows_vdi_IApplicationView_method_get_AdjacentToLeftDisplayEdge(self):
        method = (
            ctypes.HRESULT,
            "get_AdjacentToLeftDisplayEdge",
            (ctypes.POINTER(ctypes.wintypes.BOOL),),
            ((10, "value"),),
            ("Method get_AdjacentToLeftDisplayEdge",),
            "Method get_AdjacentToLeftDisplayEdge",
        )
        assert method == vdi.IApplicationView._methods_[1]

    def test_windows_vdi_IApplicationView_method_get_AdjacentToRightDisplayEdge(self):
        method = (
            ctypes.HRESULT,
            "get_AdjacentToRightDisplayEdge",
            (ctypes.POINTER(ctypes.wintypes.BOOL),),
            ((10, "value"),),
            ("Method get_AdjacentToRightDisplayEdge",),
            "Method get_AdjacentToRightDisplayEdge",
        )
        assert method == vdi.IApplicationView._methods_[2]

    def test_windows_vdi_IApplicationView_method_get_IsFullScreen(self):
        method = (
            ctypes.HRESULT,
            "get_IsFullScreen",
            (ctypes.POINTER(ctypes.wintypes.BOOL),),
            ((10, "value"),),
            ("Method get_IsFullScreen",),
            "Method get_IsFullScreen",
        )
        assert method == vdi.IApplicationView._methods_[3]

    def test_windows_vdi_IApplicationView_method_get_IsOnLockScreen(self):
        method = (
            ctypes.HRESULT,
            "get_IsOnLockScreen",
            (ctypes.POINTER(ctypes.wintypes.BOOL),),
            ((10, "value"),),
            ("Method get_IsOnLockScreen",),
            "Method get_IsOnLockScreen",
        )
        assert method == vdi.IApplicationView._methods_[4]

    def test_windows_vdi_IApplicationView_method_get_IsScreenCaptureEnabled(self):
        method = (
            ctypes.HRESULT,
            "get_IsScreenCaptureEnabled",
            (ctypes.POINTER(ctypes.wintypes.BOOL),),
            ((10, "value"),),
            ("Method get_IsScreenCaptureEnabled",),
            "Method get_IsScreenCaptureEnabled",
        )
        assert method == vdi.IApplicationView._methods_[5]

    def test_windows_vdi_IApplicationView_method_put_IsScreenCaptureEnabled(self):
        method = (
            ctypes.HRESULT,
            "put_IsScreenCaptureEnabled",
            (ctypes.wintypes.BOOL,),
            ((1, "value"),),
            ("Method put_IsScreenCaptureEnabled",),
            "Method put_IsScreenCaptureEnabled",
        )
        assert method == vdi.IApplicationView._methods_[6]

    def test_windows_vdi_IApplicationView_method_put_Title(self):
        method = (
            ctypes.HRESULT,
            "put_Title",
            (ctypes.POINTER(vdi.HSTRING__),),
            ((1, "value"),),
            ("Method put_Title",),
            "Method put_Title",
        )
        assert method == vdi.IApplicationView._methods_[7]

    def test_windows_vdi_IApplicationView_method_get_Title(self):
        method = (
            ctypes.HRESULT,
            "get_Title",
            (ctypes.POINTER(ctypes.POINTER(vdi.HSTRING__)),),
            ((10, "value"),),
            ("Method get_Title",),
            "Method get_Title",
        )
        assert method == vdi.IApplicationView._methods_[8]

    def test_windows_vdi_IApplicationView_method_get_Id(self):
        method = (
            ctypes.HRESULT,
            "get_Id",
            (ctypes.POINTER(ctypes.c_int32),),
            ((10, "value"),),
            ("Method get_Id",),
            "Method get_Id",
        )
        assert method == vdi.IApplicationView._methods_[9]

    def test_windows_vdi_IApplicationView_method_add_Consolidated(self):
        method = (
            ctypes.HRESULT,
            "add_Consolidated",
            (
                ctypes.POINTER(vdi.IApplicationViewConsolidatedEventArgs),
                ctypes.POINTER(vdi.EventRegistrationToken),
            ),
            ((1, "handler"), (10, "token")),
            ("Method add_Consolidated",),
            "Method add_Consolidated",
        )
        assert method == vdi.IApplicationView._methods_[10]

    def test_windows_vdi_IApplicationView_method_remove_Consolidated(self):
        method = (
            ctypes.HRESULT,
            "remove_Consolidated",
            (vdi.EventRegistrationToken,),
            ((1, "EventRegistrationToken"),),
            ("Method remove_Consolidated",),
            "Method remove_Consolidated",
        )
        assert method == vdi.IApplicationView._methods_[11]


class TestWindowsVdiIApplicationViewCollection(object):
    """Testing class for :class:`arrangeit.windows.vdi.IApplicationViewCollection` class."""

    def test_windows_vdi_IApplicationViewCollection_is_IUnknown_subclass(self):
        assert issubclass(vdi.IApplicationViewCollection, comtypes.IUnknown)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("_case_insensitive_", True),
            ("_iid_", vdi.IID_IApplicationViewCollection),
            ("_idlflags_", []),
        ],
    )
    def test_windows_vdi_IApplicationViewCollection_field_and_value(self, field, value):
        assert hasattr(vdi.IApplicationViewCollection, field)
        assert getattr(vdi.IApplicationViewCollection, field) == value

    def test_windows_vdi_IApplicationViewCollection_method_GetViews(self):
        method = (
            ctypes.HRESULT,
            "GetViews",
            (ctypes.POINTER(ctypes.POINTER(vdi.IObjectArray)),),
            ((2, "array"),),
            ("Method GetViews",),
            "Method GetViews",
        )
        assert method == vdi.IApplicationViewCollection._methods_[0]

    def test_windows_vdi_IApplicationViewCollection_method_GetViewsByZOrder(self):
        method = (
            ctypes.HRESULT,
            "GetViewsByZOrder",
            (ctypes.POINTER(ctypes.POINTER(vdi.IObjectArray)),),
            ((2, "array"),),
            ("Method GetViewsByZOrder",),
            "Method GetViewsByZOrder",
        )
        assert method == vdi.IApplicationViewCollection._methods_[1]

    def test_windows_vdi_IApplicationViewCollection_method_GetViewsByAppUserModelId(
        self,
    ):
        method = (
            ctypes.HRESULT,
            "GetViewsByAppUserModelId",
            (ctypes.wintypes.LPCWSTR, ctypes.POINTER(ctypes.POINTER(vdi.IObjectArray))),
            ((1, "id"), (2, "array")),
            ("Method GetViewsByAppUserModelId",),
            "Method GetViewsByAppUserModelId",
        )
        assert method == vdi.IApplicationViewCollection._methods_[2]

    def test_windows_vdi_IApplicationViewCollection_method_GetViewForHwnd(self):
        method = (
            ctypes.HRESULT,
            "GetViewForHwnd",
            (
                ctypes.wintypes.HWND,
                ctypes.POINTER(ctypes.POINTER(vdi.IApplicationView)),
            ),
            ((1, "hwnd"), (2, "view")),
            ("Method GetViewForHwnd",),
            "Method GetViewForHwnd",
        )
        assert method == vdi.IApplicationViewCollection._methods_[3]

    def test_windows_vdi_IApplicationViewCollection_method_GetViewForApplication(self):
        method = (
            ctypes.HRESULT,
            "GetViewForApplication",
            (
                ctypes.POINTER(ctypes.wintypes.UINT),
                ctypes.POINTER(ctypes.POINTER(vdi.IApplicationView)),
            ),
            ((1, "application"), (2, "view")),
            ("Method GetViewForApplication",),
            "Method GetViewForApplication",
        )
        assert method == vdi.IApplicationViewCollection._methods_[4]

    def test_windows_vdi_IApplicationViewCollection_method_GetViewForAppUserModelId(
        self,
    ):
        method = (
            ctypes.HRESULT,
            "GetViewForAppUserModelId",
            (
                ctypes.wintypes.LPCWSTR,
                ctypes.POINTER(ctypes.POINTER(vdi.IApplicationView)),
            ),
            ((1, "id"), (2, "view")),
            ("Method GetViewForAppUserModelId",),
            "Method GetViewForAppUserModelId",
        )
        assert method == vdi.IApplicationViewCollection._methods_[5]

    def test_windows_vdi_IApplicationViewCollection_method_GetViewInFocus(self):
        method = (
            ctypes.HRESULT,
            "GetViewInFocus",
            (ctypes.POINTER(ctypes.POINTER(vdi.IApplicationView)),),
            ((2, "view"),),
            ("Method GetViewInFocus",),
            "Method GetViewInFocus",
        )
        assert method == vdi.IApplicationViewCollection._methods_[6]

    def test_windows_vdi_IApplicationViewCollection_method_Unknown1(self):
        method = (
            ctypes.HRESULT,
            "Unknown1",
            (ctypes.POINTER(ctypes.POINTER(vdi.IApplicationView)),),
            ((2, "view"),),
            ("Method Unknown1",),
            "Method Unknown1",
        )
        assert method == vdi.IApplicationViewCollection._methods_[7]

    def test_windows_vdi_IApplicationViewCollection_method_RefreshCollection(self):
        method = (
            ctypes.HRESULT,
            "RefreshCollection",
            (),
            (),
            ("Method RefreshCollection",),
            "Method RefreshCollection",
        )
        assert method == vdi.IApplicationViewCollection._methods_[8]

    def test_windows_vdi_IApplicationViewCollection_RegisterForApplicationViewChanges(
        self,
    ):
        method = (
            ctypes.HRESULT,
            "RegisterForApplicationViewChanges",
            (
                ctypes.POINTER(ctypes.wintypes.UINT),
                ctypes.POINTER(ctypes.wintypes.DWORD),
            ),
            ((1, "listener"), (2, "cookie")),
            ("Method RegisterForApplicationViewChanges",),
            "Method RegisterForApplicationViewChanges",
        )
        assert method == vdi.IApplicationViewCollection._methods_[9]

    def test_windows_vdi_IApplicationViewCollection_UnregisterForApplicationViewChanges(
        self,
    ):
        method = (
            ctypes.HRESULT,
            "UnregisterForApplicationViewChanges",
            (ctypes.wintypes.DWORD,),
            ((1, "cookie"),),
            ("Method UnregisterForApplicationViewChanges",),
            "Method UnregisterForApplicationViewChanges",
        )
        assert method == vdi.IApplicationViewCollection._methods_[10]


class TestWindowsVdiIVirtualDesktop(object):
    """Testing class for :class:`arrangeit.windows.vdi.IVirtualDesktop` class."""

    def test_windows_vdi_IVirtualDesktop_is_IUnknown_subclass(self):
        assert issubclass(vdi.IVirtualDesktop, comtypes.IUnknown)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("_case_insensitive_", True),
            ("_iid_", vdi.IID_IVirtualDesktop),
            ("_idlflags_", []),
        ],
    )
    def test_windows_vdi_IVirtualDesktop_field_and_value(self, field, value):
        assert hasattr(vdi.IVirtualDesktop, field)
        assert getattr(vdi.IVirtualDesktop, field) == value

    def test_windows_vdi_IVirtualDesktop_method_IsViewVisible(self):
        method = (
            ctypes.HRESULT,
            "IsViewVisible",
            (ctypes.POINTER(vdi.IApplicationView), ctypes.POINTER(ctypes.wintypes.INT)),
            ((2, "pView"), (2, "pfVisible")),
            ("Method IsViewVisible",),
            "Method IsViewVisible",
        )
        assert method == vdi.IVirtualDesktop._methods_[0]

    def test_windows_vdi_IVirtualDesktop_method_GetID(self):
        method = (
            ctypes.HRESULT,
            "GetID",
            (ctypes.POINTER(GUID),),
            ((2, "pGuid"),),
            ("Method GetID",),
            "Method GetID",
        )
        assert method == vdi.IVirtualDesktop._methods_[1]


class TestWindowsVdiIVirtualDesktopManager(object):
    """Testing class for :class:`arrangeit.windows.vdi.IVirtualDesktopManager` class."""

    def test_windows_vdi_IVirtualDesktopManager_is_IUnknown_subclass(self):
        assert issubclass(vdi.IVirtualDesktopManager, comtypes.IUnknown)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("_case_insensitive_", True),
            ("_iid_", vdi.IID_IVirtualDesktopManager),
            ("_idlflags_", []),
        ],
    )
    def test_windows_vdi_IVirtualDesktopManager_field_and_value(self, field, value):
        assert hasattr(vdi.IVirtualDesktopManager, field)
        assert getattr(vdi.IVirtualDesktopManager, field) == value

    def test_windows_vdi_IVirtualDesktopManager_method_IsWindowOnCurrentVirtualDesktop(
        self,
    ):
        method = (
            ctypes.HRESULT,
            "IsWindowOnCurrentVirtualDesktop",
            (ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.BOOL)),
            ((1, "topLevelWindow"), (2, "onCurrentDesktop")),
            ("Method IsWindowOnCurrentVirtualDesktop",),
            "Method IsWindowOnCurrentVirtualDesktop",
        )
        assert method == vdi.IVirtualDesktopManager._methods_[0]

    def test_windows_vdi_IVirtualDesktopManager_method_GetWindowDesktopId(self):
        method = (
            ctypes.HRESULT,
            "GetWindowDesktopId",
            (ctypes.wintypes.HWND, ctypes.POINTER(GUID)),
            ((1, "topLevelWindow"), (2, "desktopId")),
            ("Method GetWindowDesktopId",),
            "Method GetWindowDesktopId",
        )
        assert method == vdi.IVirtualDesktopManager._methods_[1]

    def test_windows_vdi_IVirtualDesktopManager_method_MoveWindowToDesktop(self):
        method = (
            ctypes.HRESULT,
            "MoveWindowToDesktop",
            (ctypes.wintypes.HWND, ctypes.POINTER(GUID)),
            ((1, "topLevelWindow"), (1, "desktopId")),
            ("Method MoveWindowToDesktop",),
            "Method MoveWindowToDesktop",
        )
        assert method == vdi.IVirtualDesktopManager._methods_[2]


class TestWindowsVdiIVirtualDesktopManagerInternal(object):
    """Testing class for :class:`arrangeit.windows.vdi.IVirtualDesktopManagerInternal` class."""

    def test_windows_vdi_IVirtualDesktopManagerInternal_is_IUnknown_subclass(self):
        assert issubclass(vdi.IVirtualDesktopManagerInternal, comtypes.IUnknown)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("_case_insensitive_", True),
            ("_iid_", vdi.IID_IVirtualDesktopManagerInternal),
            ("_idlflags_", []),
        ],
    )
    def test_windows_vdi_IVirtualDesktopManagerInternal_field_and_value(
        self, field, value
    ):
        assert hasattr(vdi.IVirtualDesktopManagerInternal, field)
        assert getattr(vdi.IVirtualDesktopManagerInternal, field) == value

    def test_windows_vdi_IVirtualDesktopManagerInternal_method_GetCount(self):
        method = (
            ctypes.HRESULT,
            "GetCount",
            (ctypes.POINTER(ctypes.wintypes.UINT),),
            ((1, "pCount"),),
            ("Method GetCount",),
            "Method GetCount",
        )
        assert method == vdi.IVirtualDesktopManagerInternal._methods_[0]

    def test_windows_vdi_IVirtualDesktopManagerInternal_method_MoveViewToDesktop(self):
        method = (
            ctypes.HRESULT,
            "MoveViewToDesktop",
            (ctypes.POINTER(vdi.IApplicationView), ctypes.POINTER(vdi.IVirtualDesktop)),
            ((1, "pView"), (1, "pDesktop")),
            ("Method MoveViewToDesktop",),
            "Method MoveViewToDesktop",
        )
        assert method == vdi.IVirtualDesktopManagerInternal._methods_[1]

    def test_windows_vdi_IVirtualDesktopManagerInternal_method_CanViewMoveDesktops(
        self,
    ):
        method = (
            ctypes.HRESULT,
            "CanViewMoveDesktops",
            (ctypes.POINTER(vdi.IApplicationView), ctypes.POINTER(ctypes.wintypes.INT)),
            ((2, "pView"), (2, "pfCanViewMoveDesktops")),
            ("Method CanViewMoveDesktops",),
            "Method CanViewMoveDesktops",
        )
        assert method == vdi.IVirtualDesktopManagerInternal._methods_[2]

    def test_windows_vdi_IVirtualDesktopManagerInternal_method_GetCurrentDesktop(self):
        method = (
            ctypes.HRESULT,
            "GetCurrentDesktop",
            (ctypes.POINTER(ctypes.POINTER(vdi.IVirtualDesktop)),),
            ((2, "desktop"),),
            ("Method GetCurrentDesktop",),
            "Method GetCurrentDesktop",
        )
        assert method == vdi.IVirtualDesktopManagerInternal._methods_[3]

    def test_windows_vdi_IVirtualDesktopManagerInternal_method_GetDesktops(self):
        method = (
            ctypes.HRESULT,
            "GetDesktops",
            (ctypes.POINTER(ctypes.POINTER(vdi.IObjectArray)),),
            ((2, "ppDesktops"),),
            ("Method GetDesktops",),
            "Method GetDesktops",
        )
        assert method == vdi.IVirtualDesktopManagerInternal._methods_[4]

    def test_windows_vdi_IVirtualDesktopManagerInternal_method_GetAdjacentDesktop(self):
        method = (
            ctypes.HRESULT,
            "GetAdjacentDesktop",
            (
                ctypes.POINTER(vdi.IVirtualDesktop),
                vdi.AdjacentDesktop,
                ctypes.POINTER(ctypes.POINTER(vdi.IVirtualDesktop)),
            ),
            ((2, "pDesktopReference"), (1, "uDirection"), (2, "ppAdjacentDesktop")),
            ("Method GetAdjacentDesktop",),
            "Method GetAdjacentDesktop",
        )
        assert method == vdi.IVirtualDesktopManagerInternal._methods_[5]

    def test_windows_vdi_IVirtualDesktopManagerInternal_method_SwitchDesktop(self):
        method = (
            ctypes.HRESULT,
            "SwitchDesktop",
            (ctypes.POINTER(vdi.IVirtualDesktop),),
            ((1, "pDesktop"),),
            ("Method SwitchDesktop",),
            "Method SwitchDesktop",
        )
        assert method == vdi.IVirtualDesktopManagerInternal._methods_[6]

    def test_windows_vdi_IVirtualDesktopManagerInternal_method_CreateDesktopW(self):
        method = (
            ctypes.HRESULT,
            "CreateDesktopW",
            (ctypes.POINTER(ctypes.POINTER(vdi.IVirtualDesktop)),),
            ((2, "ppNewDesktop"),),
            ("Method CreateDesktopW",),
            "Method CreateDesktopW",
        )
        assert method == vdi.IVirtualDesktopManagerInternal._methods_[7]

    def test_windows_vdi_IVirtualDesktopManagerInternal_method_RemoveDesktop(self):
        method = (
            ctypes.HRESULT,
            "RemoveDesktop",
            (ctypes.POINTER(vdi.IVirtualDesktop), ctypes.POINTER(vdi.IVirtualDesktop)),
            ((1, "pRemove"), (1, "pFallbackDesktop")),
            ("Method RemoveDesktop",),
            "Method RemoveDesktop",
        )
        assert method == vdi.IVirtualDesktopManagerInternal._methods_[8]

    def test_windows_vdi_IVirtualDesktopManagerInternal_method_FindDesktop(self):
        method = (
            ctypes.HRESULT,
            "FindDesktop",
            (ctypes.POINTER(GUID), ctypes.POINTER(ctypes.POINTER(vdi.IVirtualDesktop))),
            ((1, "desktopId"), (2, "ppDesktop")),
            ("Method FindDesktop",),
            "Method FindDesktop",
        )
        assert method == vdi.IVirtualDesktopManagerInternal._methods_[9]


## CUSTOM API
@pytest.mark.skipif(not platform_supports_virtual_desktops(), reason="Win 10 only")
class TestWindowsVdiVirtualDesktopsWin10(object):
    """Testing class for :class:`arrangeit.windows.vdi.VirtualDesktopsWin10` class."""

    # VirtualDesktopsWin10
    @pytest.mark.parametrize(
        "attr", ["manager", "internal_manager", "view_collection", "desktops"]
    )
    def test_windows_vdi_VirtualDesktopsWin10_inits_attr_as_None(self, attr):
        assert getattr(VirtualDesktopsWin10, attr) is None

    # VirtualDesktopsWin10.__init__
    def test_windows_vdi_VirtualDesktopsWin10__init__calls_setup(self, mocker):
        mocked = mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        VirtualDesktopsWin10()
        mocked.assert_called_once()
        mocked.assert_called_with()

    # VirtualDesktopsWin10._setup
    def test_windows_vdi_VirtualDesktopsWin10__setup_calls_CoInitialize(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_manager")
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_service_provider")
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_internal_manager")
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_view_collection")
        mocked = mocker.patch("comtypes.CoInitialize")
        vd = VirtualDesktopsWin10()
        mocked.reset_mock()
        vd._setup()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_windows_vdi_VirtualDesktopsWin10__setup_calls__get_manager_and_sets_attr(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_service_provider")
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_internal_manager")
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_view_collection")
        mocker.patch("comtypes.CoInitialize")
        mocked = mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_manager")
        vd = VirtualDesktopsWin10()
        mocked.reset_mock()
        vd.manager = None
        vd._setup()
        mocked.assert_called_once()
        mocked.assert_called_with()
        assert vd.manager == mocked.return_value

    def test_windows_vdi_VirtualDesktopsWin10__setup_calls__get_service_provider(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_internal_manager")
        mocker.patch("comtypes.CoInitialize")
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_manager")
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_view_collection")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_service_provider"
        )
        vd = VirtualDesktopsWin10()
        mocked.reset_mock()
        vd._setup()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_windows_vdi_VirtualDesktopsWin10__setup_calls__get_internal_manager_attr(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_manager")
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_view_collection")
        mocker.patch("comtypes.CoInitialize")
        mocked_provider = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_service_provider"
        )
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_internal_manager"
        )
        vd = VirtualDesktopsWin10()
        mocked.reset_mock()
        vd.internal_manager = None
        vd._setup()
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_provider.return_value)
        assert vd.internal_manager == mocked.return_value

    def test_windows_vdi_VirtualDesktopsWin10__setup_calls__get_view_collection_attr(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_manager")
        mocker.patch("comtypes.CoInitialize")
        mocked_provider = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_service_provider"
        )
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._get_internal_manager")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_view_collection"
        )
        vd = VirtualDesktopsWin10()
        mocked.reset_mock()
        vd.view_collection = None
        vd._setup()
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_provider.return_value)
        assert vd.view_collection == mocked.return_value

    # VirtualDesktopsWin10._get_desktop_id_from_array
    def test_windows_vdi_VDWin10__get_desktop_id_from_array_calls_POINTER(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("ctypes.POINTER")
        VirtualDesktopsWin10()._get_desktop_id_from_array(mocker.MagicMock(), 0)
        mocked.assert_called_once()
        mocked.assert_called_with(vdi.IVirtualDesktop)

    def test_windows_vdi_VDWin10__get_desktop_id_from_array_instantiates_POINTER(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("ctypes.POINTER")
        VirtualDesktopsWin10()._get_desktop_id_from_array(mocker.MagicMock(), 0)
        mocked.return_value.assert_called_once()
        mocked.return_value.assert_called_with()

    def test_windows_vdi_VDWin10__get_desktop_id_from_array_calls_byref(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked_pointer = mocker.patch("ctypes.POINTER")
        mocked = mocker.patch("ctypes.byref")
        VirtualDesktopsWin10()._get_desktop_id_from_array(mocker.MagicMock(), 0)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_pointer.return_value.return_value)

    def test_windows_vdi_VDWin10__get_desktop_id_from_array_calls_array_GetAt(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("ctypes.POINTER")
        mocked = mocker.patch("ctypes.byref")
        array, INDEX = mocker.MagicMock(), 1
        VirtualDesktopsWin10()._get_desktop_id_from_array(array, INDEX)
        array.GetAt.assert_called_once()
        array.GetAt.assert_called_with(
            INDEX, vdi.IID_IVirtualDesktop, mocked.return_value
        )

    def test_windows_vdi_VDWin10__get_desktop_id_from_array_calls__and_returns_GetID(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("ctypes.POINTER")
        returned = VirtualDesktopsWin10()._get_desktop_id_from_array(
            mocker.MagicMock(), 0
        )
        mocked.return_value.return_value.GetID.assert_called_once()
        mocked.return_value.return_value.GetID.assert_called_with()
        assert returned == mocked.return_value.return_value.GetID.return_value

    # VirtualDesktopsWin10._get_desktop_id_from_ordinal
    def test_windows_vdi_VDWin10__get_desktop_id_from_ordinal_calls_get_desktops(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10.get_desktops",
            return_value=[(0, ""), (1, "barfoo")],
        )
        vd = VirtualDesktopsWin10()
        vd._get_desktop_id_from_ordinal(1)
        mocked.assert_called_once()
        mocked.assert_called_with()

    @pytest.mark.parametrize("ordinal,expected", [(0, ""), (1, "barfoo"), (2, "foo")])
    def test_windows_vdi_VDWin10__get_desktop_id_from_ordinal_functionality(
        self, mocker, ordinal, expected
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10.get_desktops",
            return_value=[(0, ""), (1, "barfoo"), (2, "foo")],
        )
        vd = VirtualDesktopsWin10()
        returned = vd._get_desktop_id_from_ordinal(ordinal)
        assert returned == expected

    # VirtualDesktopsWin10._get_desktops
    def test_windows_vdi_VDWin10__get_desktops_calls_GetDesktops(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_array"
        )
        vd = VirtualDesktopsWin10()
        vd.internal_manager = mocker.MagicMock()
        vd._get_desktops()
        vd.internal_manager.GetDesktops.assert_called_once()
        vd.internal_manager.GetDesktops.assert_called_with()

    def test_windows_vdi_VDWin10__get_desktops_calls_GetCount(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_array"
        )
        vd = VirtualDesktopsWin10()
        vd.internal_manager = mocker.MagicMock()
        vd._get_desktops()
        vd.internal_manager.GetDesktops.return_value.GetCount.assert_called_once()
        vd.internal_manager.GetDesktops.return_value.GetCount.assert_called_with()

    def test_windows_vdi_VDWin10__get_desktops_calls__get_desktop_id_from_array(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_array"
        )
        vd = VirtualDesktopsWin10()
        vd.internal_manager = mocker.MagicMock()
        vd.internal_manager.GetDesktops.return_value.GetCount.return_value = 2
        vd._get_desktops()
        calls = [
            mocker.call(vd.internal_manager.GetDesktops.return_value, 0),
            mocker.call(vd.internal_manager.GetDesktops.return_value, 1),
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_windows_vdi_VDWin10__get_desktops_returns_list(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_array"
        )
        vd = VirtualDesktopsWin10()
        vd.internal_manager = mocker.MagicMock()
        vd.internal_manager.GetDesktops.return_value.GetCount.return_value = 1
        returned = vd._get_desktops()
        assert returned == [(0, mocked.return_value)]

    # VirtualDesktopsWin10._get_internal_manager
    def test_windows_vdi_VDWin10__get_internal_manager_calls_QueryService(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("ctypes.POINTER")
        mocker.patch("comtypes.cast")
        provider = mocker.MagicMock()
        VirtualDesktopsWin10()._get_internal_manager(provider)
        provider.QueryService.assert_called_once()
        provider.QueryService.assert_called_with(
            vdi.CLSID_VirtualDesktopManagerInternal,
            vdi.IID_IVirtualDesktopManagerInternal,
        )

    def test_windows_vdi_VDWin10__get_internal_manager_calls_POINTER(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("comtypes.cast")
        mocked = mocker.patch("ctypes.POINTER")
        VirtualDesktopsWin10()._get_internal_manager(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with(vdi.IVirtualDesktopManagerInternal)

    def test_windows_vdi_VDWin10__get_internal_manager_calls_and_returns_ctypes_cast(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked = mocker.patch("comtypes.cast")
        mocked_pointer = mocker.patch("ctypes.POINTER")
        provider = mocker.MagicMock()
        returned = VirtualDesktopsWin10()._get_internal_manager(provider)
        mocked.assert_called_once()
        mocked.assert_called_with(
            provider.QueryService.return_value, mocked_pointer.return_value
        )
        assert returned == mocked.return_value

    # VirtualDesktopsWin10._get_manager
    def test_windows_vdi_VDWin10__get_manager_calls_and_returns_CoCreateInstance(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked = mocker.patch("comtypes.CoCreateInstance")
        returned = VirtualDesktopsWin10()._get_manager()
        mocked.assert_called_once()
        mocked.assert_called_with(
            vdi.CLSID_VirtualDesktopManager, vdi.IVirtualDesktopManager
        )
        assert returned == mocked.return_value

    # VirtualDesktopsWin10._get_service_provider
    def test_windows_vdi_VDWin10__get_service_provider_calls_and_returns_CoCreateInstance(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked = mocker.patch("comtypes.CoCreateInstance")
        returned = VirtualDesktopsWin10()._get_service_provider()
        mocked.assert_called_once()
        mocked.assert_called_with(
            vdi.CLSID_ImmersiveShell, vdi.IServiceProvider, comtypes.CLSCTX_LOCAL_SERVER
        )
        assert returned == mocked.return_value

    # VirtualDesktopsWin10._get_view_collection
    def test_windows_vdi_VDWin10__get_view_collection_calls_QueryService(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("ctypes.POINTER")
        mocker.patch("comtypes.cast")
        provider = mocker.MagicMock()
        VirtualDesktopsWin10()._get_view_collection(provider)
        provider.QueryService.assert_called_once()
        provider.QueryService.assert_called_with(
            vdi.IID_IApplicationViewCollection, vdi.IID_IApplicationViewCollection
        )

    def test_windows_vdi_VDWin10__get_view_collection_calls_POINTER(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("comtypes.cast")
        mocked = mocker.patch("ctypes.POINTER")
        VirtualDesktopsWin10()._get_view_collection(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with(vdi.IApplicationViewCollection)

    def test_windows_vdi_VDWin10__get_view_collection_calls_and_returns_ctypes_cast(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked = mocker.patch("comtypes.cast")
        mocked_pointer = mocker.patch("ctypes.POINTER")
        provider = mocker.MagicMock()
        returned = VirtualDesktopsWin10()._get_view_collection(provider)
        mocked.assert_called_once()
        mocked.assert_called_with(
            provider.QueryService.return_value, mocked_pointer.return_value
        )
        assert returned == mocked.return_value

    # VirtualDesktopsWin10.get_desktops
    def test_windows_vdi_VDWin10_get_desktops_calls__get_desktops_for_None(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktops"
        )
        vd = VirtualDesktopsWin10()
        vd.desktops = None
        returned = vd.get_desktops()
        mocked.assert_called_once()
        mocked.assert_called_with()
        assert returned == mocked.return_value

    def test_windows_vdi_VDWin10_get_desktops_calls__get_desktops_for_refresh_True(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktops"
        )
        vd = VirtualDesktopsWin10()
        vd.desktops = "foo"
        returned = vd.get_desktops(refresh=True)
        mocked.assert_called_once()
        mocked.assert_called_with()
        assert returned == mocked.return_value

    def test_windows_vdi_VDWin10_get_desktops_not_calling__get_desktops(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktops"
        )
        vd = VirtualDesktopsWin10()
        VALUE = "foo"
        vd.desktops = VALUE
        returned = vd.get_desktops(refresh=False)
        mocked.assert_not_called()
        assert returned == VALUE

    # VirtualDesktopsWin10.get_window_desktop
    def test_windows_vdi_VDWin10_get_window_desktop_calls_GetWindowDesktopId(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("arrangeit.windows.vdi.next")
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10.get_desktops")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        HWND = 972
        vd.get_window_desktop(HWND)
        vd.manager.GetWindowDesktopId.assert_called_once()
        vd.manager.GetWindowDesktopId.assert_called_with(HWND)

    def test_windows_vdi_VDWin10_get_window_desktop_calls_get_desktops(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("arrangeit.windows.vdi.next")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10.get_desktops",
            return_value=[(0, "")],
        )
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        REFRESH = True
        vd.get_window_desktop(974, REFRESH)
        mocked.assert_called_once()
        mocked.assert_called_with(REFRESH)

    def test_windows_vdi_VDWin10_get_window_desktop_calls_next(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10.get_desktops",
            return_value=[(0, "")],
        )
        mocked = mocker.patch("arrangeit.windows.vdi.next")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.get_window_desktop(975)
        mocked.assert_called_once()

    def test_windows_vdi_VDWin10_get_window_desktop_returns_tuple(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        ID = "foobar"
        DESKTOP = (1, ID)
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10.get_desktops",
            return_value=[(0, ""), DESKTOP],
        )
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.manager.GetWindowDesktopId.return_value = ID
        returned = vd.get_window_desktop(976)
        assert returned == DESKTOP

    def test_windows_vdi_VDWin10_get_window_desktop_returns_0_None_for_no_desktop(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10.get_desktops",
            return_value=[(0, ""), (1, "barfoo")],
        )
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.manager.GetWindowDesktopId.return_value = "foo"
        returned = vd.get_window_desktop(977)
        assert returned == (0, None)

    # VirtualDesktopsWin10.is_window_in_current_desktop
    def test_windows_vdi_VDWin10_is_window_in_current_desktop_calls_IsWindowOnCurrent(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        HWND = 22
        returned = vd.is_window_in_current_desktop(HWND)
        vd.manager.IsWindowOnCurrentVirtualDesktop.assert_called_once()
        vd.manager.IsWindowOnCurrentVirtualDesktop.assert_called_with(HWND)
        assert returned == vd.manager.IsWindowOnCurrentVirtualDesktop.return_value

    # VirtualDesktopsWin10.move_other_window_to_desktop
    def test_windows_vdi_VDWin10_move_other_window_to_desktop_get_desktop_id_from_ord(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        vd = VirtualDesktopsWin10()
        vd.view_collection = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        ORDINAL = 1
        vd.move_other_window_to_desktop(8720, ORDINAL)
        mocked.assert_called_once()
        mocked.assert_called_with(ORDINAL)

    def test_windows_vdi_VDWin10_move_other_window_to_desktop_calls_byref(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        VALUE = "barfoo"
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal",
            return_value=VALUE,
        )
        mocked = mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.view_collection = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.move_other_window_to_desktop(8721, 1)
        mocked.assert_called_once()
        mocked.assert_called_with(VALUE)

    def test_windows_vdi_VDWin10_move_other_window_to_desktop_calls_FindDesktop(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocked = mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.view_collection = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.move_other_window_to_desktop(9420, 1)
        vd.internal_manager.FindDesktop.assert_called_once()
        vd.internal_manager.FindDesktop.assert_called_with(mocked.return_value)

    def test_windows_vdi_VDWin10_move_other_window_to_desktop_calls_GetViewForHwnd(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.view_collection = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        HWND = 5400
        vd.move_other_window_to_desktop(HWND, 1)
        vd.view_collection.GetViewForHwnd.assert_called_once()
        vd.view_collection.GetViewForHwnd.assert_called_with(HWND)

    def test_windows_vdi_VDWin10_move_other_window_to_desktop_calls_MoveViewToDesktop(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.view_collection = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.move_other_window_to_desktop(5401, 1)
        vd.internal_manager.MoveViewToDesktop.assert_called_once()
        vd.internal_manager.MoveViewToDesktop.assert_called_with(
            vd.view_collection.GetViewForHwnd.return_value,
            vd.internal_manager.FindDesktop.return_value,
        )

    def test_windows_vdi_VDWin10_move_other_window_to_desktop_returns_None_for_not_ok(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.view_collection = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.internal_manager.MoveViewToDesktop.return_value = 1
        returned = vd.move_other_window_to_desktop(5402, 1)
        assert returned is None

    def test_windows_vdi_VDWin10_move_other_window_to_desktop_returns_False(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.view_collection = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.internal_manager.MoveViewToDesktop.return_value = vdi.S_OK
        returned = vd.move_other_window_to_desktop(5403, 1)
        assert returned is False

    # VirtualDesktopsWin10.move_own_window_to_desktop
    def test_windows_vdi_VDWin10_move_own_window_to_desktop_get_desktop_id_from_ordinal(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        ORDINAL = 1
        vd.move_own_window_to_desktop(140, ORDINAL)
        mocked.assert_called_once()
        mocked.assert_called_with(ORDINAL)

    def test_windows_vdi_VDWin10_move_own_window_to_desktop_calls_byref(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        VALUE = "barfoo"
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal",
            return_value=VALUE,
        )
        mocked = mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.manager.MoveWindowToDesktop.return_value = 1
        vd.internal_manager = mocker.MagicMock()
        vd.move_own_window_to_desktop(141, 1)
        mocked.assert_called_once()
        mocked.assert_called_with(VALUE)

    def test_windows_vdi_VDWin10_move_own_window_to_desktop_calls_MoveWindowToDesktop(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocked = mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        HWND = 142
        vd.move_own_window_to_desktop(HWND, 1)
        vd.manager.MoveWindowToDesktop.assert_called_once()
        vd.manager.MoveWindowToDesktop.assert_called_with(HWND, mocked.return_value)

    def test_windows_vdi_VDWin10_move_own_window_to_desktop_returns_None_for_move_not_ok(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.manager.MoveWindowToDesktop.return_value = 1
        returned = vd.move_own_window_to_desktop(143, 0)
        assert returned is None

    def test_windows_vdi_VDWin10_move_own_window_to_desktop_calls_byref_find(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        VALUE = "barfoo"
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal",
            return_value=VALUE,
        )
        mocked = mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.manager.MoveWindowToDesktop.return_value = vdi.S_OK
        vd.move_own_window_to_desktop(141, 1)
        assert mocked.call_count == 2
        mocked.assert_called_with(VALUE)

    def test_windows_vdi_VDWin10_move_own_window_to_desktop_calls_FindDesktop(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocked = mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.manager.MoveWindowToDesktop.return_value = vdi.S_OK
        vd.move_own_window_to_desktop(2800, 1)
        vd.internal_manager.FindDesktop.assert_called_once()
        vd.internal_manager.FindDesktop.assert_called_with(mocked.return_value)

    def test_windows_vdi_VDWin10_move_own_window_to_desktop_calls_SwitchDesktop(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.manager.MoveWindowToDesktop.return_value = vdi.S_OK
        vd.move_own_window_to_desktop(2801, 1)
        vd.internal_manager.SwitchDesktop.assert_called_once()
        vd.internal_manager.SwitchDesktop.assert_called_with(
            vd.internal_manager.FindDesktop.return_value
        )

    def test_windows_vdi_VDWin10_move_own_window_to_desktop_returns_None_for_Switch(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.manager.MoveWindowToDesktop.return_value = vdi.S_OK
        vd.internal_manager.SwitchDesktop.return_value = 1
        returned = vd.move_own_window_to_desktop(2802, 1)
        assert returned is None

    def test_windows_vdi_VDWin10_move_own_window_to_desktop_returns_False(self, mocker):
        mocker.patch("arrangeit.windows.vdi.VirtualDesktopsWin10._setup")
        mocker.patch(
            "arrangeit.windows.vdi.VirtualDesktopsWin10._get_desktop_id_from_ordinal"
        )
        mocker.patch("ctypes.byref")
        vd = VirtualDesktopsWin10()
        vd.manager = mocker.MagicMock()
        vd.internal_manager = mocker.MagicMock()
        vd.manager.MoveWindowToDesktop.return_value = vdi.S_OK
        vd.internal_manager.SwitchDesktop.return_value = vdi.S_OK
        returned = vd.move_own_window_to_desktop(2803, 1)
        assert returned is False
