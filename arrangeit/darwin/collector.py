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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import io

from PIL import Image

from AppKit import NSApplicationActivationPolicyRegular, NSScreen, NSWorkspace
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGNullWindowID,
    kCGWindowListExcludeDesktopElements,
)

from arrangeit.base import BaseCollector
from arrangeit.data import WindowModel


class Collector(BaseCollector):
    """Collecting windows class with Mac OS specific code."""

    def _get_application_icon(self, win):
        """Returns icon of the provided app.

        TODO implement

        :param win: window object
        :type win: dict
        """
        app = self._running_apps_ids()[win.valueForKey_("kCGWindowOwnerPID")]
        return Image.open(io.BytesIO(app.icon().TIFFRepresentation()))

    def get_application_name(self, win):
        """Returns application/owner name for the provided win.

        :param win: window object
        :type win: dict
        :returns: str
        """
        return win.valueForKey_("kCGWindowOwnerName")

    def _get_window_geometry(self, win):
        """Returns window geometry for the provided win.

        Window geometry is represented with tuple (x, y, width, height)

        :param win: window object
        :type win: dict
        :returns: (int, int, int, int)
        """
        bounds = win.valueForKey_("kCGWindowBounds")
        return (
            int(bounds.valueForKey_("X")),
            int(bounds.valueForKey_("Y")),
            int(bounds.valueForKey_("Width")),
            int(bounds.valueForKey_("Height")),
        )

    def _get_window_id(self, win):
        """Returns ID of the provided win.

        :param win: window object
        :type win: dict
        :returns: int
        """
        return win.valueForKey_("kCGWindowNumber")

    def _get_window_title(self, win):
        """Returns title/caption of the provided win.

        :param win: window object
        :type win: dict
        :returns: str
        """
        return win.valueForKey_("kCGWindowName")

    def _running_apps_ids(self):
        """Returns dictionary of all app ids and instances for running applications.

        :returns: dict {int: :class:`NSRunningApplication`}
        """
        return {
            app.processIdentifier(): app
            for app in NSWorkspace.sharedWorkspace().runningApplications()
            if app.activationPolicy() == NSApplicationActivationPolicyRegular
        }

    def add_window(self, win):
        """Creates WindowModel instance from provided win and adds it to collection.

        :param win: window object
        :type win: dict
        """
        self.collection.add(
            WindowModel(
                wid=self._get_window_id(win),
                rect=self._get_window_geometry(win),
                resizable=self.is_resizable(win),
                title=self._get_window_title(win),
                name=self.get_application_name(win),
                icon=self._get_application_icon(win),
                workspace=self.get_workspace_number_for_window(win),
            )
        )

    def check_window(self, win):
        """Checks does window qualify to be collected

        by checking window type applicability with :func:`is_applicable`
        and its current state validity with :func:`is_valid_state`.

        :param win: window object
        :type win: dict
        :returns: Boolean
        """
        if not self.is_applicable(win):
            return False

        if not self.is_valid_state(win):
            return False

        return True

    def get_available_workspaces(self):
        """

        TODO implement

        :returns: list
        """
        return [(0, "")]

    def get_monitors_rects(self):
        """Returns list of available monitors position and size rectangles.

        :returns: list [(x,y,w,h)]
        """
        return [
            (
                int(screen.frame().origin.x),
                int(screen.frame().origin.y),
                int(screen.frame().size.width),
                int(screen.frame().size.height),
            )
            for screen in NSScreen.screens()
        ]

    def get_windows(self):
        """Returns list of all windows as dictionary objects

        :returns: list
        """
        return [
            win
            for win in CGWindowListCopyWindowInfo(
                kCGWindowListExcludeDesktopElements, kCGNullWindowID
            )
        ]

    def get_workspace_number_for_window(self, win):
        """TODO implement

        :param win: window object
        :type win: dict
        :returns: str
        """
        return 0

    def is_applicable(self, win):
        """Checks if provided win represents window that should be collected.

        TODO implement

        :param win: window object
        :type win: dict
        :returns: Boolean
        """
        if not win.valueForKey_("kCGWindowOwnerPID") in self._running_apps_ids():
            return False

        if win.valueForKey_("kCGWindowName") in (None, ""):
            return False

        return True

    def is_resizable(self, win):
        """

        TODO implement

        :param win: window object
        :type win: dict
        :returns: Boolean
        """
        return True

    def is_restored(self, win):
        """

        TODO implement

        :param win: window object
        :type win: dict
        :returns: Boolean
        """
        return True

    def is_valid_state(self, win):
        """Checks if provided win is window with valid state for collecting.

        TODO implement

        :param win: window object
        :type win: dict
        :returns: Boolean
        """

        return True
