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

import tkinter as tk
from gettext import gettext as _
from tkinter.font import ITALIC, NORMAL, nametofont

from PIL import Image, ImageTk

from arrangeit.options import OptionsDialog
from arrangeit.settings import Settings
from arrangeit.utils import increased_by_fraction, open_image, set_icon


def get_tkinter_root():
    """Initializes and returns Tkinter root window.

    :returns: :class:`tk.Tk` window instance
    """
    root = tk.Tk(className="arrangeit")
    root.title("arrangeit")
    set_icon(root)
    return root


def get_screenshot_widget(root):
    """Returns Label widget that will hold screenshot image in background.

    :param root: application main window
    :type root: :class:`tk.Tk`
    :returns: :class:`tk.Label`
    """
    label = tk.Label(root)
    label.place(x=Settings.SCREENSHOT_SHIFT_PIXELS, y=Settings.SCREENSHOT_SHIFT_PIXELS)
    return label


class ViewApplication(tk.Frame):
    """Tkinter frame showing current window from the data provided through controller.

    :var ViewApplication.master: master Tkinter window
    :type ViewApplication.master: :class:`tk.Tk` root window instance
    :var ViewApplication.controller: controller object providing windows data
    :type ViewApplication.controller: type(:class:`BaseController`) instance (platform specific)
    """

    master = None
    controller = None

    def __init__(self, master=None, controller=None):
        """Sets master and controller attributes from provided arguments

        after super __init__ is called. Then calls :func:`setup_widgets
        and :func:`setup_bindings` methods.
        """
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.config(background=Settings.MAIN_BG)
        self.setup_widgets()
        self.setup_bindings()

    def hide_root(self):
        """Hides master/root window."""
        self.master.withdraw()

    def reset_bindings(self):
        """Unbinds all relevant events and binds those for positioning routine."""
        self.unbind_all("<Button-1>")
        self.unbind_all("<Button-2>")
        self.unbind_all("<Button-3>")
        self.unbind_all("<Key>")

        self.title_label.bind("<Button-1>", self.controller.on_continue)
        self.icon.bind("<Button-1>", self.controller.on_continue)
        self.windows.bind("<Button-1>", self.controller.on_continue)
        self.workspaces.bind("<Button-1>", self.controller.on_continue)

    def show_root(self):
        """Shows master/root window."""
        self.master.update()
        self.master.deiconify()

    def setup_bindings(self):
        """Binds relevant events to related controller callbacks.

        ``bind_all`` method is used if possible so events can be catch in label widget.
        It first unbinds Button-1 events (in case they were bound
        in :func:`reset_bindings`)

        NOTE master is None check exists solely because unit tests.
        """
        self.unbind_all("<Button-1>")

        if self.master is not None:
            self.master.bind("<Button-1>", self.controller.on_mouse_left_down)
        self.bind("<Button-1>", self.controller.on_mouse_left_down)
        self.title_label.bind("<Button-1>", self.controller.on_mouse_left_down)
        self.bind_all("<Button-2>", self.controller.on_mouse_middle_down)
        self.bind_all("<Button-3>", self.controller.on_mouse_right_down)
        self.bind_all("<Key>", self.controller.on_key_pressed)
        self.bind("<Enter>", self.controller.on_focus)

    def setup_corner(self):
        """Creates and places corner widget in the default corner 0."""
        self.corner = CornerWidget(
            self.master, shift=Settings.SHIFT_CURSOR, background=Settings.CORNER_COLOR
        )

    def setup_icon(self):
        """Sets and places icon label widget."""
        self.icon = tk.Label(
            self,
            bitmap="hourglass",
            background=Settings.ICON_LABEL_BG,
            padx=Settings.ICON_LABEL_PADX,
            pady=Settings.ICON_LABEL_PADY,
        )
        self.icon.place(
            relx=Settings.TITLE_LABEL_RELWIDTH + Settings.NAME_LABEL_RELWIDTH / 2,
            anchor=Settings.ICON_LABEL_ANCHOR,
        )

    def setup_name(self):
        """Sets and places application name label widget."""
        self.name = tk.StringVar()
        self.name_label = tk.Label(
            self,
            textvariable=self.name,
            height=Settings.NAME_LABEL_HEIGHT,
            foreground=Settings.NAME_LABEL_FG,
            background=Settings.NAME_LABEL_BG,
            anchor=Settings.NAME_LABEL_ANCHOR,
            padx=Settings.NAME_LABEL_PADX,
            pady=Settings.NAME_LABEL_PADY,
        )
        self.name_label.place(
            relx=Settings.TITLE_LABEL_RELWIDTH,
            relheight=Settings.NAME_LABEL_RELHEIGHT,
            relwidth=Settings.NAME_LABEL_RELWIDTH,
        )

    def setup_resizable(self):
        """Sets and places resizable label widget."""
        self.resizable = Resizable(self, background=Settings.TITLE_LABEL_BG)
        self.resizable.place(
            x=-(Settings.PROPERTY_ICON_SIZE + Settings.PROPERTY_ICON_PADX),
            y=-(Settings.PROPERTY_ICON_SIZE + Settings.PROPERTY_ICON_PADY),
            relx=Settings.TITLE_LABEL_RELWIDTH,
            rely=Settings.TITLE_LABEL_RELHEIGHT,
        )

    def setup_restored(self):
        """Sets and places restored label widget."""
        self.restored = Restored(self, background=Settings.TITLE_LABEL_BG)
        self.restored.place(
            x=-2 * (Settings.PROPERTY_ICON_SIZE + Settings.PROPERTY_ICON_PADX),
            y=-(Settings.PROPERTY_ICON_SIZE + Settings.PROPERTY_ICON_PADY),
            relx=Settings.TITLE_LABEL_RELWIDTH,
            rely=Settings.TITLE_LABEL_RELHEIGHT,
        )

    def setup_statusbar(self):
        """Creates and places ``statusbar`` widget and sets corresponding variable."""
        self.statusbar = Statusbar(self)
        self.statusbar.place(
            rely=Settings.TITLE_LABEL_RELHEIGHT + Settings.WINDOWS_LIST_RELHEIGHT,
            relheight=Settings.STATUSBAR_RELHEIGHT,
            relwidth=Settings.STATUSBAR_RELWIDTH,
        )

    def setup_title(self):
        """Sets and places title label widget."""
        self.title = tk.StringVar()
        self.title_label = tk.Label(
            self,
            textvariable=self.title,
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"],
                    Settings.TITLE_LABEL_FONT_INCREASE,
                ),
            ),
            height=Settings.TITLE_LABEL_HEIGHT,
            foreground=Settings.TITLE_LABEL_FG,
            background=Settings.TITLE_LABEL_BG,
            anchor=Settings.TITLE_LABEL_ANCHOR,
            padx=Settings.TITLE_LABEL_PADX,
            pady=Settings.TITLE_LABEL_PADY,
        )
        self.title_label.place(
            relheight=Settings.TITLE_LABEL_RELHEIGHT,
            relwidth=Settings.TITLE_LABEL_RELWIDTH,
        )

    def setup_toolbar(self):
        """Creates and places ``toolbar`` widget and sets corresponding variable."""
        self.toolbar = Toolbar(self)
        self.toolbar.place(
            rely=Settings.TITLE_LABEL_RELHEIGHT + Settings.WORKSPACES_FRAME_RELHEIGHT,
            relx=Settings.WINDOWS_LIST_RELWIDTH,
            relheight=Settings.TOOLBAR_RELHEIGHT,
            relwidth=Settings.TOOLBAR_RELWIDTH,
        )

    def setup_widgets(self):
        """Calls all the frame's widgets creation and placement methods."""
        self.setup_title()
        self.setup_resizable()
        self.setup_restored()
        self.setup_name()
        self.setup_icon()
        self.setup_workspaces()
        self.setup_windows()
        self.setup_statusbar()
        self.setup_toolbar()
        self.setup_corner()

    def setup_windows(self):
        """Creates and places ``windows`` widget and sets corresponding variable."""
        self.windows = WindowsList(self)
        self.windows.place(
            rely=Settings.TITLE_LABEL_RELHEIGHT,
            relheight=Settings.WINDOWS_LIST_RELHEIGHT,
            relwidth=Settings.WINDOWS_LIST_RELWIDTH,
        )

    def setup_workspaces(self):
        """Creates and places ``workspaces`` widget and sets corresponding variable."""
        self.workspaces = WorkspacesCollection(self)
        self.workspaces.place(
            rely=Settings.NAME_LABEL_RELHEIGHT,
            relx=Settings.TITLE_LABEL_RELWIDTH,
            relheight=Settings.WORKSPACES_FRAME_RELHEIGHT,
            relwidth=Settings.WORKSPACES_FRAME_RELWIDTH,
        )

    def startup(self):
        """Shows master and then calculates and sets now visible parameters.

        Calls :func:`focus_set` so frame can trigger keyboard events.
        """
        self.show_root()
        self.place(width=self.master.winfo_width(), height=self.master.winfo_height())
        self.title_label.config(
            wraplength=int(self.master.winfo_width() * Settings.TITLE_LABEL_RELWIDTH)
        )
        self.name_label.config(
            wraplength=int(self.master.winfo_width() * Settings.NAME_LABEL_RELWIDTH)
        )
        self.focus_set()

    def update_widgets(self, model):
        """Updates widgets with the data from provided WindowModel instance.

        Tkinter needs a reference to image so we create ``icon_image`` reference.

        :param model: window data
        :type model: :class:`WindowModel` instance
        """
        self.title.set(model.title)
        self.resizable.set_value(model.resizable)
        self.restored.set_value(model.restored)
        self.icon_image = ImageTk.PhotoImage(model.icon)
        self.icon.config(image=self.icon_image)
        self.name.set(model.name)
        self.workspaces.select_active(model.workspace)


class PropertyIcon(tk.Label):
    """Tkinter label holding on/off image for a property.

    :var PropertyIcon.master: master widget
    :type PropertyIcon.master: :class:`tk.Frame`
    :var PropertyIcon.images: collection of two possible images
    :type PropertyIcon.images: dict
    :var PropertyIcon.colorized: collection of two highlighted images
    :type PropertyIcon.colorized: dict
    :var PropertyIcon.background: main background color
    :type PropertyIcon.background: str
    :var PropertyIcon.value: current widget value
    :type PropertyIcon.value: Boolean
    :var PropertyIcon.on_name: image name when the property is on
    :type PropertyIcon.on_name: str
    :var PropertyIcon.off_name: image name when the property is off
    :type PropertyIcon.off_name: str
    :var PropertyIcon.callback: method to call on triggered event
    :type PropertyIcon.callback: method
    """

    master = None
    images = {True: None, False: None}
    colorized = {True: None, False: None}
    background = "white"
    value = True
    on_name = None
    off_name = None
    callback = None

    def __init__(self, master=None, background="white", callback=None):
        """Sets master attribute from provided argument

        after super __init__ is called.
        :param background: label background
        :type background: str
        """
        super().__init__(master)
        self.master = master
        self.background = background
        self.callback = callback
        self.setup_widgets()
        self.setup_bindings()

    def setup_widgets(self):
        """Configures widgets images and sets current image."""
        self.images[True] = ImageTk.PhotoImage(
            open_image(self.on_name, background=self.background)
        )
        self.images[False] = ImageTk.PhotoImage(
            open_image(self.off_name, background=self.background)
        )
        self.colorized[True] = ImageTk.PhotoImage(
            open_image(
                self.on_name,
                background=self.background,
                colorized=True,
                foreground=Settings.HIGHLIGHTED_COLOR,
            )
        )
        self.colorized[False] = ImageTk.PhotoImage(
            open_image(
                self.off_name,
                background=self.background,
                colorized=True,
                foreground=Settings.HIGHLIGHTED_COLOR,
            )
        )
        self.config(image=self.images[True])

    def setup_bindings(self):
        """Binds relevant events to related callback."""
        self.bind("<Enter>", self.on_widget_enter)
        self.bind("<Leave>", self.on_widget_leave)
        self.bind("<Button-1>", self.callback)

    def set_value(self, value):
        """Sets label image in relation to provided `value`.

        :param value: is property on or not
        :type value: Boolean
        """
        self.value = value
        self.config(image=self.images[self.value])

    def on_widget_enter(self, event):
        """Highlights widget by changing image and its foreground."""
        self.config(image=self.colorized[not self.value])
        return "break"

    def on_widget_leave(self, event):
        """Resets widget image and its foreground color."""
        self.config(image=self.images[self.value])
        return "break"


class Resizable(PropertyIcon):
    """Widget holding resizable/non-resizable image.

    :var Resizable.images: collection of two possible images
    :type Resizable.images: dict
    :var Resizable.colorized: collection of two highlighted images
    :type Resizable.colorized: dict
    :var Resizable.on_name: image name when the property is on
    :type Resizable.on_name: str
    :var Resizable.off_name: image name when the property is off
    :type Resizable.off_name: str
    """

    images = {True: None, False: None}
    colorized = {True: None, False: None}
    on_name = "resize.png"
    off_name = "move.png"

    def __init__(self, master=None, background="white"):
        """Sets master attribute from provided argument

        after super __init__ is called.
        :param background: label background
        :type background: str
        """
        super().__init__(
            master,
            background=background,
            callback=master.controller.on_resizable_change,
        )


class Restored(PropertyIcon):
    """Widget holding restored/minimized image.

    :var Restored.images: collection of two possible images
    :type Restored.images: dict
    :var Restored.colorized: collection of two highlighted images
    :type Restored.colorized: dict
    :var Restored.on_name: image name when the property is on
    :type Restored.on_name: str
    :var Restored.off_name: image name when the property is off
    :type Restored.off_name: str
    """

    images = {True: None, False: None}
    colorized = {True: None, False: None}
    on_name = "restore.png"
    off_name = "minimize.png"

    def __init__(self, master=None, background="white"):
        """Sets master attribute from provided argument

        after super __init__ is called.
        :param background: label background
        :type background: str
        """
        super().__init__(
            master, background=background, callback=master.controller.on_restored_change
        )


class CornerWidget(object):
    """Widget holding three frames for emphasizing current corner.

    :var CornerWidget.master: parent widget
    :type CornerWidget.master: :class:`tk.Tk`
    :var shift: cursor shift from corner in pixels
    :type shift: int
    :var CornerWidget.background: widget background color
    :type CornerWidget.background: str
    :var length: axes frame length (long side) in pixels
    :type length: int
    :var width: axes frame width (small side) in pixels
    :type width: int
    :var box_size: box frame width/height in pixels
    :type box_size: int
    """

    master = None
    shift = 0
    background = "red"
    length = 20
    width = 4
    box_size = 8

    def __init__(self, master=None, shift=0, background="red"):
        """Creates and places widget frames and sets master and shift attributes

        from provided arguments.

        :param master: parent widget
        :type master: :class:`tk.Frame`
        :var shift: cursor shift from corner in pixels
        :type shift: int
        :var background: widget background color
        :type background: str
        """
        self.master = master
        self.shift = shift
        self.background = background
        self.setup_widgets()

    def anchor(self, corner=0):
        """Returns anchor for provided corner.

        :returns: str
        """
        return {0: "nw", 1: "ne", 2: "se", 3: "sw"}.get(corner)

    def get_place_parameters(self, corner, size_property):
        """Returns parameters for place method for given corner and size method.

        :returns: dict
        """
        parameters = {
            "relx": 0.0,
            "rely": 0.0,
            "x": size_property,
            "y": size_property,
            "anchor": self.anchor(corner),
        }
        if corner // 2:
            parameters["rely"] = 1.0
            parameters["y"] = -parameters["y"]
        if corner % 3:
            parameters["relx"] = 1.0
            parameters["x"] = -parameters["x"]
        return parameters

    def hide_corner(self):
        """Places widget frames in provided corner."""
        self.horizontal.place(relx=0.0, rely=0.0, y=-self.width * 2)
        self.vertical.place(relx=0.0, rely=0.0, x=-self.width * 2)
        self.box.place(relx=0.0, rely=0.0, x=-self.box_size * 2)

    @property
    def max_xy(self):
        """Returns placement on axis related to shift.

        :returns: int
        """
        return max(0, self.shift - self.width)

    @property
    def max_box(self):
        """Returns box placement on axis related to shift.

        :returns: int
        """
        return max(self.width, self.shift)

    def set_corner(self, corner=0):
        """Places widget frames in provided corner."""
        params = self.get_place_parameters(corner, self.max_xy)
        self.horizontal.place(**params)
        self.vertical.place(**params)

        params = self.get_place_parameters(corner, self.max_box)
        self.box.place(**params)

    def setup_widgets(self):
        """Creates all three frames and places them in default corner."""
        common = {"master": self.master, "bg": self.background, "borderwidth": 0}
        self.horizontal = tk.Frame(**common, width=self.length, height=self.width)
        self.vertical = tk.Frame(**common, width=self.width, height=self.length)
        self.box = tk.Frame(**common, width=self.box_size, height=self.box_size)
        self.set_corner()


class WorkspacesCollection(tk.Frame):
    """Tkinter frame holding all the available workspaces widgets.

    :var WorkspacesCollection.master: master widget
    :type WorkspacesCollection.master: :class:`tk.Frame`
    :var active: currently active workspace number
    :type active: int
    :var capacity: number of children workspaces
    :type capacity: int
    """

    master = None
    active = 0

    def __init__(self, master=None):
        """Sets master attribute from provided argument

        after super __init__ is called.
        """
        super().__init__(master)
        self.master = master
        self.config(background=Settings.WORKSPACE_NUMBER_LABEL_BG)

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

        relheight = (
            0.5 if len(workspaces) < 5 else float(1 / ((len(workspaces) - 1) // 2 + 1))
        )
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

        Foreground text coloured by setting SELECTED_COLOR is used
        to emphasize selection, together with SELECT_CURSOR setting.

        :param number: number of workspace to select
        :type number: int
        :var workspace: child widget
        :type workspace: :class:`Workspace`
        :var color: Tkinter color name
        :type color: str
        :var cursor: Tkinter cursor name
        :type cursor: str
         """
        workspaces = self.winfo_children()
        if len(workspaces) < 2:
            return True

        for workspace in workspaces:
            color = (
                Settings.SELECTED_COLOR
                if workspace.number == number
                else Settings.WORKSPACE_NUMBER_LABEL_FG
            )
            workspace.number_label.config(foreground=color)
            workspace.name_label.config(foreground=color)
            cursor = (
                Settings.DEFAULT_CURSOR
                if workspace.number == number
                else Settings.SELECT_CURSOR
            )
            workspace.config(cursor=cursor)

        self.active = number

    def on_workspace_label_button_down(self, event):
        """Activates workspace by number carried with provided event.

        :param event: catched event
        :type event: Tkinter event
        """
        self.master.controller.workspace_activated(event.widget.master.number)
        return "break"


class WindowsList(tk.Frame):
    """Tkinter frame holding titles and small icons of the windows in queue.

    :var WindowsList.master: master widget
    :type WindowsList.master: :class:`tk.Frame`
    """

    master = None

    def __init__(self, master=None):
        """Sets master attribute from provided argument

        after super __init__ is called.
        """
        super().__init__(master)
        self.master = master
        self.config(background=Settings.WINDOWS_LIST_BG)

    def add_windows(self, windows):
        """Creates children widgets from provided windows list.

        :param windows: list of windows tuples (number, title, icon)
        :type windows: [(int, str, :class:`PIL.Image.Image`)]
        """
        for i, window in enumerate(windows):
            widget = ListedWindow(self, wid=window[0], title=window[1], icon=window[2])
            self.place_widget_on_position(widget, i)

    def clear_list(self):
        """Destroys all children widgets."""
        for widget in self.winfo_children():
            widget.destroy()

    def place_widget_on_position(self, widget, position):
        """Configures placement and place provided widget at provided vertical position.

        :param widget: Tkinter Frame widget
        :type widget: :class:`ListedWindow`
        :param position: vertical position in master starting from top
        :type position: int
        """
        widget.place(
            relheight=Settings.LISTED_WINDOW_RELHEIGHT,
            relwidth=1.0,
            relx=0.0,
            rely=position * Settings.LISTED_WINDOW_RELHEIGHT,
        )

    def place_children(self):
        """Place children widgets in order.

        Used after the top widget is destroyed.
        """
        for i, widget in enumerate(self.winfo_children()):
            self.place_widget_on_position(widget, i)

    def on_window_label_button_down(self, event):
        """Activates window by wid carried with provided event.

        :param event: catched event
        :type event: Tkinter event
        """
        self.master.controller.listed_window_activated(event.widget.master.wid)
        return "break"


class Workspace(tk.Frame):
    """Tkinter frame holding individual workspace widget.

    :var Workspace.master: master widget
    :type Workspace.master: :class:`tk.Frame`
    :var Workspace.number: workspace number
    :type Workspace.number: int
    :var Workspace.name: workspace name
    :type Workspace.name: str
    """

    master = None
    number = 0
    name = ""

    def __init__(self, master=None, number=0, name=""):
        """Sets attributes from provided arguments

        after super __init__ is called. Then calls :func:`setup_widgets
        and :func:`setup_bindings` methods.
        """
        super().__init__(master)
        self.master = master
        self.number = number
        self.name = name
        self.setup_widgets()
        self.setup_bindings()

    def get_humanized_number(self, number):
        """Returns workspace number without screen part and increased by 1

        as systems count workspaces from 0, but users expect to be from 1.

        :param number: workspace number
        :type number: int
        """
        return str(number % 1000 + 1)

    def setup_widgets(self):
        """Creates and places all the frame's variables and widgets.

        As systems counts workspace from 0, we increase number by 1.
        """

        self.number_label = tk.Label(
            self,
            text=self.get_humanized_number(self.number),
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"],
                    Settings.WORKSPACE_NUMBER_FONT_INCREASE,
                ),
            ),
            foreground=Settings.WORKSPACE_NUMBER_LABEL_FG,
            background=Settings.WORKSPACE_NUMBER_LABEL_BG,
            anchor=Settings.WORKSPACE_NUMBER_LABEL_ANCHOR,
            padx=Settings.WORKSPACE_NUMBER_LABEL_PADX,
            pady=Settings.WORKSPACE_NUMBER_LABEL_PADY,
        )
        self.number_label.place(
            relheight=Settings.WORKSPACE_NUMBER_RELHEIGHT,
            relwidth=Settings.WORKSPACE_NUMBER_RELWIDTH,
        )

        self.name_label = tk.Label(
            self,
            text=self.name,
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"],
                    Settings.WORKSPACE_NAME_FONT_INCREASE,
                ),
            ),
            height=Settings.WORKSPACE_NAME_LABEL_HEIGHT,
            foreground=Settings.WORKSPACE_NAME_LABEL_FG,
            background=Settings.WORKSPACE_NAME_LABEL_BG,
            anchor=Settings.WORKSPACE_NAME_LABEL_ANCHOR,
            padx=Settings.WORKSPACE_NAME_LABEL_PADX,
            pady=Settings.WORKSPACE_NAME_LABEL_PADY,
        )
        self.name_label.place(
            rely=Settings.WORKSPACE_NUMBER_RELHEIGHT,
            relheight=Settings.WORKSPACE_NAME_RELHEIGHT,
            relwidth=Settings.WORKSPACE_NAME_RELWIDTH,
        )

    def setup_bindings(self):
        """Binds relevant events to related callback."""
        self.bind("<Enter>", self.on_widget_enter)
        self.bind("<Leave>", self.on_widget_leave)
        self.number_label.bind("<Button-1>", self.master.on_workspace_label_button_down)
        self.name_label.bind("<Button-1>", self.master.on_workspace_label_button_down)

    def on_widget_enter(self, event):
        """Highlights widget by changing foreground color."""
        if self.number != self.master.active:
            self.number_label.config(foreground=Settings.HIGHLIGHTED_COLOR)
            self.name_label.config(foreground=Settings.HIGHLIGHTED_COLOR)
        return "break"

    def on_widget_leave(self, event):
        """Resets widget foreground color."""
        if self.number != self.master.active:
            self.number_label.config(foreground=Settings.WORKSPACE_NUMBER_LABEL_FG)
            self.name_label.config(foreground=Settings.WORKSPACE_NUMBER_LABEL_FG)
        return "break"


class ListedWindow(tk.Frame):
    """Tkinter frame holding window title and smaller icon.

    :var ListedWindow.master: master widget
    :type ListedWindow.master: :class:`tk.Frame`
    :var ListedWindow.wid: window id
    :type ListedWindow.wid: int
    :var ListedWindow.title: window title
    :type ListedWindow.title: str
    :var ListedWindow.icon: window's application icon
    :type ListedWindow.icon: Image.Image
    """

    master = None
    wid = 0
    title = ""
    icon = Settings.BLANK_ICON

    def __init__(self, master=None, wid=0, title="", icon=Settings.BLANK_ICON):
        """Sets attributes from provided arguments

        after super __init__ is called. Also converts and references provided icon,
        then calls :func:`setup_widgets and :func:`setup_bindings` methods.
        """
        super().__init__(master, cursor=Settings.SELECT_CURSOR)
        self.master = master
        self.wid = wid
        self.title = title
        self.icon = self.get_icon_image(icon)
        self.setup_widgets()
        self.setup_bindings()

    def get_icon_image(self, icon):
        """Returns provided icon resized and converted to format suitable for Tkinter.

        :param icon: window's application icon
        :type icon: :class:`PIL.Image.Image`
        :returns: :class:`PIL.ImageTk.PhotoImage`
        """
        return ImageTk.PhotoImage(
            icon.resize(
                (int(Settings.ICON_SIZE / 2), int(Settings.ICON_SIZE / 2)),
                Image.ANTIALIAS,
            )
        )

    def setup_widgets(self):
        """Creates and places all the frame's variables and widgets."""
        self.title_label = tk.Label(
            self,
            text=self.title,
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"],
                    Settings.LISTED_WINDOW_NAME_FONT_INCREASE,
                ),
            ),
            foreground=Settings.LISTED_WINDOW_LABEL_FG,
            background=Settings.LISTED_WINDOW_LABEL_BG,
            anchor=Settings.LISTED_WINDOW_LABEL_ANCHOR,
            padx=Settings.LISTED_WINDOW_LABEL_PADX,
            pady=Settings.LISTED_WINDOW_LABEL_PADY,
        )
        self.title_label.place(
            x=Settings.ICON_SIZE / 2 + Settings.LISTED_ICON_LABEL_PADX,
            relheight=1.0,
            relwidth=Settings.LISTED_WINDOW_RELWIDTH,
        )

        self.icon_label = tk.Label(
            self,
            image=self.icon,
            background=Settings.LISTED_ICON_LABEL_BG,
            anchor=Settings.LISTED_ICON_LABEL_ANCHOR,
            padx=Settings.LISTED_ICON_LABEL_PADX,
            pady=Settings.LISTED_ICON_LABEL_PADY,
        )
        self.icon_label.place(
            x=Settings.LISTED_ICON_LABEL_PADX / 2,
            rely=0.5,
            relheight=1.0,
            anchor=Settings.LISTED_ICON_LABEL_ANCHOR,
        )
        self.config(background=Settings.LISTED_WINDOW_LABEL_BG)

    def setup_bindings(self):
        """Binds relevant events to related callback."""
        self.bind("<Enter>", self.on_widget_enter)
        self.bind("<Leave>", self.on_widget_leave)
        self.title_label.bind("<Button-1>", self.master.on_window_label_button_down)
        self.icon_label.bind("<Button-1>", self.master.on_window_label_button_down)

    def on_widget_enter(self, event):
        """Highlights widget by changing foreground color."""
        self.title_label.config(foreground=Settings.HIGHLIGHTED_COLOR)
        return "break"

    def on_widget_leave(self, event):
        """Resets widget foreground color."""
        self.title_label.config(foreground=Settings.LISTED_WINDOW_LABEL_FG)
        return "break"


class Statusbar(tk.Frame):
    """Tkinter frame showing app messages at the bottom of root window.

    :var Statusbar.master: master widget
    :type Statusbar.master: :class:`tk.Frame`
    """

    master = None

    def __init__(self, master=None):
        """Sets master attribute from provided argument

        after super __init__ is called. Also sets widget background.
        """
        super().__init__(master)
        self.master = master
        self.config(background=Settings.STATUSBAR_BG)
        self.setup_widgets()

    def setup_widgets(self):
        """Creates and places all the widget's variables and widgets."""
        self.message = tk.StringVar()
        self.message_label = tk.Label(
            self,
            textvariable=self.message,
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"],
                    Settings.STATUSBAR_LABEL_FONT_INCREASE,
                ),
                NORMAL,
                ITALIC,
            ),
            height=Settings.STATUSBAR_LABEL_HEIGHT,
            foreground=Settings.STATUSBAR_FG,
            background=Settings.STATUSBAR_BG,
            anchor=Settings.STATUSBAR_LABEL_ANCHOR,
            padx=Settings.STATUSBAR_LABEL_PADX,
            pady=Settings.STATUSBAR_LABEL_PADY,
        )
        self.message_label.pack()


class Toolbar(tk.Frame):
    """Tkinter frame holding options and quit button.

    :var Toolbar.master: master widget
    :type Toolbar.master: :class:`tk.Frame`
    """

    master = None

    def __init__(self, master=None):
        """Sets master attribute from provided argument

        after super __init__ is called. Also sets widget background.
        """
        super().__init__(master)
        self.master = master
        self.config(background=Settings.TOOLBAR_BG)
        self.setup_widgets()

    def setup_widgets(self):
        """Creates and places all the frame's variables and widgets."""
        options_button = tk.Button(
            self,
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"],
                    Settings.TOOLBAR_BUTTON_FONT_INCREASE,
                ),
            ),
            text=_("Options"),
            activeforeground=Settings.HIGHLIGHTED_COLOR,
            command=self.on_options_click,
        )
        options_button.place(
            relx=Settings.TOOLBAR_BUTTON_SHRINK_WIDTH / 2,
            relheight=Settings.OPTIONS_BUTTON_RELHEIGHT
            - Settings.TOOLBAR_BUTTON_SHRINK_HEIGHT,
            relwidth=Settings.OPTIONS_BUTTON_RELWIDTH
            - Settings.TOOLBAR_BUTTON_SHRINK_WIDTH,
            anchor=Settings.OPTIONS_BUTTON_ANCHOR,
        )

        quit_button = tk.Button(
            self,
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"],
                    Settings.TOOLBAR_BUTTON_FONT_INCREASE,
                ),
            ),
            text=_("Quit"),
            activeforeground=Settings.HIGHLIGHTED_COLOR,
            command=self.master.controller.shutdown,
        )
        quit_button.place(
            relx=0.5 + Settings.TOOLBAR_BUTTON_SHRINK_WIDTH / 2,
            relheight=Settings.QUIT_BUTTON_RELHEIGHT
            - Settings.TOOLBAR_BUTTON_SHRINK_HEIGHT,
            relwidth=Settings.QUIT_BUTTON_RELWIDTH
            - Settings.TOOLBAR_BUTTON_SHRINK_WIDTH,
            anchor=Settings.QUIT_BUTTON_ANCHOR,
        )

    def on_options_click(self):
        """Creates and shows options dialog and hides root window."""
        options = OptionsDialog(self.master)
        options.wm_attributes("-topmost", True)
        self.master.hide_root()
        options.wm_attributes("-topmost", False)
