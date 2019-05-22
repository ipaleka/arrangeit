import tkinter as tk
from tkinter.font import nametofont

from PIL import ImageTk
from pynput import mouse

from arrangeit.constants import (
    TITLE_LABEL_ANCHOR,
    TITLE_LABEL_BG,
    TITLE_LABEL_FG,
    TITLE_LABEL_FONT_INCREASE,
    TITLE_LABEL_HEIGHT,
    TITLE_LABEL_PADX,
    TITLE_LABEL_PADY,
    ICON_WIDTH,
    ICON_WIDTH_FRACTION,
    ICON_LABEL_ANCHOR,
    ICON_LABEL_BG,
    ICON_LABEL_PADX,
    ICON_LABEL_PADY,
    NAME_LABEL_ANCHOR,
    NAME_LABEL_BG,
    NAME_LABEL_FG,
    NAME_LABEL_HEIGHT,
    NAME_LABEL_PADX,
    NAME_LABEL_PADY,
)
from arrangeit.utils import increased_by_fraction


def get_tkinter_root():
    """Initializes and returns Tkinter root window.

    :returns: :class:`tkinter.Tk` window instance
    """
    return tk.Tk()


# NOTE following 3 functions probably should be moved somewhere else


def get_mouse_listener(callback):
    """Initializes mouse listener by binding it to provided ``callback`` and returns it.

    :returns: :class:`mouse.Listener` instance
    """
    return mouse.Listener(on_move=callback)


def click_left():
    """Makes a left button mouse click in the current cursor position."""
    controller = mouse.Controller()
    controller.press(mouse.Button.left)
    controller.release(mouse.Button.left)


def move_cursor(x, y):
    """Moves cursor position to a point defined by provided x and y."""
    controller = mouse.Controller()
    controller.position = (x, y)


class ViewApplication(tk.Frame):
    """Tkinter frame showing current window from the data provided through controller.

    :var master: parent Tkinter window
    :type master: :class:`tk.Tk` root window instance
    :var ViewApplication.controller: controller object providing windows data
    :type ViewApplication.controller: type(:class:`BaseController`) instance (platform specific)
    """

    master = None
    controller = None

    def __init__(self, master=None, controller=None):
        """Sets master and controller attributes from provided arguments

        after super __init__ is called. Then sets the packer and
        calls :func:`setup_widgets` method.
        """
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)
        self.setup_widgets()
        self.setup_bindings()

    def setup_widgets(self):
        """Creates and packs all the frame's variables and widgets."""
        self.grid_columnconfigure(0, weight=7)
        self.grid_columnconfigure(2, weight=2)
        self.setup_title()
        self.setup_icon()
        self.setup_name()
        self.setup_workspaces()
        self.setup_windows()

    def setup_bindings(self):
        """Binds relevant events to related controller callbacks.

        `bind_all` method is used so events can be catch in label widget too.
        """
        self.bind_all("<Button-1>", self.controller.on_mouse_left_down)
        self.bind_all("<Button-2>", self.controller.on_mouse_middle_down)
        self.bind_all("<Button-3>", self.controller.on_mouse_right_down)
        self.bind_all("<Key>", self.controller.on_key_pressed)

    def setup_title(self):
        """Sets `title` variable and corresponding Label widget."""
        self.title = tk.StringVar()
        self.title_label = tk.Label(
            self,
            textvariable=self.title,
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"], TITLE_LABEL_FONT_INCREASE
                ),
            ),
            height=TITLE_LABEL_HEIGHT,
            foreground=TITLE_LABEL_FG,
            background=TITLE_LABEL_BG,
            anchor=TITLE_LABEL_ANCHOR,
            padx=TITLE_LABEL_PADX,
            pady=TITLE_LABEL_PADY,
        )
        self.title_label.grid(row=0, column=0, sticky="new")

    def setup_icon(self):
        """Sets `icon` Label widget."""
        self.icon = tk.Label(
            self,
            bitmap="hourglass",
            background=ICON_LABEL_BG,
            anchor=ICON_LABEL_ANCHOR,
            padx=ICON_LABEL_PADX,
            pady=ICON_LABEL_PADY,
        )
        self.icon.grid(row=0, column=1, sticky="nsw")

    def setup_name(self):
        """Sets `name` variable and corresponding Label widget."""
        self.name = tk.StringVar()
        self.name_label = tk.Label(
            self,
            textvariable=self.name,
            height=NAME_LABEL_HEIGHT,
            foreground=NAME_LABEL_FG,
            background=NAME_LABEL_BG,
            anchor=NAME_LABEL_ANCHOR,
            padx=NAME_LABEL_PADX,
            pady=NAME_LABEL_PADY,
        )
        self.name_label.grid(row=0, column=2, sticky="nsew")

    def setup_workspaces(self):
        """Creates `workspaces` widget and sets corresponding variable."""
        self.workspaces = WorkspacesCollection(self)
        self.workspaces.grid(row=1, column=0, sticky="nsew")

    def setup_windows(self):
        """Creates `windows` widget and sets corresponding variable."""
        self.windows = WindowsList(self)
        self.windows.grid(row=1, column=2, sticky="nsw")

    def startup(self):
        """Shows master and then calculates and sets now visible parameters.

        Calls `focus_set` so frame can trigger keyboard events.
        """
        self.master.update()
        self.master.deiconify()
        self.focus_set()
        self.title_label.configure(
            wraplength=int(self.master.winfo_width() * (1 - ICON_WIDTH_FRACTION))
        )
        self.name_label.configure(
            wraplength=int(
                self.winfo_width() * ICON_WIDTH_FRACTION - ICON_WIDTH
            )
        )

    def update_widgets(self, model):
        """Updates widgets with the data from provided WindowModel instance.

        Tkinter needs a reference to image so we create `icon_image` reference.

        :param model: window data
        :type model: :class:`WindowModel` instance
        """
        self.title.set(model.title)
        self.icon_image = ImageTk.PhotoImage(model.icon)
        self.icon.configure(image=self.icon_image)
        self.name.set(model.name)


class WorkspacesCollection(tk.Frame):
    """Tkinter frame holding all the available workspaces widgets.

    :var parent: parent widget
    :type parent: :class:`.tk.Frame`
    """

    parent = None

    def __init__(self, parent=None):
        """Sets parent attribute from provided argument and sets the packer

        after super __init__ is called.
        """
        super().__init__(parent)
        self.parent = parent

        self["background"] = "red"

    def add_workspaces(self, workspaces):
        """Creates children widgets from provided list of workspaces.

        :var workspaces: list of workspaces two-tuples (number, name)
        :type workspaces: [(int, str)]
        """
        pass

    def on_child_activated(self, event):
        """Calls parent's controller method in charge for workspace activation.

        :var event: catched event
        :type event: Tkinter event
        """
        pass
        # self.parent.controller.workspace_activated(event.widget.number)
        # return "break"

    def highlight_workspace(self, number):
        """Visually emphasizes child workspace having provided number 

        and reset highlighting in other children to default.

        :var number: number of workspace to highlight
        :type number: int
        """
        pass


class Workspace(tk.Frame):
    """Tkinter frame holding individual workspace widget.

    :var parent: parent widget
    :type parent: :class:`.tk.Frame`
    :var number: workspace number
    :type number: int
    :var name: workspace name
    :type name: str
    """

    parent = None
    number = 0
    name = ""

    def __init__(self, parent=None, number=0, name=""):
        """Sets attributes from provided arguments and sets the packer

        after super __init__ is called.
        """
        super().__init__(parent)
        # self.parent = parent
        # self.number = number
        # self.name = name
        # self.pack(fill=tk.BOTH, expand=True)

        # self["background"] = "blue"

    def setup_bindings(self):
        """Binds relevant events to related parent callback."""
        # self.bind("<Button-1>", self.parent.on_child_activated)
        # self.bind("<Button-2>", self.parent.on_child_activated)


class WindowsList(tk.Frame):
    """Tkinter frame holding titles and small icons of the windows in queue.

    :var parent: parent widget
    :type parent: :class:`.tk.Frame`
    """

    parent = None

    def __init__(self, parent=None):
        """Sets parent attribute from provided argument and sets the packer

        after super __init__ is called.
        """
        super().__init__(parent)
        self.parent = parent

        self["background"] = "red"

    def add_windows(self, windows):
        """Creates children widgets from provided list of windows.

        :var windows: list of windows two-tuples (wid, title)
        :type windows: [(int, str)]
        """
        pass

    def on_child_activated(self, event):
        """Calls parent's controller method in charge for window activation.

        :var event: catched event
        :type event: Tkinter event
        """
        pass
        # self.parent.controller.window_activated(event.widget.wid)
        # return "break"

    def highlight_window(self, wid):
        """Visually emphasizes child window having provided wid

        and reset highlighting in other children to default.

        :var wid: window id to highlight
        :type wid: int
        """
        pass


class ListedWindow(tk.Frame):
    """Tkinter frame holding window title and smaller icon.

    :var parent: parent widget
    :type parent: :class:`.tk.Frame`
    :var number: workspace number
    :type number: int
    :var name: workspace name
    :type name: str
    """

    parent = None
    wid = 0
    title = ""

    def __init__(self, parent=None, wid=None, title=""):
        """Sets attributes from provided arguments and sets the packer

        after super __init__ is called.
        """
        super().__init__(parent)
        # self.parent = parent
        # self.wid = wid
        # self.title = title
        # self.pack(fill=tk.BOTH, expand=True)

        # self["background"] = "blue"

    def setup_bindings(self):
        """Binds relevant events to related parent callback."""
        # self.bind("<Button-1>", self.parent.on_child_activated)
        # self.bind("<Button-2>", self.parent.on_child_activated)
