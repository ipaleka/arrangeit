import tkinter as tk
import tkinter.ttk as ttk
from gettext import gettext as _

from arrangeit import options
from arrangeit.settings import Settings


MESSAGES = {
    "options_title": _("arrangeit options"),
    "appearance": _("Appearance"),
    "TRANSPARENCY_IS_ON": _("Transparent window"),
    "ROOT_ALPHA": _("Main window transparency"),
    "SCREENSHOT_TO_GRAYSCALE": _("Convert screenshot to grayscale"),
    "SCREENSHOT_BLUR_PIXELS": _("Blur size in pixels"),
    "SNAPPING_IS_ON": _("Windows snapping"),
    "SNAP_INCLUDE_SELF": _("Include itself in snapping"),
    "SHIFT_CURSOR": _("Cursor shift from a corner in pixels"),
    # "SNAPPING_IS_ON": _(""),
    "SNAP_PIXELS": _("Snapping size in pixels"),
    "MAIN_BG": _("Background color"),
    "setting_changed": _(
        "Setting is changed, please restart program in order for the change to take effect."
    ),
}

OPTIONS = {"HIGHLIGHTED_COLOR": (str, "red")}

WIDGETS = {
    "appearance": (
        ("TRANSPARENCY_IS_ON", {}),
        (
            "ROOT_ALPHA",
            {"from_": 50, "to": 99, "resolution": 5, "tickinterval": 20, "digits": 3},
        ),
        ("SCREENSHOT_TO_GRAYSCALE", {}),
        (
            "SCREENSHOT_BLUR_PIXELS",
            {"from_": 0, "to": 8, "resolution": 1, "tickinterval": 2, "digits": 1},
        ),
        ("SNAPPING_IS_ON", {}),
        (
            "SNAP_PIXELS",
            {"from_": 1, "to": 12, "resolution": 1, "tickinterval": 3, "digits": 1},
        ),
        ("SNAP_INCLUDE_SELF", {}),
        (
            "SHIFT_CURSOR",
            {"from_": 1, "to": 15, "resolution": 1, "tickinterval": 3, "digits": 1},
        ),
    )
}


class OptionsMetaclass(type):
    """Meta class needed to access Options class attributes by names."""

    def __getattr__(self, name):
        """Returns value for provided attribute name."""
        return OPTIONS.get(name, [None, None])[1]


class Options(metaclass=OptionsMetaclass):
    """Class holding all the program's constants and Options."""

    COLORS = (
        "white",
        "gray",
        "slate gray",
        "gray25",
        "gray75",
        "light blue",
        "blue",
        "royal blue",
        "cyan",
        "orange",
        "salmon",
        "indian red",
        "red",
        "orchid",
        "pink",
        "green",
        "olive drab",
        "wheat",
        "khaki",
        "tan",
        "yellow",
    )


class OptionsDialog(tk.Toplevel):
    """Tkinter dialog window for manipulating of user settings data.

    :var OptionsDialog.master: master widget
    :type OptionsDialog.master: :class:`.tk.Tk`
    """

    master = None

    def __init__(self, master=None):
        """Sets master attribute, position dialog on former master position

        and call setup routines after super __init__ is called.
        """
        super().__init__(master)
        self.master = master
        self.setup_widgets()
        self.setup_bindings()
        self.title(MESSAGES["options_title"])
        self.geometry(
            "+{}+{}".format(self.master.master.winfo_x(), self.master.master.winfo_y())
        )

    def setup_bindings(self):
        """Binds relevant events to related callback."""
        self.bind("<Destroy>", self.on_destroy_options)

    def widget_class_from_name(self, name):
        """Returns related widget class from provided setting name.

        :param name: setting name
        :type name: str
        :returns: custom Tkinter widget instance
        """
        typ = "Scale"
        if Settings.setting_type(name) == bool:
            typ = "Check"
        elif Settings.setting_type(name) == str:
            typ = "Choice"
        return getattr(options, "{}Option".format(typ))

    def create_widget(self, master, name, **kwargs):
        """Creates widget with provided master for setting with provided name.

        :param master: parent widget
        :type master: :class:`ttk.LabelFrame`
        :param name: setting name
        :type name: str
        """
        widget_class = self.widget_class_from_name(name)
        initial = getattr(Settings, name)
        widget = widget_class(
            master,
            name=name,
            change_callback=self.change_setting,
            initial=int(initial * 100)
            if Settings.setting_type(name) == float
            else initial,
            text=MESSAGES[name],
            **kwargs
        )
        widget.pack(fill=tk.X, side=tk.TOP)
        return widget

    def frame_placeholder(self, master):
        """Returns frame that will holds pair of widgets."""
        frame = tk.Frame(master)
        frame.pack(fill=tk.X, side=tk.LEFT, expand=True)
        return frame

    def setup_appearance(self):
        """Creates and places widgets related to program appearance."""
        appearance = ttk.LabelFrame(self, text="Appearance")
        appearance.pack(fill=tk.BOTH, expand=True)

        for i, (name, kwargs) in enumerate(WIDGETS["appearance"]):
            if not i % 4:
                frame = self.frame_placeholder(appearance)
            self.create_widget(frame, name, **kwargs)

        return appearance

    def setup_widgets(self):
        """Creates and places all the options' widgets."""
        self.message = tk.StringVar()

        self.setup_appearance()

        message = tk.Label(self, textvariable=self.message, anchor="center")
        message.pack()

        quit_button = tk.Button(
            self,
            text=_("Continue"),
            activeforeground=Options.HIGHLIGHTED_COLOR,
            command=self.destroy,
        )
        quit_button.pack()

    def on_destroy_options(self, event):
        """Brings back root window and destroys options dialog."""
        self.master.show_root()
        self.destroy()

    def change_setting(self, name="", value=None):
        """Calls sontroller's change setting method and updates message log.

        :param name: setting name
        :type name: str
        :param value: value for given name setting
        :type name: str/int/float
        """
        self.master.controller.change_setting(
            name,
            float(value) / 100.0 if Settings.setting_type(name) == float else value,
        )
        self.message.set(MESSAGES["setting_changed"])


class ScaleOption(tk.Scale):
    """Tkinter widget for showing and changing range settings values.

    :var ScaleOption.master: master widget
    :type ScaleOption.master: :class:`.tk.Toplevel`
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
        initial=0.0,
        text="",
        from_=0.0,
        to=1.0,
        resolution=0.05,
        tickinterval=0.2,
        digits=3,
    ):
        """Sets master attribute and configs scale widget from provided arguments

        after super __init__ is called.

        Also sets command callback and orientation.

        :param master: parent widget
        :param master: :class:`.tk.Toplevel`
        :param name: settings name to change
        :param name: str
        :param change_callback: callback method to call on value change
        :param change_callback: method
        :param initial: starting value
        :param initial: float/int
        :param text: explanation text/label for this scale
        :param text: str
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
            label=text,
            from_=from_,
            to=to,
            resolution=resolution,
            tickinterval=tickinterval,
            digits=digits,
            orient=tk.HORIZONTAL,
            command=self.on_update_value,
        )
        self.set(initial)

    def on_update_value(self, value):
        self.change_callback(name=self.name, value=value)
        return "break"


class CheckOption(tk.Checkbutton):
    """Tkinter widget for showing and changing Boolean values.

    :var CheckOption.master: master widget
    :type CheckOption.master: :class:`.tk.Toplevel`
    :var CheckOption.name: setting name to change
    :type CheckOption.name: str
    :var CheckOption.var: variable holding the check button value
    :type CheckOption.var: :class:`tk.IntVar`
    """

    master = None
    name = ""
    var = None

    def __init__(
        self, master=None, name="", change_callback=None, initial=False, text=""
    ):
        """Sets master attribute and configs check button widget from provided arguments

        after super __init__ is called.

        Also sets command callback.

        :param master: parent widget
        :param master: :class:`.tk.Toplevel`
        :param name: settings name to change
        :param name: str
        :param change_callback: callback method to call on value change
        :param change_callback: method
        :param initial: starting value
        :param initial: bool
        :param text: explanation text for this check button
        :param text: str
        """
        super().__init__(master)
        self.master = master
        self.name = name
        self.change_callback = change_callback
        self.var = tk.IntVar()
        self.config(text=text, variable=self.var, command=self.on_update_value)
        self.select() if initial else self.deselect()

    def on_update_value(self, *args):
        self.change_callback(name=self.name, value=bool(self.var.get()))
        return "break"


class ChoiceOption(tk.OptionMenu):
    """Tkinter widget for showing and changing Boolean values.

    :var ChoiceOption.master: master widget
    :type ChoiceOption.master: :class:`.tk.Toplevel`
    :var ChoiceOption.name: setting name to change
    :type ChoiceOption.name: str
    :var ChoiceOption.var: variable holding the choice value
    :type ChoiceOption.var: :class:`tk.StringVar`
    """

    master = None
    name = ""
    var = None

    def __init__(
        self, master=None, name="", change_callback=None, initial="", choices=()
    ):
        """Sets master attribute and configs choice widget from provided arguments

        after super __init__ is called.

        Also sets command callback.

        :param master: parent widget
        :param master: :class:`.tk.Toplevel`
        :param name: settings name to change
        :param name: str
        :param change_callback: callback method to call on value change
        :param change_callback: method
        :param initial: starting value
        :param initial: str
        :param choices: collection of available text values
        :param choices: tuple
        """
        self.var = tk.StringVar()
        self.var.set(initial)
        super().__init__(master, self.var, *choices, command=self.on_update_value)
        self.master = master
        self.name = name
        self.change_callback = change_callback

    def on_update_value(self, *args):
        self.change_callback(name=self.name, value=self.var.get())
        return "break"
