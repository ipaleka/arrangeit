import tkinter as tk

from pynput import mouse

from arrangeit.constants import (
    TITLE_LABEL_FG,
    TITLE_LABEL_BG,
    TITLE_LABEL_ANCHOR,
    TITLE_LABEL_PADX,
    TITLE_LABEL_PADY,
)


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
        self.pack()
        self.setup_widgets()
        self.setup_bindings()

    def setup_widgets(self):
        """Creates and packs all the frame's variables and widgets."""
        self.title = tk.StringVar()
        title_label = tk.Label(
            textvariable=self.title,
            foreground=TITLE_LABEL_FG,
            background=TITLE_LABEL_BG,
            anchor=TITLE_LABEL_ANCHOR,
            padx=TITLE_LABEL_PADX,
            pady=TITLE_LABEL_PADY,
        )
        title_label.pack(fill=tk.X)

        # bitmap = tk.BitmapImage(file="bitmap.xbm")

        # self.icon = tk.Label(bitmap=bitmap)
        # self.icon.bitmap = bitmap # keep a reference!
        # self.icon.pack()

        # self.icon["bitmap"] = value

    def setup_bindings(self):
        """Binds relevant events to related controller callbacks.

        `bind_all` method is used so events can be catch in label widget too.
        """
        self.bind_all("<Escape>", self.controller.on_escape_key_pressed)
        self.bind_all("<Button-1>", self.controller.on_mouse_left_down)
        self.bind_all("<Button-2>", self.controller.on_mouse_middle_down)
        self.bind_all("<Button-3>", self.controller.on_mouse_right_down)

    def update_widgets(self, model):
        """Updates widgets with the data from provided WindowModel instance.

        :param model: window data
        :type model: :class:`WindowModel` instance
        """
        self.title.set(model.title)
