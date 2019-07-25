# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2019 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

u"""
    Name: VirtualDesktopsWin10
    Author: Kgschlosser
    Version: 0.1
    Description: Creates events based on Virtual desktop interactions.
    GUID: {5DFFBD61-7582-4D6F-8EA9-9CB36284C9CF}
    URL: http://eventghost.net/forum/viewtopic.php?f=10&p=53389#p53389
"""
# import eg

# eg.RegisterPlugin(
#     name = "Virtual Desktops",
#     author = "Kgschlosser",
#     version = "0.0.004",
#     guid = "{C2F03A33-21F5-47FA-B4BB-156362A2F239}",
#     canMultiLoad = False,
#     url = "http://eventghost.net/forum/viewtopic.php?f=10&p=53389#p53389",
#     description = "Creates events based on Virtual desktop interactions.",

# )


# from ctypes.wintypes import HRESULT, HWND, BOOL, POINTER, DWORD, INT, UINT, LPVOID, ULONG

import comtypes
import ctypes
import ctypes.wintypes
from comtypes import helpstring, COMMETHOD
from comtypes.GUID import GUID

REFGUID = ctypes.POINTER(GUID)
REFIID = REFGUID
ENUM = ctypes.wintypes.INT
IID = GUID
INT32 = ctypes.c_int32
INT64 = ctypes.c_int64

S_OK = 0x00000000

CLSID_ImmersiveShell = GUID("{C2F03A33-21F5-47FA-B4BB-156362A2F239}")

CLSID_IVirtualNotificationService = GUID("{A501FDEC-4A09-464C-AE4E-1B9C21B84918}")


class HSTRING__(ctypes.Structure):
    _fields_ = [("unused", ctypes.wintypes.INT)]


HSTRING = ctypes.POINTER(HSTRING__)


class EventRegistrationToken(ctypes.Structure):
    _fields_ = [("value", INT64)]


class AdjacentDesktop(ENUM):
    LeftDirection = 3
    RightDirection = 4


class ApplicationViewOrientation(ENUM):
    ApplicationViewOrientation_Landscape = 0
    ApplicationViewOrientation_Portrait = 1


class TrustLevel(ENUM):
    BaseTrust = 0
    PartialTrust = BaseTrust + 1
    FullTrust = PartialTrust + 1


IID_IInspectable = GUID("{AF86E2E0-B12D-4C6A-9C5A-D7AA65101E90}")


class IInspectable(comtypes.IUnknown):
    _case_insensitive_ = True
    _idlflags_ = []
    _iid_ = IID_IInspectable
    _methods_ = [
        COMMETHOD(
            [helpstring("Method GetIids")],
            ctypes.HRESULT,
            "GetIids",
            (["out"], ctypes.POINTER(ctypes.wintypes.ULONG), "iidCount"),
            (["out"], ctypes.POINTER(ctypes.POINTER(IID)), "iids"),
        ),
        COMMETHOD(
            [helpstring("Method GetRuntimeClassName")],
            ctypes.HRESULT,
            "GetRuntimeClassName",
            (["out"], ctypes.POINTER(HSTRING), "className"),
        ),
        COMMETHOD(
            [helpstring("Method GetTrustLevel")],
            ctypes.HRESULT,
            "GetTrustLevel",
            (["out"], ctypes.POINTER(TrustLevel), "trustLevel"),
        ),
    ]


IID_IApplicationViewConsolidatedEventArgs = GUID(
    "{514449EC-7EA2-4DE7-A6A6-7DFBAAEBB6FB}"
)


class IApplicationViewConsolidatedEventArgs(IInspectable):
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


IID_IApplicationView = GUID("{D222D519-4361-451E-96C4-60F4F9742DB0}")


class IApplicationView(IInspectable):
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
            (["in"], HSTRING, "value"),
        ),
        COMMETHOD(
            [helpstring("Method get_Title")],
            ctypes.HRESULT,
            "get_Title",
            (["retval", "out"], ctypes.POINTER(HSTRING), "value"),
        ),
        COMMETHOD(
            [helpstring("Method get_Id")],
            ctypes.HRESULT,
            "get_Id",
            (["retval", "out"], ctypes.POINTER(INT32), "value"),
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


IID_IServiceProvider = GUID("{6D5140C1-7436-11CE-8034-00AA006009FA}")


class IServiceProvider(comtypes.IUnknown):
    _case_insensitive_ = True
    _idlflags_ = []
    _iid_ = IID_IServiceProvider
    _methods_ = [
        COMMETHOD(
            [helpstring("Method QueryService"), "local", "in"],
            ctypes.HRESULT,
            "QueryService",
            (["in"], REFGUID, "guidService"),
            (["in"], REFIID, "riid"),
            (["out"], ctypes.POINTER(ctypes.wintypes.LPVOID), "ppvObject"),
        )
    ]


IID_IObjectArray = GUID("{92CA9DCD-5622-4BBA-A805-5E9F541BD8C9}")


class IObjectArray(comtypes.IUnknown):
    """
    Unknown Object Array
    """

    _case_insensitive_ = True
    _idlflags_ = []
    _iid_ = None

    _methods_ = [
        COMMETHOD(
            [helpstring("Method GetCount")],
            ctypes.HRESULT,
            "GetCount",
            (["in"], ctypes.POINTER(ctypes.wintypes.UINT), "pcObjects"),
        ),
        COMMETHOD(
            [helpstring("Method GetAt")],
            ctypes.HRESULT,
            "GetAt",
            (["in"], ctypes.wintypes.UINT, "uiIndex"),
            (["in"], REFIID, "riid"),
            (["in", "iid_is"], ctypes.POINTER(ctypes.wintypes.LPVOID), "ppv"),
        ),
    ]


IID_IVirtualDesktop = GUID("{FF72FFDD-BE7E-43FC-9C03-AD81681E88E4}")


class IVirtualDesktop(comtypes.IUnknown):
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
            (["in"], ctypes.POINTER(GUID), "pGuid"),
        ),
    ]


CLSID_VirtualDesktopManager = GUID("{AA509086-5CA9-4C25-8F95-589D3C07B48A}")
IID_IVirtualDesktopManager = GUID("{A5CD92FF-29BE-454C-8D04-D82879FB3F1B}")


class IVirtualDesktopManager(comtypes.IUnknown):
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
            (["in"], ctypes.POINTER(GUID), "desktopId"),
        ),
        COMMETHOD(
            [helpstring("Method MoveWindowToDesktop")],
            ctypes.HRESULT,
            "MoveWindowToDesktop",
            (["in"], ctypes.wintypes.HWND, "topLevelWindow"),
            (["in"], REFGUID, "desktopId"),
        ),
    ]


CLSID_VirtualDesktopManagerInternal = GUID("{C5E0CDCA-7B6E-41B2-9FC4-D93975CC467B}")

IID_IVirtualDesktopManagerInternal = GUID("{F31574D6-B682-4CDC-BD56-1827860ABEC6}")


# IID_IVirtualDesktopManagerInternal = GUID(
#     '{AF8DA486-95BB-4460-B3B7-6E7A6B2962B5}'
# )

# IID_IVirtualDesktopManagerInternal = GUID(
#     '{EF9F1A6C-D3CC-4358-B712-F84B635BEBE7}'
# )


class IVirtualDesktopManagerInternal(comtypes.IUnknown):
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
            (["out"], ctypes.POINTER(IApplicationView), "pView"),
            (["out"], ctypes.POINTER(IVirtualDesktop), "pDesktop"),
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
            (["in"], ctypes.POINTER(ctypes.POINTER(IObjectArray)), "ppDesktops"),
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
            # ctypes.c_void_p,
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


IID_IVirtualDesktopNotification = GUID("{C179334C-4295-40D3-BEA1-C654D965605A}")


class IVirtualDesktopNotification(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IVirtualDesktopNotification
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method VirtualDesktopCreated")],
            ctypes.HRESULT,
            "VirtualDesktopCreated",
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktop"),
        ),
        COMMETHOD(
            [helpstring("Method VirtualDesktopDestroyBegin")],
            ctypes.HRESULT,
            "VirtualDesktopDestroyBegin",
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktopDestroyed"),
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktopFallback"),
        ),
        COMMETHOD(
            [helpstring("Method VirtualDesktopDestroyFailed")],
            ctypes.HRESULT,
            "VirtualDesktopDestroyFailed",
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktopDestroyed"),
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktopFallback"),
        ),
        COMMETHOD(
            [helpstring("Method VirtualDesktopDestroyed")],
            ctypes.HRESULT,
            "VirtualDesktopDestroyed",
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktopDestroyed"),
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktopFallback"),
        ),
        COMMETHOD(
            [helpstring("Method ViewVirtualDesktopChanged")],
            ctypes.HRESULT,
            "ViewVirtualDesktopChanged",
            (["in"], ctypes.POINTER(IApplicationView), "pView"),
        ),
        COMMETHOD(
            [helpstring("Method CurrentVirtualDesktopChanged")],
            ctypes.HRESULT,
            "CurrentVirtualDesktopChanged",
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktopOld"),
            (["in"], ctypes.POINTER(IVirtualDesktop), "pDesktopNew"),
        ),
    ]


IID_IVirtualDesktopNotificationService = GUID("{0CD45E71-D927-4F15-8B0A-8FEF525337BF}")


class IVirtualDesktopNotificationService(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IVirtualDesktopNotificationService
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method Register")],
            ctypes.HRESULT,
            "Register",
            (["in"], ctypes.POINTER(IVirtualDesktopNotification), "pNotification"),
            (["out"], ctypes.POINTER(ctypes.wintypes.DWORD), "pdwCookie"),
        ),
        COMMETHOD(
            [helpstring("Method Unregister")],
            ctypes.HRESULT,
            "Unregister",
            (["in"], ctypes.wintypes.DWORD, "dwCookie"),
        ),
    ]


class VirtualDesktopsWin10(object):
    """Helper class for calls to Windows 10 virtual desktop interfaces.

    IVirtualDesktopManager is an interface publicly documented by Microsofr,
    whilst IVirtualDesktopManagerInternal is documented by community.

    :var manager: interface to publicly available API for virtual desktops
    :type manager: pointer to :class:`IVirtualDesktopManager`
    :var internal_manager: interface to internal API for virtual desktops
    :type internal_manager: pointer to :class:`IVirtualDesktopManagerInternal`
    :var desktops: collection of virtual desktops ordinals and uids
    :type desktops: list of (int, :class:`GUID`)
    """

    manager = None
    internal_manager = None
    desktops = None

    def __init__(self):
        """Calls method dealing with managers preparing and setup."""
        self._setup()

    ## CONFIGURATION
    def _setup(self):
        """Initializes the COM library on the current thread and sets managers."""
        comtypes.CoInitialize()
        self.manager = self._get_manager()
        self.internal_manager = self._get_internal_manager(self._get_service_provider())

    ## PRIVATE API
    def _get_desktop_id_from_array(self, array, index):
        """Returns uid instance of virtual desktop at ``index`` position in ``array``.

        :param array: array holding pointers to virtual desktops instances
        :type array: pointer to :class:`IObjectArray`
        :param index: desktop position in array
        :type index: int
        :var desktop: virtual desktop instance
        :type desktop: pointer to :class:`IVirtualDesktop`
        :var desktop_id: virtual desktop's uid representation
        :type desktop_id: :class:`GUID`
        :returns: :class:`GUID`
        """
        desktop = ctypes.POINTER(IVirtualDesktop)()
        array.GetAt(index, IID_IVirtualDesktop, ctypes.byref(desktop))
        desktop_id = GUID()
        desktop.GetID(ctypes.byref(desktop_id))
        return desktop_id

    def _get_desktops(self):
        """Returns collection of two-tuples representing available virtual desktops.

        :var array: array holding pointers to virtual desktops instances
        :type array: pointer to :class:`IObjectArray`
        :var count: number of desktops in array
        :type count: :class:`ctypes.wintypes.UINT`
        :returns: list of (int,:class:`GUID`)
        """
        array = ctypes.POINTER(IObjectArray)()

        ret_val = self.internal_manager.GetDesktops(ctypes.byref(array))
        if ret_val != S_OK:
            return None

        count = ctypes.wintypes.UINT()
        array.GetCount(ctypes.byref(count))

        return [
            (i, self._get_desktop_id_from_array(array, i)) for i in range(count.value)
        ]

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

    ## PUBLIC API
    def get_desktops(self, refresh=False):
        """Returns virtual desktops collection avaialable in the system.

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
        desktop_id = GUID()
        ret_val = self.manager.GetWindowDesktopId(hwnd, ctypes.byref(desktop_id))
        if ret_val != S_OK:
            return None

        return next(
            (
                desktop
                for desktop in self.get_desktops(refresh)
                if desktop[1] == desktop_id
            ),
            None,
        )

    def move_window_to_desktop(self, hwnd, desktop_ordinal):
        """Returns virtual desktop in which window with provided ``hwnd`` is placed.

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
        desktop_id = self.desktops[desktop_ordinal][1]
        ret_val = self.manager.MoveWindowToDesktop(hwnd, ctypes.byref(desktop_id))
        if ret_val != S_OK:
            return None

        desktop = ctypes.POINTER(IVirtualDesktop)()
        self.internal_manager.SwitchDesktop(ctypes.byref(desktop))

        return False
