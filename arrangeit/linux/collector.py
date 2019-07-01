import gi
from PIL import Image

gi.require_version("Gdk", "3.0")
gi.require_version("Wnck", "3.0")
from gi.repository import Wnck, Gdk

from arrangeit.base import BaseCollector
from arrangeit.data import WindowModel

MOVE_RESIZE_MASKS = {
    "x": Wnck.WindowMoveResizeMask.X,
    "y": Wnck.WindowMoveResizeMask.Y,
    "w": Wnck.WindowMoveResizeMask.WIDTH,
    "h": Wnck.WindowMoveResizeMask.HEIGHT,
}


class Collector(BaseCollector):
    """Collecting windows class with GNU/Linux specific code."""

    def is_applicable(self, window_type):
        """Checks if provided `window_type` qualifies window for collecting.

        :param window_type: type of window
        :type window_type: Wnck.WindowType int flag
        :returns: Boolean
        """
        return window_type in (
            Wnck.WindowType.NORMAL,
            Wnck.WindowType.DIALOG,
            Wnck.WindowType.UTILITY,
        )

    def is_valid_state(self, window_type, window_state):
        """Checks if `window state` for `window_type` qualifies window to collect.

        :param window_type: type of window
        :type window_type: Wnck.WindowType int flag
        :param window_state: current state of window
        :type window_state: Wnck.WindowState int flag
        :returns: Boolean
        """
        return not (
            window_state & Wnck.WindowState.FULLSCREEN  # TODO Research do we need this
            or (
                window_type == Wnck.WindowType.DIALOG
                and window_state & Wnck.WindowState.SKIP_TASKLIST
            )
            or (
                window_state & Wnck.WindowState.HIDDEN
                and not window_state & Wnck.WindowState.MINIMIZED
            )
            or (
                window_state & Wnck.WindowState.SKIP_TASKLIST
                and window_state & Wnck.WindowState.SKIP_PAGER
                and window_state & Wnck.WindowState.BELOW
            )
        )

    def is_resizable(self, window_type):
        """Checks if provided `window_type` implies that window is resizable.

        :param window_type: type of window
        :type window_type: Wnck.WindowType int flag
        :returns: Boolean
        """
        return window_type in (Wnck.WindowType.NORMAL,)

    def is_restored(self, win):
        """Checks if provided `win` is not minimized.

        :param win: window instance to check
        :type win: :class:`Wnck.Window` object
        :returns: Boolean
        """
        return not win.is_minimized()

    def get_windows(self):
        """Returns windows list from the Wnck.Screen object.

        :var screen: provides all the windows instances
        :type screen: :class:`Wnck.Screen`
        :returns: list of Wnck.Window instances
        """
        screen = Wnck.Screen.get_default()
        screen.force_update()
        return screen.get_windows()

    def check_window(self, win):
        """Checks does window qualify to be collected

        by checking window type applicability with :func:`is_applicable`
        and its state validity for the type with :func:`is_valid_state`.

        :param win: window instance to check
        :type win: :class:`Wnck.Window` object
        :var window_type: window type
        :type window_type: Wnck.WindowType int flag
        :var window_state: window state
        :type window_state: Wnck.WindowState int flag
        :returns: Boolean
        """
        window_type = win.get_window_type()
        # First of all, skip windows that not qualify at all
        if not self.is_applicable(window_type):
            return False

        window_state = win.get_state()
        # Skip windows having type and state combination that not qualify
        if not self.is_valid_state(window_type, window_state):
            return False

        return True

    def add_window(self, win):
        """Creates WindowModel instance from provided win and adds it to collection.

        :param win: window to create WindowModel from it
        :type win: :class:`Wnck.Window` object
        """
        self.collection.add(
            WindowModel(
                wid=win.get_xid(),
                rect=tuple(win.get_geometry()),
                resizable=self.is_resizable(win.get_window_type()),
                restored=self.is_restored(win),
                title=win.get_name(),
                name=win.get_class_group_name(),
                icon=self.get_image_from_pixbuf(win.get_icon()),
                workspace=self.get_workspace_number_for_window(win),
            )
        )

    def get_image_from_pixbuf(self, pixbuf):
        """Returns PIL image converted from provided pixbuf.

        https://gist.github.com/mozbugbox/10cd35b2872628246140

        :returns: :class:`PIL.Image` instance
        """
        mode = "RGBA" if pixbuf.props.has_alpha else "RGB"
        return Image.frombytes(
            mode,
            (pixbuf.props.width, pixbuf.props.height),
            pixbuf.get_pixels(),
            "raw",
            mode,
            pixbuf.props.rowstride,
        )

    def get_workspace_number(self, workspace):
        """Returns integer containing screen and workspace numbers of the workspace.

        In returned integer screen number represents thousands part, and
        workspace number represents remainder of division by 1000.

        :param workspace: workspace instance
        :type workspace: :class:`Wnck.workspace`
        :returns: int
        """
        if workspace is None:
            return 0
        return 1000 * workspace.get_screen().get_number() + workspace.get_number()

    def get_workspace_number_for_window(self, win):
        """Returns workspace number for the provided window.

        :param win: window instance
        :type win: :class:`Wnck.Window`
        :returns: int
        """
        return self.get_workspace_number(win.get_workspace())

    def _get_available_wnck_workspaces(self):
        """Returns Wnck list of workspaces available on default screen.

        :var screen: screen object
        :type screen: :class:`Wnck.Screen`
        :returns: list of :class:`Wnck.Workspace` instances
        """
        screen = Wnck.Screen.get_default()
        screen.force_update()
        return screen.get_workspaces()

    def get_available_workspaces(self):
        """Returns custom list of workspaces available on default screen.

        Returned list contains two-tuples of calculated workspace number
        and corresponding name.

        :var workspaces: workspaces collection
        :type workspaces: list of :class:`Wnck.Workspace` instances
        :returns: [(int, str)]
        """
        workspaces = self._get_available_wnck_workspaces()
        if not workspaces:
            return [(0, "")]
        collection = []
        for i, workspace in enumerate(workspaces):
            collection.append(
                (self.get_workspace_number(workspace), workspace.get_name())
            )
        return collection

    def get_wnck_workspace_for_custom_number(self, number):
        """Returns :class:`Wnck.Workspace` instance from provided custom number.

        :var number: our custom workspace number
        :type number: int
        """
        try:
            return next(
                workspace
                for workspace in self._get_available_wnck_workspaces()
                if self.get_workspace_number(workspace) == number
            )
        except StopIteration:
            return False

    def get_window_by_wid(self, wid):
        """Returns window instance having provided wid.

        :param wid: window id
        :type wid: int
        :returns: Wnck.Window object
        """
        return Wnck.Window.get(wid)

    def _check_mask_part(self, model, parts, value=False):
        """Returns call to itself if parts are not exhausted or value if they are.

        :param model: model holding window data
        :type model: :class:`WindowModel` instance
        :param parts: rect elements names
        :type parts: list
        :param value: current value of bit flags
        :type value: :class:`Wnck.WindowMoveResizeMask` bits combination
        :var part: rect element name
        :type part: str
        :returns: flag
        """
        part = parts.pop()
        if getattr(model, part) != getattr(model, "changed_{}".format(part)):
            value = (
                value | MOVE_RESIZE_MASKS[part] if value else MOVE_RESIZE_MASKS[part]
            )
        if parts:
            return self._check_mask_part(model, parts, value)
        return value

    def get_window_move_resize_mask(self, model):
        """Returns flag indicating what is changed when we move/resize window.

        Calls recursive method traversing all rect parts.
        Returned flag is combination of the X, Y, WIDTH and HEIGHT bits.

        :param model: model holding window data
        :type model: :class:`WindowModel` instance
        :returns: flag
        """
        return self._check_mask_part(model, list(MOVE_RESIZE_MASKS.keys()))

    def get_monitors_rects(self):
        """Returns list of available monitors position and size rectangles.

        :var display: default display
        :type display: :class:`Gdk.Display`
        :var area: monitor working area rect
        :type area: :class:`Gdk.Rectangle`
        :returns: list [(x,y,w,h)]
        """
        display = Gdk.Display.get_default()
        rects = []
        for i in range(display.get_n_monitors()):
            area = display.get_monitor(i).get_workarea()
            rects.append((area.x, area.y, area.width, area.height))
        return rects
