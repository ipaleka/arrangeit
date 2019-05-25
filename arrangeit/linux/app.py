import gi
import subprocess
import time

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck
from Xlib import X

from arrangeit.base import BaseApp


class App(BaseApp):
    """Main app class with GNU/Linux specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move_and_resize(self, wid):
        """Moves and resizes window having provided wid.

        Gravity stays the same (Wnck.WindowGravity.CURRENT) and the other arguments
        are calculated/retrieved from model where `changed` attribute holds needed data.

        :var model: window data
        :type model: :class:`WindowModel` instance
        :var mask: combination of bits holding information what is changed
        :type mask: :class:`Wnck.WindowMoveResizeMask` flag
        :var win: window instance
        :type win: :class:`Wnck.Window` object
        """
        model = self.collector.collection.get_model_by_wid(wid)
        mask = self.collector.get_window_move_resize_mask(model)
        win = self.collector.get_window_by_wid(wid)
        return win.set_geometry(Wnck.WindowGravity.CURRENT, mask, *model.changed)

    def move(self, wid):
        """Just calls `move_and_resize` as the same method moves and resizes

        in Wnck.Window class under GNU/Linux.
        """
        return self.move_and_resize(wid)

    def activate_workspace(self, number, return_workspace=False):
        """Activates workspace identified by provided our custom workspace number."""
        workspace = self.collector.get_wnck_workspace_for_custom_number(number)
        if workspace:
            workspace.activate(X.CurrentTime)
            return workspace if return_workspace else False
        return True

    def move_to_workspace(self, wid, number):
        """Move active window to provided custom workspace number."""
        Wnck.shutdown()
        workspace = self.activate_workspace(number, return_workspace=True)
        if workspace:
            # FIXME nasty hack wid+1
            win = self.collector.get_window_by_wid(wid+1)
            win.move_to_workspace(workspace)
            # TODO X.CurrentTime/0 activates with a warning
            win.activate(X.CurrentTime)
            return False
        return True
