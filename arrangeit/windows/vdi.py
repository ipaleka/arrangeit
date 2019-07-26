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
Code from this module is influenced by the code from Virtual_Desktops_Plugin
<https://github.com/DanEdens/Virtual_Desktops_Plugin> authored by Kgschlosser.
That code was shipped with the following copyright notice:

 This file is a plugin for EventGhost.
 Copyright © 2005-2019 EventGhost Project <http://www.eventghost.net/>

 EventGhost is free software: you can redistribute it and/or modify it under
 the terms of the GNU General Public License as published by the Free
 Software Foundation, either version 2 of the License, or (at your option)
 any later version.

 EventGhost is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 more details.

 You should have received a copy of the GNU General Public License along
 with EventGhost. If not, see <http://www.gnu.org/licenses/>.
"""

import ctypes
import ctypes.wintypes

import comtypes
from comtypes import COMMETHOD, helpstring
from comtypes.GUID import GUID

S_OK = 0x00000000

CLSID_ImmersiveShell = GUID("{C2F03A33-21F5-47FA-B4BB-156362A2F239}")
CLSID_VirtualDesktopManager = GUID("{AA509086-5CA9-4C25-8F95-589D3C07B48A}")
CLSID_VirtualDesktopManagerInternal = GUID("{C5E0CDCA-7B6E-41B2-9FC4-D93975CC467B}")

IID_IServiceProvider = GUID("{6D5140C1-7436-11CE-8034-00AA006009FA}")
IID_IVirtualDesktop = GUID("{FF72FFDD-BE7E-43FC-9C03-AD81681E88E4}")
IID_IVirtualDesktopManager = GUID("{A5CD92FF-29BE-454C-8D04-D82879FB3F1B}")
IID_IVirtualDesktopManagerInternal = GUID("{F31574D6-B682-4CDC-BD56-1827860ABEC6}")


class AdjacentDesktop(ctypes.wintypes.INT):
    LeftDirection = 3
    RightDirection = 4


class IServiceProvider(comtypes.IUnknown):
    _case_insensitive_ = True
    _idlflags_ = []
    _iid_ = IID_IServiceProvider
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
            (["in"], ctypes.POINTER(GUID), "riid"),
            (["in", "iid_is"], ctypes.POINTER(ctypes.wintypes.LPVOID), "ppv"),
        ),
    ]


class IVirtualDesktop(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IVirtualDesktop
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [helpstring("Method IsViewVisible")],
            ctypes.HRESULT,
            "IsViewVisible",
            (["out"], ctypes.POINTER(comtypes.IUnknown), "pView"),
            (["out"], ctypes.POINTER(ctypes.wintypes.INT), "pfVisible"),
        ),
        COMMETHOD(
            [helpstring("Method GetID")],
            ctypes.HRESULT,
            "GetID",
            (["in"], ctypes.POINTER(GUID), "pGuid"),
        ),
    ]


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
            (["in"], ctypes.POINTER(GUID), "desktopId"),
        ),
    ]


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
            (["out"], ctypes.POINTER(comtypes.IUnknown), "pView"),
            (["out"], ctypes.POINTER(IVirtualDesktop), "pDesktop"),
        ),
        COMMETHOD(
            [helpstring("Method CanViewMoveDesktops")],
            ctypes.HRESULT,
            "CanViewMoveDesktops",
            (["out"], ctypes.POINTER(comtypes.IUnknown), "pView"),
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

        # desktop = ctypes.POINTER(IVirtualDesktop)()
        # self.internal_manager.SwitchDesktop(ctypes.byref(desktop))

        return False
