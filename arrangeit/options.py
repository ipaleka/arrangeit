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

import gettext
import platform
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

import arrangeit
from arrangeit import options
from arrangeit.settings import Settings
from arrangeit.utils import get_resized_image, get_resource_path, set_icon

_ = gettext.translation("arrangeit", "arrangeit/locale", fallback=True).gettext

MESSAGES = {
    "_BG": _("Background:"),
    "_FG": _("Foreground:"),
    "CORNER_CURSOR_ARROW": _("Corner cursor with arrow"),
    "HIGHLIGHTED_COLOR": _("Highlighted:"),
    "ROOT_ALPHA": _("Main window opacity [%]:"),
    "ROOT_SIZE": _("Main window size:"),
    "SCREENSHOT_TO_GRAYSCALE": _("Grayscale background image"),
    "SCREENSHOT_BLUR_PIXELS": _("Background image blur [pixels]:"),
    "SCREENSHOT_DISABLED": _("Don't show background image"),
    "SELECTED_COLOR": _("Selected:"),
    "SHIFT_CURSOR": _("Corner cursor shift [pixels]:"),
    "SNAP_INCLUDE_SELF": _("Include itself in snapping"),
    "SNAP_PIXELS": _("Snapping size [pixels]:"),
    "SNAPPING_IS_ON": _("Use snapping"),
    "TITLE_LABEL_BG": _("Title background:"),
    "TITLE_LABEL_FG": _("Title foreground:"),
    "TRANSPARENCY_IS_ON": _("Use transparency"),
    "WINDOWS_LIST_COUNT": _("Queued windows shown:"),
    "about_title": _("About - arrangeit"),
    "appearance": _("Appearance"),
    "colors": _("Colors"),
    "files": _("Files"),
    "options_title": _("Options - arrangeit"),
    "save_default": _("Collected windows data saved to default file."),
    "setting_changed": _(
        "Setting is changed - some settings may require\n"
        "program restart in order for the change to take effect."
    ),
}
CLASSES = {int: "Scale", float: "FloatScale", bool: "Check", str: "Color"}
WIDGETS = {
    "appearance": (
        ("SCREENSHOT_DISABLED", {}),
        (
            "ROOT_SIZE",
            {"from_": 1, "to": 4, "resolution": 1, "tickinterval": 1, "digits": 1},
        ),
        ("TRANSPARENCY_IS_ON", {}),
        (
            "ROOT_ALPHA",
            {"from_": 50, "to": 99, "resolution": 2, "tickinterval": 20, "digits": 3},
        ),
        ("SNAP_INCLUDE_SELF", {}),
        (
            "WINDOWS_LIST_COUNT",
            {"from_": 4, "to": 10, "resolution": 1, "tickinterval": 3, "digits": 1},
        ),
        ("SCREENSHOT_TO_GRAYSCALE", {}),
        (
            "SCREENSHOT_BLUR_PIXELS",
            {"from_": 0, "to": 8, "resolution": 1, "tickinterval": 2, "digits": 1},
        ),
        ("CORNER_CURSOR_ARROW", {}),
        (
            "SHIFT_CURSOR",
            {"from_": 1, "to": 12, "resolution": 1, "tickinterval": 3, "digits": 1},
        ),
        ("SNAPPING_IS_ON", {}),
        (
            "SNAP_PIXELS",
            {"from_": 1, "to": 12, "resolution": 1, "tickinterval": 3, "digits": 1},
        ),
    ),
    "colors": (
        ("_BG", {}),
        ("_FG", {}),
        ("TITLE_LABEL_BG", {}),
        ("TITLE_LABEL_FG", {}),
        ("SELECTED_COLOR", {}),
        ("HIGHLIGHTED_COLOR", {}),
    ),
}
COLORS = (
    "white",
    "black",
    "gray",
    "slategray",
    "gray25",
    "gray75",
    "lightblue",
    "blue",
    "royalblue",
    "cyan",
    "orange",
    "salmon",
    "indianred",
    "red",
    "orchid",
    "pink",
    "green",
    "olivedrab",
    "wheat",
    "khaki",
    "tan",
    "lightgoldenrodyellow",
    "yellow",
)


class OptionsDialog(tk.Toplevel):
    """Tkinter dialog window for manipulating of user settings data.

    :var OptionsDialog.master: master widget
    :type OptionsDialog.master: :class:`tk.Tk`
    :var message: variable holding message log
    :type message: :class:`tk.StringVar`
    :var OptionsDialog.timer: id of active timer
    :type OptionsDialog.timer: int
    """

    master = None
    message = None
    timer = None

    def __init__(self, master=None):
        """Sets master attribute, position dialog on former master position

        and calls setup routines after super __init__ is called.
        """
        super().__init__(master)
        self.master = master
        self.setup_widgets()
        self.setup_bindings()
        self.title(MESSAGES["options_title"])
        set_icon(self)
        self.geometry(
            "+{}+{}".format(self.master.master.winfo_x(), self.master.master.winfo_y())
        )

    ## CONFIGURATION
    def create_frame(self, master):
        """Creates and returns frame that will holds pair of widgets.

        :param master: parent widget
        :type master: Tkinter widget
        """
        return ttk.Frame(master)

    def create_separator(self, master, vertical=False):
        """Creates and returns default horizontal separator of vertical if argument set.

        :param master: parent widget
        :type master: Tkinter widget
        :param vertical: is separator oriented vertical instead default horizontal
        :type vertical: Booleand
        """
        return ttk.Separator(master, orient=tk.VERTICAL if vertical else tk.HORIZONTAL)

    def create_widget(self, master, name, **kwargs):
        """Creates and returns presentation widget for setting with provided name.

        :param master: parent widget
        :type master: :class:`ttk.LabelFrame`
        :param name: setting name
        :type name: str
        :returns: Tkinter widget instance
        """
        return self.widget_class_from_name(name)(
            master,
            name=name,
            change_callback=self.change_setting,
            initial=getattr(Settings, name),
            label=MESSAGES[name],
            **kwargs
        )

    def setup_bindings(self):
        """Binds relevant events to related callback."""
        self.bind("<Destroy>", self.on_destroy_options)

    def setup_files_section(self):
        """Creates and packs widgets for section dealing with files.

        :returns: :class:`ttk.LabelFrame`
        """
        files = ttk.LabelFrame(self, text=MESSAGES["files"], labelanchor="nw")
        tk.Button(
            files,
            text=_("Save data to default file"),
            activeforeground=Settings.HIGHLIGHTED_COLOR,
            command=self.on_save_default,
        ).pack(
            side=tk.LEFT,
            padx=Settings.OPTIONS_WIDGETS_PADX,
            pady=Settings.OPTIONS_WIDGETS_PADY,
        )
        return files

    def setup_section(self, name, denominator=6):
        """Creates and packs widgets for section with provided name.

        :returns: :class:`ttk.LabelFrame`
        """
        section = ttk.LabelFrame(self, text=MESSAGES[name], labelanchor="nw")

        for i, (name, kwargs) in enumerate(WIDGETS[name]):
            if not i % denominator:
                frame = self.create_frame(section)
                frame.pack(fill=tk.X, side=tk.LEFT, expand=True)

            separator = self.create_separator(frame)
            separator.pack(fill=tk.X, expand=True)

            widget = self.create_widget(frame, name, **kwargs)
            if hasattr(widget, "label"):
                widget.label.pack(
                    fill=tk.X, side=tk.TOP, padx=Settings.OPTIONS_WIDGETS_PADX, pady=0
                )
            widget.pack(
                fill=tk.X,
                side=tk.TOP,
                padx=Settings.OPTIONS_WIDGETS_PADX,
                pady=Settings.OPTIONS_WIDGETS_PADY,
            )

        return section

    def setup_widgets(self):
        """Creates and packs all the options' widgets."""
        self.message = tk.StringVar()

        section_pack_kwargs = {
            "fill": tk.BOTH,
            "padx": Settings.OPTIONS_WIDGETS_PADX,
            "pady": Settings.OPTIONS_WIDGETS_PADY,
            "expand": True,
        }

        self.setup_section("appearance").pack(**section_pack_kwargs)
        self.setup_section("colors", denominator=2).pack(**section_pack_kwargs)
        self.setup_files_section().pack(**section_pack_kwargs)

        tk.Label(
            self,
            textvariable=self.message,
            height=Settings.OPTIONS_MESSAGE_HEIGHT,
            anchor="center",
        ).pack(fill=tk.X, pady=Settings.OPTIONS_WIDGETS_PADY)

        tk.Button(
            self,
            text=_("Continue"),
            activeforeground=Settings.HIGHLIGHTED_COLOR,
            command=self.destroy,
        ).pack(
            padx=Settings.OPTIONS_WIDGETS_PADX,
            pady=Settings.OPTIONS_WIDGETS_PADY * 2,
            anchor="se",
            side=tk.RIGHT,
        )

        tk.Button(
            self,
            text=_("About"),
            activeforeground=Settings.HIGHLIGHTED_COLOR,
            command=self.on_show_about,
        ).pack(
            padx=Settings.OPTIONS_WIDGETS_PADX,
            pady=Settings.OPTIONS_WIDGETS_PADY * 2,
            anchor="se",
            side=tk.RIGHT,
        )

    def widget_class_from_name(self, name):
        """Returns related widget class from provided setting name.

        :param name: setting name
        :type name: str
        :returns: custom Tkinter widget instance
        """
        typ = Settings.setting_type(name)
        if typ is None:
            return getattr(options, "ThemeOption")
        return getattr(options, "{}Option".format(CLASSES[typ]))

    ## COMMANDS
    def change_setting(self, name="", value=None):
        """Calls sontroller's change setting method and updates message log.

        Also cancels previous timer if it exists and create a new one.

        :param name: setting name
        :type name: str
        :param value: value for given name setting
        :type name: str/int/float
        """
        self.master.controller.change_setting(name, value)
        self.message.set(MESSAGES["setting_changed"])
        self.set_timer()

    def set_timer(self):
        """Cancels previous timer if it exists and creates a new one."""
        if self.timer is not None:
            self.after_cancel(self.timer)
        self.timer = self.after(Settings.TIMER_DELAY, self.message.set, "")

    ## EVENTS CALLBACKS
    def on_destroy_options(self, event):
        """Brings back root window and destroys options dialog."""
        self.master.show_root()
        self.destroy()

    def on_save_default(self):
        """Saves windows collection data to default file."""
        self.master.controller.save()
        self.message.set(MESSAGES["save_default"])
        self.set_timer()

    def on_show_about(self):
        """Creates and shows about dialog on top of this dialog."""
        AboutDialog(self).lift(self)


class ScaleOption(tk.Scale):
    """Tkinter widget for showing and changing range settings values.

    :var ScaleOption.master: master widget
    :type ScaleOption.master: :class:`tk.Toplevel`
    :var ScaleOption.name: setting name to change
    :type ScaleOption.name: str
    """

    master = None
    name = ""

    def __init__(
        self,
        master=None,
        name="",
        change_callback=None,
        initial=0,
        label="",
        from_=0,
        to=8,
        resolution=1,
        tickinterval=1,
        digits=1,
    ):
        """Sets master attribute and configs scale widget from provided arguments

        after super __init__ is called.

        Also sets command callback and orientation.

        :param master: parent widget
        :param master: :class:`tk.Toplevel`
        :param name: settings name to change
        :param name: str
        :param change_callback: callback method to call on value change
        :param change_callback: method
        :param initial: starting value
        :param initial: float/int
        :param label: explanation text/label for this scale
        :param label: str
        :param from_: starting value
        :param from_: float/int
        :param to: ending value
        :param to: float/int
        :param resolution: minimum step
        :param resolution: float/int
        :param tickinterval: named values on scale
        :param tickinterval: float/int
        :param digits: how many digits are shown on tick intervals
        :param digits: int
        """
        super().__init__(master)
        self.master = master
        self.name = name
        self.change_callback = change_callback
        self.config(
            label=label,
            from_=from_,
            to=to,
            resolution=resolution,
            tickinterval=tickinterval,
            digits=digits,
            orient=tk.HORIZONTAL,
        )
        self.set(initial)
        self.config(command=self.on_update_value)

    def on_update_value(self, value):
        self.change_callback(name=self.name, value=int(value))
        return "break"


class FloatScaleOption(ScaleOption):
    """Tkinter widget for showing and changing float range settings values."""

    def __init__(self, master, **kwargs):
        """Calls super class with initial multiplied by 100."""
        kwargs.update(initial=kwargs.get("initial", 0) * 100)
        super().__init__(master, **kwargs)

    def on_update_value(self, value):
        self.change_callback(name=self.name, value=float(value) / 100.0)
        return "break"


class CheckOption(tk.Checkbutton):
    """Tkinter widget for showing and changing Boolean values.

    :var CheckOption.master: master widget
    :type CheckOption.master: :class:`tk.Toplevel`
    :var CheckOption.name: setting name to change
    :type CheckOption.name: str
    :var CheckOption.var: variable holding the check button value
    :type CheckOption.var: :class:`tk.IntVar`
    """

    master = None
    name = ""
    var = None

    def __init__(
        self, master=None, name="", change_callback=None, initial=False, label=""
    ):
        """Sets master attribute and configs check button widget from provided arguments

        after super __init__ is called.

        Also sets command callback.

        :param master: parent widget
        :param master: :class:`tk.Toplevel`
        :param name: settings name to change
        :param name: str
        :param change_callback: callback method to call on value change
        :param change_callback: method
        :param initial: starting value
        :param initial: bool
        :param label: explanation text for this check button
        :param label: str
        """
        super().__init__(master)
        self.master = master
        self.name = name
        self.change_callback = change_callback
        self.var = tk.IntVar()
        self.config(text=label, variable=self.var, command=self.on_update_value)
        self.select() if initial else self.deselect()

    def on_update_value(self, *args):
        self.change_callback(name=self.name, value=bool(self.var.get()))
        return "break"


class ColorOption(tk.OptionMenu):
    """Tkinter widget for showing and changing Boolean values.

    :var ColorOption.master: master widget
    :type ColorOption.master: :class:`tk.Toplevel`
    :var ColorOption.name: setting name to change
    :type ColorOption.name: str
    :var ColorOption.var: variable holding the choice value
    :type ColorOption.var: :class:`tk.StringVar`
    """

    master = None
    name = ""
    var = None
    label = None

    def __init__(
        self,
        master=None,
        name="",
        change_callback=None,
        initial="",
        label="",
        choices=COLORS,
    ):
        """Sets master attribute and configs choice widget from provided arguments

        after super __init__ is called.

        Also sets command callback.

        :param master: parent widget
        :param master: :class:`tk.Toplevel`
        :param name: settings name to change
        :param name: str
        :param change_callback: callback method to call on value change
        :param change_callback: method
        :param initial: starting value
        :param initial: str
        :param label: explanation text for this check button
        :param label: str
        :param choices: collection of available text values
        :param choices: tuple
        """
        self.var = tk.StringVar()
        self.var.set(initial)
        super().__init__(
            master, self.var, initial, *choices, command=self.on_update_value
        )
        self.master = master
        self.name = name
        self.change_callback = change_callback
        self.label = tk.Label(self.master, text=label, anchor="sw")

    def on_update_value(self, *args):
        self.change_callback(name=self.name, value=self.var.get())
        return "break"


class ThemeOption(ColorOption):
    def __init__(self, *args, **kwargs):
        kwargs.update(initial=getattr(Settings, "MAIN{}".format(kwargs.get("name"))))
        super().__init__(*args, **kwargs)


class AboutDialog(tk.Toplevel):
    """Tkinter "About" dialog window.

    :var AboutDialog.master: master widget
    :type AboutDialog.master: :class:`tk.Tk`
    :var AboutDialog.logo: arrangeit logo
    :type AboutDialog.logo: :class:`PIL.ImageTk.PhotoImage`
    """

    master = None
    logo = None

    def __init__(self, master=None):
        """Sets master attribute, position dialog on former master position

        and calls setup routines after super __init__ is called.
        """
        super().__init__(master)
        self.master = master
        self.setup_widgets()
        self.title(MESSAGES["about_title"])
        set_icon(self)
        self.geometry("+{}+{}".format(self.master.winfo_x(), self.master.winfo_y()))

    def setup_widgets(self):
        """Creates and packs all the dialog's widgets."""
        self.logo = get_resized_image("logo.png", Settings.ABOUT_LOGO_SIZE)
        tk.Label(self, image=self.logo).pack(anchor="n", fill=tk.X, side=tk.TOP)

        with open(get_resource_path("COPYRIGHT"), "r") as notice:
            tk.Label(self, text=notice.read(), justify=tk.LEFT).pack(
                padx=Settings.OPTIONS_WIDGETS_PADX * 2,
                pady=Settings.OPTIONS_WIDGETS_PADY * 2,
                fill=tk.X,
                side=tk.TOP,
            )

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(
            padx=Settings.OPTIONS_WIDGETS_PADX * 2,
            pady=Settings.OPTIONS_WIDGETS_PADY * 2,
            fill=tk.X,
            expand=True,
        )

        version = "{}: {}".format(_("Version"), arrangeit.__version__)
        tk.Label(self, text=version, anchor="w").pack(
            padx=Settings.OPTIONS_WIDGETS_PADX * 2, fill=tk.X, side=tk.TOP
        )
        python = "Python {}: {}".format(_("version"), platform.python_version())
        tk.Label(self, text=python, anchor="w").pack(
            padx=Settings.OPTIONS_WIDGETS_PADX * 2, fill=tk.X, side=tk.TOP
        )
        tcl_tk = "Tcl/Tk {}: {}".format(_("version"), tk.TkVersion)
        tk.Label(self, text=tcl_tk, anchor="w").pack(
            padx=Settings.OPTIONS_WIDGETS_PADX * 2, fill=tk.X, side=tk.TOP
        )
        system = "OS: {}".format(platform.platform())
        tk.Label(self, text=system, anchor="w").pack(
            padx=Settings.OPTIONS_WIDGETS_PADX * 2, fill=tk.X, side=tk.TOP
        )
        gui = "GUI: {}".format(
            self.master.master.tk.call("winfo", "server", self.master.master._w)
        )
        tk.Label(self, text=gui, anchor="w").pack(
            padx=Settings.OPTIONS_WIDGETS_PADX * 2, fill=tk.X, side=tk.TOP
        )

        tk.Button(
            self,
            text=_("Exit"),
            activeforeground=Settings.HIGHLIGHTED_COLOR,
            command=self.destroy,
        ).pack(
            padx=Settings.OPTIONS_WIDGETS_PADX,
            pady=Settings.OPTIONS_WIDGETS_PADY * 2,
            anchor="se",
            side=tk.RIGHT,
        )
        tk.Button(
            self,
            text=_("Releases"),
            activeforeground=Settings.HIGHLIGHTED_COLOR,
            command=self.on_releases_click,
        ).pack(
            padx=Settings.OPTIONS_WIDGETS_PADX,
            pady=Settings.OPTIONS_WIDGETS_PADY * 2,
            anchor="se",
            side=tk.RIGHT,
        )
        tk.Button(
            self,
            text=_("Online help"),
            activeforeground=Settings.HIGHLIGHTED_COLOR,
            command=self.on_help_click,
        ).pack(
            padx=Settings.OPTIONS_WIDGETS_PADX,
            pady=Settings.OPTIONS_WIDGETS_PADY * 2,
            anchor="se",
            side=tk.RIGHT,
        )

    def on_help_click(self):
        """Opens documentation page in user's default web browser."""
        webbrowser.open(Settings.HELP_PAGE_URL, new=2)

    def on_releases_click(self):
        """Opens download releases page in user's default web browser."""
        webbrowser.open(Settings.RELEASES_PAGE_URL, new=2)
