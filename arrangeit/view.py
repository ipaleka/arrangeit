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
    :type master: :class:`Tk` root window instance
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

    def setup_bindings(self):
        """Binds relevant events to related controller callbacks.

        `bind_all` method is used so events can be catch in label widget too.
        """
        self.bind_all("<Escape>", self.controller.on_escape_key_pressed)
        self.bind_all("<Button-1>", self.controller.on_mouse_left_down)
        self.bind_all("<Button-2>", self.controller.on_mouse_middle_down)
        self.bind_all("<Button-3>", self.controller.on_mouse_right_down)

    def setup_title(self):
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
