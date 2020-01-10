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

"""
Code from this module is based on the blog <http://www.cyberforum.ru/blogs/105416/blog3671.html>.
The Python implementation is based on the work by @kdschlosser
<https://github.com/DanEdens/Virtual_Desktops_Plugin/blob/master/Virtualdesktops/__int__.py>
(<http://www.eventghost.net>, <http://www.eventghost.net/forum/viewtopic.php?p=53308#p53308>)
"""

import ctypes
import ctypes.wintypes

import comtypes
from comtypes import COMMETHOD, helpstring
from comtypes.GUID import GUID

S_OK = 0x00000000

## UIDS
CLSID_ImmersiveShell = GUID("{C2F03A33-21F5-47FA-B4BB-156362A2F239}")
CLSID_VirtualDesktopManager = GUID("{AA509086-5CA9-4C25-8F95-589D3C07B48A}")
CLSID_VirtualDesktopManagerInternal = GUID("{C5E0CDCA-7B6E-41B2-9FC4-D93975CC467B}")

IID_IServiceProvider = GUID("{6D5140C1-7436-11CE-8034-00AA006009FA}")
IID_IInspectable = GUID("{AF86E2E0-B12D-4C6A-9C5A-D7AA65101E90}")
IID_IApplicationViewConsolidatedEventArgs = GUID(
    "{514449EC-7EA2-4DE7-A6A6-7DFBAAEBB6FB}"
)
IID_IApplicationView = GUID("{D222D519-4361-451E-96C4-60F4F9742DB0}")
IID_IApplicationViewCollection = GUID("{1841C6D7-4F9D-42C0-AF41-8747538F10E5}")
IID_IVirtualDesktop = GUID("{FF72FFDD-BE7E-43FC-9C03-AD81681E88E4}")
IID_IVirtualDesktopManager = GUID("{A5CD92FF-29BE-454C-8D04-D82879FB3F1B}")
IID_IVirtualDesktopManagerInternal = GUID("{F31574D6-B682-4CDC-BD56-1827860ABEC6}")


## STRUCTURES
class HSTRING__(ctypes.Structure):
    """Class holding structure for the immutable strings in the Windows Runtime."""

    _fields_ = [("unused", ctypes.wintypes.INT)]


class EventRegistrationToken(ctypes.Structure):
    """Class holding structure for a delegate that receives change notifications."""

    _fields_ = [("value", ctypes.c_int64)]


## ENUMS
class TrustLevel(ctypes.wintypes.INT):
    """Enum holding trust level of an activatable class."""

    BaseTrust = 0
    PartialTrust = BaseTrust + 1
    FullTrust = PartialTrust + 1


class ApplicationViewOrientation(ctypes.wintypes.INT):
    """Enum holding application view's orientation values."""

    ApplicationViewOrientation_Landscape = 0
    ApplicationViewOrientation_Portrait = 1


class AdjacentDesktop(ctypes.wintypes.INT):
    """Enum holding identifying values for neighbouring desktops."""

    LeftDirection = 3
    RightDirection = 4


## INTERFACES
class IServiceProvider(comtypes.IUnknown):
    """Interface that provides custom support to other objects."""

    _case_insensitive_ = True
    _iid_ = IID_IServiceProvider
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method QueryService"), "local", "in"],
            ctypes.HRESULT,
            "QueryService",
            (["in"], ctypes.POINTER(GUID), "guidService"),
            (["in"], ctypes.POINTER(GUID), "riid"),
            (["out"], ctypes.POINTER(ctypes.wintypes.LPVOID), "ppvObject"),
        )
    ]


class IObjectArray(comtypes.IUnknown):
    """Interface for accessing collection of objects based on IUnknown interface."""

    _case_insensitive_ = True
    _iid_ = None
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method GetCount")],
            ctypes.HRESULT,
            "GetCount",
            (["out"], ctypes.POINTER(ctypes.wintypes.UINT), "pcObjects"),
        ),
        COMMETHOD(
            [helpstring("Method GetAt")],
            ctypes.HRESULT,
            "GetAt",
            (["in"], ctypes.wintypes.UINT, "uiIndex"),
            (["in"], ctypes.POINTER(GUID), "riid"),
            (["in", "iid_is"], ctypes.POINTER(ctypes.wintypes.LPVOID), "ppv"),
        ),
    ]


class IInspectable(comtypes.IUnknown):
    """Interface that provides functionality required for all Windows Runtime classes."""

    _case_insensitive_ = True
    _iid_ = IID_IInspectable
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method GetIids")],
            ctypes.HRESULT,
            "GetIids",
            (["out"], ctypes.POINTER(ctypes.wintypes.ULONG), "iidCount"),
            (["out"], ctypes.POINTER(ctypes.POINTER(GUID)), "iids"),
        ),
        COMMETHOD(
            [helpstring("Method GetRuntimeClassName")],
            ctypes.HRESULT,
            "GetRuntimeClassName",
            (["out"], ctypes.POINTER(ctypes.POINTER(HSTRING__)), "className"),
        ),
        COMMETHOD(
            [helpstring("Method GetTrustLevel")],
            ctypes.HRESULT,
            "GetTrustLevel",
            (["out"], ctypes.POINTER(TrustLevel), "trustLevel"),
        ),
    ]


class IApplicationViewConsolidatedEventArgs(IInspectable):
    """Interface providing the results of application view consolidation operations."""

    _case_insensitive_ = True
    _iid_ = IID_IApplicationViewConsolidatedEventArgs
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method get_IsUserInitiated")],
            ctypes.HRESULT,
            "get_IsUserInitiated",
            (["retval", "out"], ctypes.POINTER(ctypes.wintypes.BOOL), "value"),
        )
    ]


class IApplicationView(IInspectable):
    """Interface that provides view for the top-level application information."""

    _case_insensitive_ = True
    _iid_ = IID_IApplicationView
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method get_Orientation")],
            ctypes.HRESULT,
            "get_Orientation",
            (["retval", "out"], ctypes.POINTER(ApplicationViewOrientation), "value"),
        ),
        COMMETHOD(
            [helpstring("Method get_AdjacentToLeftDisplayEdge")],
            ctypes.HRESULT,
            "get_AdjacentToLeftDisplayEdge",
            (["retval", "out"], ctypes.POINTER(ctypes.wintypes.BOOL), "value"),
        ),
        COMMETHOD(
            [helpstring("Method get_AdjacentToRightDisplayEdge")],
            ctypes.HRESULT,
            "get_AdjacentToRightDisplayEdge",
            (["retval", "out"], ctypes.POINTER(ctypes.wintypes.BOOL), "value"),
        ),
        COMMETHOD(
            [helpstring("Method get_IsFullScreen")],
            ctypes.HRESULT,
            "get_IsFullScreen",
            (["retval", "out"], ctypes.POINTER(ctypes.wintypes.BOOL), "value"),
        ),
        COMMETHOD(
            [helpstring("Method get_IsOnLockScreen")],
            ctypes.HRESULT,
            "get_IsOnLockScreen",
            (["retval", "out"], ctypes.POINTER(ctypes.wintypes.BOOL), "value"),
        ),
        COMMETHOD(
            [helpstring("Method get_IsScreenCaptureEnabled")],
            ctypes.HRESULT,
            "get_IsScreenCaptureEnabled",
            (["retval", "out"], ctypes.POINTER(ctypes.wintypes.BOOL), "value"),
        ),
        COMMETHOD(
            [helpstring("Method put_IsScreenCaptureEnabled")],
            ctypes.HRESULT,
            "put_IsScreenCaptureEnabled",
            (["in"], ctypes.wintypes.BOOL, "value"),
        ),
        COMMETHOD(
            [helpstring("Method put_Title")],
            ctypes.HRESULT,
            "put_Title",
            (["in"], ctypes.POINTER(HSTRING__), "value"),
        ),
        COMMETHOD(
            [helpstring("Method get_Title")],
            ctypes.HRESULT,
            "get_Title",
            (["retval", "out"], ctypes.POINTER(ctypes.POINTER(HSTRING__)), "value"),
        ),
        COMMETHOD(
            [helpstring("Method get_Id")],
            ctypes.HRESULT,
            "get_Id",
            (["retval", "out"], ctypes.POINTER(ctypes.c_int32), "value"),
        ),
        COMMETHOD(
            [helpstring("Method add_Consolidated")],
            ctypes.HRESULT,
            "add_Consolidated",
            (["in"], ctypes.POINTER(IApplicationViewConsolidatedEventArgs), "handler"),
            (["retval", "out"], ctypes.POINTER(EventRegistrationToken), "token"),
        ),
        COMMETHOD(
            [helpstring("Method remove_Consolidated")],
            ctypes.HRESULT,
            "remove_Consolidated",
            (["in"], EventRegistrationToken, "EventRegistrationToken"),
        ),
    ]


class IApplicationViewCollection(comtypes.IUnknown):
    """Interface to collection of application views for specified data group."""

    _case_insensitive_ = True
    _idlflags_ = []
    _iid_ = IID_IApplicationViewCollection
    _methods_ = [
        COMMETHOD(
            [helpstring("Method GetViews")],
            ctypes.HRESULT,
            "GetViews",
            (["out"], ctypes.POINTER(ctypes.POINTER(IObjectArray)), "array"),
        ),
        COMMETHOD(
            [helpstring("Method GetViewsByZOrder")],
            ctypes.HRESULT,
            "GetViewsByZOrder",
            (["out"], ctypes.POINTER(ctypes.POINTER(IObjectArray)), "array"),
        ),
        COMMETHOD(
            [helpstring("Method GetViewsByAppUserModelId")],
            ctypes.HRESULT,
            "GetViewsByAppUserModelId",
            (["in"], ctypes.wintypes.LPCWSTR, "id"),
            (["out"], ctypes.POINTER(ctypes.POINTER(IObjectArray)), "array"),
        ),
        COMMETHOD(
            [helpstring("Method GetViewForHwnd")],
            ctypes.HRESULT,
            "GetViewForHwnd",
            (["in"], ctypes.wintypes.HWND, "hwnd"),
            (["out"], ctypes.POINTER(ctypes.POINTER(IApplicationView)), "view"),
        ),
        COMMETHOD(
            [helpstring("Method GetViewForApplication")],
            ctypes.HRESULT,
            "GetViewForApplication",
            (["in"], ctypes.POINTER(ctypes.wintypes.UINT), "application"),
            (["out"], ctypes.POINTER(ctypes.POINTER(IApplicationView)), "view"),
        ),
        COMMETHOD(
            [helpstring("Method GetViewForAppUserModelId")],
            ctypes.HRESULT,
            "GetViewForAppUserModelId",
            (["in"], ctypes.wintypes.LPCWSTR, "id"),
            (["out"], ctypes.POINTER(ctypes.POINTER(IApplicationView)), "view"),
        ),
        COMMETHOD(
            [helpstring("Method GetViewInFocus")],
            ctypes.HRESULT,
            "GetViewInFocus",
            (["out"], ctypes.POINTER(ctypes.POINTER(IApplicationView)), "view"),
        ),
        COMMETHOD(
            [helpstring("Method Unknown1")],
            ctypes.HRESULT,
            "Unknown1",
            (["out"], ctypes.POINTER(ctypes.POINTER(IApplicationView)), "view"),
        ),
        COMMETHOD(
            [helpstring("Method RefreshCollection")],
            ctypes.HRESULT,
            "RefreshCollection",
        ),
        COMMETHOD(
            [helpstring("Method RegisterForApplicationViewChanges")],
            ctypes.HRESULT,
            "RegisterForApplicationViewChanges",
            (["in"], ctypes.POINTER(ctypes.wintypes.UINT), "listener"),
            (["out"], ctypes.POINTER(ctypes.wintypes.DWORD), "cookie"),
        ),
        COMMETHOD(
            [helpstring("Method UnregisterForApplicationViewChanges")],
            ctypes.HRESULT,
            "UnregisterForApplicationViewChanges",
            (["in"], ctypes.wintypes.DWORD, "cookie"),
        ),
    ]


class IVirtualDesktop(comtypes.IUnknown):
    """Class defining virtual desktop instance accessible through its pointer."""

    _case_insensitive_ = True
    _iid_ = IID_IVirtualDesktop
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method IsViewVisible")],
            ctypes.HRESULT,
            "IsViewVisible",
            (["out"], ctypes.POINTER(IApplicationView), "pView"),
            (["out"], ctypes.POINTER(ctypes.wintypes.INT), "pfVisible"),
        ),
        COMMETHOD(
            [helpstring("Method GetID")],
            ctypes.HRESULT,
            "GetID",
            (["out"], ctypes.POINTER(GUID), "pGuid"),
        ),
    ]


class IVirtualDesktopManager(comtypes.IUnknown):
    """Interface to publicly documented methods dealing with virtual dektops."""

    _case_insensitive_ = True
    _iid_ = IID_IVirtualDesktopManager
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method IsWindowOnCurrentVirtualDesktop")],
            ctypes.HRESULT,
            "IsWindowOnCurrentVirtualDesktop",
            (["in"], ctypes.wintypes.HWND, "topLevelWindow"),
            (["out"], ctypes.POINTER(ctypes.wintypes.BOOL), "onCurrentDesktop"),
        ),
        COMMETHOD(
            [helpstring("Method GetWindowDesktopId")],
            ctypes.HRESULT,
            "GetWindowDesktopId",
            (["in"], ctypes.wintypes.HWND, "topLevelWindow"),
            (["out"], ctypes.POINTER(GUID), "desktopId"),
        ),
        COMMETHOD(
            [helpstring("Method MoveWindowToDesktop")],
            ctypes.HRESULT,
            "MoveWindowToDesktop",
            (["in"], ctypes.wintypes.HWND, "topLevelWindow"),
            (["in"], ctypes.POINTER(GUID), "desktopId"),
        ),
    ]


class IVirtualDesktopManagerInternal(comtypes.IUnknown):
    """Interface to methods dealing with virtual dektops documented by community."""

    _case_insensitive_ = True
    _iid_ = IID_IVirtualDesktopManagerInternal
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method GetCount")],
            ctypes.HRESULT,
            "GetCount",
            (["in"], ctypes.POINTER(ctypes.wintypes.UINT), "pCount"),
        ),
        COMMETHOD(
            [helpstring("Method MoveViewToDesktop")],
            ctypes.HRESULT,
            "MoveViewToDesktop",
            (["in"], ctypes.POINTER(IApplicationView), "pView"),
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktop"),
        ),
        COMMETHOD(
            [helpstring("Method CanViewMoveDesktops")],
            ctypes.HRESULT,
            "CanViewMoveDesktops",
            (["out"], ctypes.POINTER(IApplicationView), "pView"),
            (["out"], ctypes.POINTER(ctypes.wintypes.INT), "pfCanViewMoveDesktops"),
        ),
        COMMETHOD(
            [helpstring("Method GetCurrentDesktop")],
            ctypes.HRESULT,
            "GetCurrentDesktop",
            (["out"], ctypes.POINTER(ctypes.POINTER(IVirtualDesktop)), "desktop"),
        ),
        COMMETHOD(
            [helpstring("Method GetDesktops")],
            ctypes.HRESULT,
            "GetDesktops",
            (["out"], ctypes.POINTER(ctypes.POINTER(IObjectArray)), "ppDesktops"),
        ),
        COMMETHOD(
            [helpstring("Method GetAdjacentDesktop")],
            ctypes.HRESULT,
            "GetAdjacentDesktop",
            (["out"], ctypes.POINTER(IVirtualDesktop), "pDesktopReference"),
            (["in"], AdjacentDesktop, "uDirection"),
            (
                ["out"],
                ctypes.POINTER(ctypes.POINTER(IVirtualDesktop)),
                "ppAdjacentDesktop",
            ),
        ),
        COMMETHOD(
            [helpstring("Method SwitchDesktop")],
            ctypes.HRESULT,
            "SwitchDesktop",
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktop"),
        ),
        COMMETHOD(
            [helpstring("Method CreateDesktopW")],
            ctypes.HRESULT,
            "CreateDesktopW",
            (["out"], ctypes.POINTER(ctypes.POINTER(IVirtualDesktop)), "ppNewDesktop"),
        ),
        COMMETHOD(
            [helpstring("Method RemoveDesktop")],
            ctypes.HRESULT,
            "RemoveDesktop",
            (["in"], ctypes.POINTER(IVirtualDesktop), "pRemove"),
            (["in"], ctypes.POINTER(IVirtualDesktop), "pFallbackDesktop"),
        ),
        COMMETHOD(
            [helpstring("Method FindDesktop")],
            ctypes.HRESULT,
            "FindDesktop",
            (["in"], ctypes.POINTER(GUID), "desktopId"),
            (["out"], ctypes.POINTER(ctypes.POINTER(IVirtualDesktop)), "ppDesktop"),
        ),
    ]


## CUSTOM API
class VirtualDesktopsWin10:
    """Helper class for calls to Windows 10 virtual desktop interfaces.

    IVirtualDesktopManager is an interface publicly documented by Microsoft,
    whilst IVirtualDesktopManagerInternal is documented by community.

    :var manager: interface to publicly available API for virtual desktops
    :type manager: pointer to :class:`IVirtualDesktopManager`
    :var internal_manager: interface to internal API for virtual desktops
    :type internal_manager: pointer to :class:`IVirtualDesktopManagerInternal`
    :var view_collection: interface to application views collection
    :type view_collection: pointer to :class:`IApplicationViewCollection`
    :var desktops: collection of virtual desktops ordinals and uids
    :type desktops: list of (int, :class:`GUID`)
    """

    manager = None
    internal_manager = None
    view_collection = None
    desktops = None

    def __init__(self):
        """Calls method dealing with managers preparing and setup."""
        self._setup()

    ## CONFIGURATION
    def _setup(self):
        """Initializes the COM library on the current thread and sets managers."""
        comtypes.CoInitialize()
        self.manager = self._get_manager()
        service_provider = self._get_service_provider()
        self.internal_manager = self._get_internal_manager(service_provider)
        self.view_collection = self._get_view_collection(service_provider)

    ## PRIVATE API
    def _get_desktop_id_from_array(self, array, index):
        """Returns uid instance of virtual desktop at ``index`` position in ``array``.

        :param array: array holding pointers to virtual desktops instances
        :type array: pointer to :class:`IObjectArray`
        :param index: desktop position in array
        :type index: int
        :var desktop: virtual desktop instance
        :type desktop: pointer to :class:`IVirtualDesktop`
        :returns: :class:`GUID`
        """
        desktop = ctypes.POINTER(IVirtualDesktop)()
        array.GetAt(index, IID_IVirtualDesktop, ctypes.byref(desktop))
        return desktop.GetID()

    def _get_desktop_id_from_ordinal(self, desktop_ordinal):
        """Returns desktop uid instance for provided desktop ordinal.

        :param desktop_ordinal: virtual desktop ordinal in desktops collection
        :type desktop_ordinal: int
        :returns::class:`GUID`
        """
        return self.get_desktops()[desktop_ordinal][1]

    def _get_desktops(self):
        """Returns collection of two-tuples representing available virtual desktops.

        :var array: array holding pointers to virtual desktops instances
        :type array: pointer to :class:`IObjectArray`
        :var count: number of desktops in array
        :type count: int
        :returns: list of (int,:class:`GUID`)
        """
        array = self.internal_manager.GetDesktops()
        count = array.GetCount()
        return [(i, self._get_desktop_id_from_array(array, i)) for i in range(count)]

    def _get_internal_manager(self, service_provider):
        """Instantiates and returns pointer to interface documented by community.

        :returns: pointer to :class:`IVirtualDesktopManagerInternal`
        """
        return comtypes.cast(
            service_provider.QueryService(
                CLSID_VirtualDesktopManagerInternal, IID_IVirtualDesktopManagerInternal
            ),
            ctypes.POINTER(IVirtualDesktopManagerInternal),
        )

    def _get_manager(self):
        """Instantiates and returns pointer to interface documented by Microsoft.

        :returns: pointer to :class:`IVirtualDesktopManager`
        """
        return comtypes.CoCreateInstance(
            CLSID_VirtualDesktopManager, IVirtualDesktopManager
        )

    def _get_service_provider(self):
        """Instantiates and returns pointer to service provider.

        :returns: pointer to :class:`IServiceProvider`
        """
        return comtypes.CoCreateInstance(
            CLSID_ImmersiveShell, IServiceProvider, comtypes.CLSCTX_LOCAL_SERVER
        )

    def _get_view_collection(self, service_provider):
        """Instantiates and returns pointer to application view collection interface.

        :returns: pointer to :class:`IApplicationViewCollection`
        """
        return comtypes.cast(
            service_provider.QueryService(
                IID_IApplicationViewCollection, IID_IApplicationViewCollection
            ),
            ctypes.POINTER(IApplicationViewCollection),
        )

    ## PUBLIC API
    def get_desktops(self, refresh=False):
        """Returns virtual desktops collection available in the system.

        Retrieves and sets instance attribute holding collection if it hasn't been
        set yet or if True value is provided as ``refresh`` argument.

        :param refresh: value indicating if desktop collection should be refreshed
        :type refresh: Boolean
        :returns: list of (int, :class:`GUID`)
        """
        if self.desktops is None or refresh:
            self.desktops = self._get_desktops()

        return self.desktops

    def get_window_desktop(self, hwnd, refresh=False):
        """Returns virtual desktop where window with provided ``hwnd`` is placed.

        :param hwnd: window handle
        :type hwnd: int
        :param refresh: value indicating if desktop collection should be refreshed
        :type refresh: Boolean
        :var desktop_id: virtual desktop's uid representation
        :type desktop_id: :class:`GUID`
        :returns: (int, :class:`GUID`)
        """
        desktop_id = self.manager.GetWindowDesktopId(hwnd)

        return next(
            (
                desktop
                for desktop in self.get_desktops(refresh)
                if desktop[1] == desktop_id
            ),
            (0, None),
        )

    def is_window_in_current_desktop(self, hwnd):
        """Checks if window with provided ``hwnd`` is placed in current desktop.

        :param hwnd: window handle
        :type hwnd: int
        :returns: Boolean
        """
        return self.manager.IsWindowOnCurrentVirtualDesktop(hwnd)

    def move_other_window_to_desktop(self, hwnd, desktop_ordinal):
        """Moves other process' window with provided ``hwnd`` to the other desktop

        identified by ``desktop_ordinal``.

        :param hwnd: window handle
        :type hwnd: int
        :param desktop_ordinal: virtual desktop ordinal in desktops collection
        :type desktop_ordinal: int
        :var desktop_id: virtual desktop's uid representation
        :type desktop_id: :class:`GUID`
        :var desktop: virtual desktop instance
        :type desktop: pointer to :class:`IVirtualDesktop`
        :var app_view: interface to application view
        :type app_view: pointer to :class:`IApplicationView`
        :returns: False on success, None on failure
        """
        desktop_id = self._get_desktop_id_from_ordinal(desktop_ordinal)
        desktop = self.internal_manager.FindDesktop(ctypes.byref(desktop_id))
        app_view = self.view_collection.GetViewForHwnd(hwnd)
        ret_val = self.internal_manager.MoveViewToDesktop(app_view, desktop)
        if ret_val != S_OK:
            return None

        return False

    def move_own_window_to_desktop(self, hwnd, desktop_ordinal):
        """Moves root window with provided ``hwnd`` to the desktop with provided ordinal.

        :param hwnd: window handle
        :type hwnd: int
        :param desktop_ordinal: virtual desktop ordinal in desktops collection
        :type desktop_ordinal: int
        :var desktop_id: virtual desktop's uid representation
        :type desktop_id: :class:`GUID`
        :var desktop: virtual desktop instance
        :type desktop: pointer to :class:`IVirtualDesktop`
        :returns: False on success, None on failure
        """
        desktop_id = self._get_desktop_id_from_ordinal(desktop_ordinal)
        ret_val = self.manager.MoveWindowToDesktop(hwnd, ctypes.byref(desktop_id))
        if ret_val != S_OK:
            return None

        desktop = self.internal_manager.FindDesktop(ctypes.byref(desktop_id))
        ret_val = self.internal_manager.SwitchDesktop(desktop)
        if ret_val != S_OK:
            return None

        return False
