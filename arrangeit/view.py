import tkinter as tk
from tkinter.font import nametofont

from PIL import ImageTk, Image
from pynput import mouse

from arrangeit import constants
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
        self.setup_widgets()
        self.setup_bindings()

    def setup_widgets(self):
        """Creates and packs all the frame's variables and widgets."""
        self.setup_title()
        self.setup_name()
        self.setup_icon()
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
                    nametofont("TkDefaultFont")["size"],
                    constants.TITLE_LABEL_FONT_INCREASE,
                ),
            ),
            height=constants.TITLE_LABEL_HEIGHT,
            foreground=constants.TITLE_LABEL_FG,
            background=constants.TITLE_LABEL_BG,
            anchor=constants.TITLE_LABEL_ANCHOR,
            padx=constants.TITLE_LABEL_PADX,
            pady=constants.TITLE_LABEL_PADY,
        )
        self.title_label.place(
            relheight=constants.TITLE_LABEL_RELHEIGHT,
            relwidth=constants.TITLE_LABEL_RELWIDTH,
        )

    def setup_icon(self):
        """Sets `icon` Label widget."""
        self.icon = tk.Label(
            self,
            bitmap="hourglass",
            background=constants.ICON_LABEL_BG,
            anchor=constants.ICON_LABEL_ANCHOR,
            padx=constants.ICON_LABEL_PADX,
            pady=constants.ICON_LABEL_PADY,
        )
        self.icon.place(
            relx=constants.TITLE_LABEL_RELWIDTH + constants.NAME_LABEL_RELWIDTH / 2,
            anchor=constants.ICON_LABEL_ANCHOR,
            y=constants.ICON_LABEL_PADY,
        )

    def setup_name(self):
        """Sets `name` variable and corresponding Label widget."""
        self.name = tk.StringVar()
        self.name_label = tk.Label(
            self,
            textvariable=self.name,
            height=constants.NAME_LABEL_HEIGHT,
            foreground=constants.NAME_LABEL_FG,
            background=constants.NAME_LABEL_BG,
            anchor=constants.NAME_LABEL_ANCHOR,
            padx=constants.NAME_LABEL_PADX,
            pady=constants.NAME_LABEL_PADY,
        )
        self.name_label.place(
            relx=constants.TITLE_LABEL_RELWIDTH,
            relheight=constants.NAME_LABEL_RELHEIGHT,
            relwidth=constants.NAME_LABEL_RELWIDTH,
        )

    def setup_workspaces(self):
        """Creates `workspaces` widget and sets corresponding variable."""
        self.workspaces = WorkspacesCollection(self)
        self.workspaces.place(
            rely=constants.NAME_LABEL_RELHEIGHT,
            relx=constants.TITLE_LABEL_RELWIDTH,
            relheight=constants.WORKSPACES_FRAME_RELHEIGHT,
            relwidth=constants.WORKSPACES_FRAME_RELWIDTH,
        )

    def setup_windows(self):
        """Creates `windows` widget and sets corresponding variable."""
        self.windows = WindowsList(self)
        self.windows.place(
            rely=constants.TITLE_LABEL_RELHEIGHT,
            relheight=constants.WINDOWS_LIST_RELHEIGHT,
            relwidth=constants.WINDOWS_LIST_RELWIDTH,
        )

    def startup(self):
        """Shows master and then calculates and sets now visible parameters.

        Calls `focus_set` so frame can trigger keyboard events.
        """
        self.master.update()
        self.master.deiconify()
        self.place(width=self.master.winfo_width(), height=self.master.winfo_height())
        self.title_label.configure(
            wraplength=int(self.master.winfo_width() * constants.TITLE_LABEL_RELWIDTH)
        )
        self.name_label.configure(
            wraplength=int(self.master.winfo_width() * constants.NAME_LABEL_RELWIDTH)
        )
        self.focus_set()

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
        self.workspaces.select_active(model.workspace)


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
        self.config(background=constants.WORKSPACE_NUMBER_LABEL_BG)

    def add_workspaces(self, workspaces):
        """Creates children workspaces widgets from provided list of workspaces

        Creates no widget for configuration without multiple workspaces.
        Widgets are stacked related to their numbers from top right two positions
        towards bottom and then too the left,
        Actual workspaces are placed from left to right, then down the same orientation.
        Still, as a design decision, we use the same size for every configuration
        having less than 5 workspaces.

        :param workspaces: list of workspaces two-tuples (number, name)
        :type workspaces: [(int, str)]
        :var relwidth: workspace widget width
        :type relwidth: float
        """
        if len(workspaces) < 2:
            return True

        relheight = 0.5 if len(workspaces) < 5 else float(1 / ((len(workspaces) - 1) // 2 + 1))
        for i, workspace in enumerate(workspaces):
            widget = Workspace(self, number=workspace[0], name=workspace[1])
            widget.place(
                relheight=relheight,
                relwidth=0.5,
                relx=(i % 2) * 0.5,
                rely=(i // 2) * relheight,
            )

    def select_active(self, number):
        """Emphasizes active workspace and deemphasizes all others.

        Foreground text coloured by constant SELECTED_COLOR is used
        to emphasize selection.

        :var number: number of workspace to select
        :type number: int
         """
        workspaces = self.winfo_children()
        if len(workspaces) < 2:
            return True

        for workspace in workspaces:
            color = (
                constants.SELECTED_COLOR
                if workspace.number == number
                else constants.WORKSPACE_NUMBER_LABEL_FG
            )
            workspace.number_label.config(foreground=color)
            workspace.name_label.config(foreground=color)

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
        self.parent = parent
        self.number = number
        self.name = name
        self.setup_widgets()

    def get_humanized_number(self, number):
        """Returns workspace number without screen part and increased by 1

        as systems count workspaces from 0, but users expect to be from 1.

        :var number: workspace number
        :type number: int
        """
        return str(number % 1000 + 1)

    def setup_widgets(self):
        """Creates and packs all the frame's variables and widgets.

        As systems counts workspace from 0, we increase number by 1.
        """

        self.number_label = tk.Label(
            self,
            text=self.get_humanized_number(self.number),
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"],
                    constants.WORKSPACE_NUMBER_FONT_INCREASE,
                ),
            ),
            foreground=constants.WORKSPACE_NUMBER_LABEL_FG,
            background=constants.WORKSPACE_NUMBER_LABEL_BG,
            anchor=constants.WORKSPACE_NUMBER_LABEL_ANCHOR,
            padx=constants.WORKSPACE_NUMBER_LABEL_PADX,
            pady=constants.WORKSPACE_NUMBER_LABEL_PADY,
        )
        self.number_label.place(
            relheight=constants.WORKSPACE_NUMBER_RELHEIGHT,
            relwidth=constants.WORKSPACE_NUMBER_RELWIDTH,
        )

        self.name_label = tk.Label(
            self,
            text=self.name,
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"],
                    constants.WORKSPACE_NAME_FONT_INCREASE,
                ),
            ),
            height=constants.WORKSPACE_NAME_LABEL_HEIGHT,
            foreground=constants.WORKSPACE_NAME_LABEL_FG,
            background=constants.WORKSPACE_NAME_LABEL_BG,
            anchor=constants.WORKSPACE_NAME_LABEL_ANCHOR,
            padx=constants.WORKSPACE_NAME_LABEL_PADX,
            pady=constants.WORKSPACE_NAME_LABEL_PADY,
        )
        self.name_label.place(
            rely=constants.WORKSPACE_NUMBER_RELHEIGHT,
            relheight=constants.WORKSPACE_NAME_RELHEIGHT,
            relwidth=constants.WORKSPACE_NAME_RELWIDTH,
        )

    def setup_bindings(self):
        """Binds relevant events to related parent callback."""
        # self.bind_all("<Button-1>", self.parent.on_child_activated)
        # self.bind_all("<Button-2>", self.parent.on_child_activated)


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

    def add_windows(self, windows):
        """Creates children widgets from provided windows list.

        :param windows: list of windows tuples (number, title, icon)
        :type windows: [(int, str, :class:`PIL.Image.Image`)]
        """
        for i, window in enumerate(windows):
            widget = ListedWindow(self, wid=window[0], title=window[1], icon=window[2])
            self.place_widget_on_position(widget, i)

    def place_widget_on_position(self, widget, position):
        """Configure placement and place provided widget at provided vertical position.

        :param widget: Tkinter Frame widget
        :type widget: :class:`ListedWindow`
        :param position: vertical position in parent starting from top
        :type position: int
        """
        widget.place(
            relheight=constants.LISTED_WINDOW_RELHEIGHT,
            relwidth=1.0,
            relx=0.0,
            rely=position * constants.LISTED_WINDOW_RELHEIGHT,
        )

    def place_children(self):
        """Place children widgets in order.

        Used after the top widget is destroyed.
        """
        for i, widget in enumerate(self.winfo_children()):
            self.place_widget_on_position(widget, i)

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
    :var wid: window id
    :type wid: int
    :var title: window title
    :type title: str
    :var icon: window's application icon
    :type icon: Image.Image
    """

    parent = None
    wid = 0
    title = ""
    icon = constants.BLANK_ICON

    def __init__(self, parent=None, wid=0, title="", icon=constants.BLANK_ICON):
        """Sets attributes from provided arguments and sets the packer

        after super __init__ is called.
        """
        super().__init__(parent)
        self.parent = parent
        self.wid = wid
        self.title = title
        self.icon = self.get_icon_image(icon)
        self.setup_widgets()

    def get_icon_image(self, icon):
        """Returns provided icon resized and converted to format suitable for Tkinter.

        :var icon: window's application icon
        :type icon: :class:`PIL.Image.Image`
        :returns: :class:`PIL.ImageTk.PhotoImage`
        """
        return ImageTk.PhotoImage(
            icon.resize((int(constants.ICON_WIDTH / 2), int(constants.ICON_WIDTH / 2))),
            Image.ANTIALIAS,
        )

    def setup_widgets(self):
        """Creates and packs all the frame's variables and widgets."""
        title_label = tk.Label(
            self,
            text=self.title,
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"],
                    constants.LISTED_WINDOW_NAME_FONT_INCREASE,
                ),
            ),
            foreground=constants.LISTED_WINDOW_LABEL_FG,
            background=constants.LISTED_WINDOW_LABEL_BG,
            anchor=constants.LISTED_WINDOW_LABEL_ANCHOR,
            padx=constants.LISTED_WINDOW_LABEL_PADX,
            pady=constants.LISTED_WINDOW_LABEL_PADY,
        )
        title_label.place(
            x=constants.ICON_WIDTH / 2 + constants.LISTED_ICON_LABEL_PADX,
            relheight=1.0,
            relwidth=constants.LISTED_WINDOW_RELWIDTH,
        )

        icon_label = tk.Label(
            self,
            image=self.icon,
            background=constants.LISTED_ICON_LABEL_BG,
            anchor=constants.LISTED_ICON_LABEL_ANCHOR,
            padx=constants.LISTED_ICON_LABEL_PADX,
            pady=constants.LISTED_ICON_LABEL_PADY,
        )
        icon_label.place(
            x=constants.LISTED_ICON_LABEL_PADX / 2,
            rely=0.5,
            relheight=1.0,
            anchor=constants.LISTED_ICON_LABEL_ANCHOR,
        )
        self.config(background=constants.LISTED_WINDOW_LABEL_BG)

    def setup_bindings(self):
        """Binds relevant events to related parent callback."""
        # self.bind_all("<Button-1>", self.parent.on_child_activated)
        # self.bind_all("<Button-2>", self.parent.on_child_activated)
