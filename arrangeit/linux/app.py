import gi

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck
from PIL import Image, ImageTk
from Xlib import display, X

from arrangeit.base import BaseApp


class App(BaseApp):
    """Main app class with GNU/Linux specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def grab_window_screen(self, model):
        """Grabs and returns screenshot of the window from provided model.

        :param model: model of the window we want screenshot form
        :type model: :class:`WindowModel`
        :returns: :class:`PIL.ImageTk.PhotoImage`
        """
        root = display.Display().screen().root
        raw = root.get_image(model.x, model.y, model.w, model.h, X.ZPixmap, 0xFFFFFFFF)
        image = Image.frombytes("RGB", (model.w, model.h), raw.data, "raw", "BGRX")
        return ImageTk.PhotoImage(image)

    def move_and_resize(self, wid):
        """Moves and resizes window having provided wid.

        Gravity stays the same (Wnck.WindowGravity.CURRENT) and the other arguments
        are calculated/retrieved from model where `changed` attribute holds needed data.

        If returned `mask` is False then wee don't need to do anything more.

        :param wid: windows id
        :type wid: int
        :var model: window data
        :type model: :class:`WindowModel` instance
        :var mask: combination of bits holding information what is changed
        :type mask: :class:`Wnck.WindowMoveResizeMask` flag
        :var win: window instance
        :type win: :class:`Wnck.Window` object
        :returns: Boolean
        """
        model = self.collector.collection.get_model_by_wid(wid)
        if model.is_ws_changed:
            self._move_window_to_workspace(wid, model.changed_ws)
        mask = self.collector.get_window_move_resize_mask(model)
        if mask:
            win = self.collector.get_window_by_wid(wid)
            win.set_geometry(Wnck.WindowGravity.STATIC, mask, *model.changed)
            return False
        return True

    def move(self, wid):
        """Just calls `move_and_resize` as the same method moves and resizes

        in Wnck.Window class under GNU/Linux.

        :param wid: windows id
        :type wid: int
        """
        return self.move_and_resize(wid)

    def _activate_workspace(self, number):
        """Activates workspace identified by provided our custom workspace number.

        :param number: our custom workspace number
        :type number: int
        :var workspace: workspace to move to
        :type workspace: :class:`Wnck.Workspace`
        :returns: :class:`Wnck.Workspace`
        """
        workspace = self.collector.get_wnck_workspace_for_custom_number(number)
        if workspace:
            workspace.activate(X.CurrentTime)
            return workspace
        return True

    def _move_window_to_workspace(self, wid, number):
        """Moves window with provided wid to provided custom workspace number.

        It shutdowns Wnck in beginning as this is the only method that uses Wnck
        after initial windows collecting - without shutdown wid is not recognized.

        :param wid: windows id
        :type wid: int
        :param number: our custom workspace number
        :type number: int
        :var workspace: workspace to move to
        :type workspace: :class:`Wnck.Workspace`
        :var win: window instance
        :type win: :class:`Wnck.Window`
        :returns: Boolean
        """
        Wnck.shutdown()
        workspace = self._activate_workspace(number)
        if workspace:
            win = self.collector.get_window_by_wid(wid)
            win.move_to_workspace(workspace)
            # TODO X.CurrentTime/0 activates with a warning
            win.activate(X.CurrentTime)
            return False
        return True

    def move_to_workspace(self, wid, number):
        """Moves root window to provided custom workspace number.

        Calls `_move_window_to_workspace` with wid increased by 1.
        FIXME possible nasty hack wid+1

        :param wid: root id got from Tkinter
        :type wid: int
        :param number: our custom workspace number
        :type number: int
        """
        return self._move_window_to_workspace(wid + 1, number)
