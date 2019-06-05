import tkinter as tk
from gettext import gettext as _


MESSAGES = {
    "options_title": _("arrangeit options"),
    "setting_changed": _(
        "Setting is changed, please restart program in order for the change to take effect."
    ),
}


OPTIONS = {"HIGHLIGHTED_COLOR": (str, "red")}


class OptionsMetaclass(type):
    """Meta class needed to access Options class attributes by names."""

    def __getattr__(self, name):
        """Returns value for provided attribute name."""
        return OPTIONS.get(name, [None, None])[1]


class Options(metaclass=OptionsMetaclass):
    """Class holding all the program's constants and Options."""

    COLORS = (
        "white",
        "light blue",
        "blue",
        "royal blue",
        "cyan",
        "khaki",
        "slate gray",
        "gray",
        "orange",
        "salmon",
        "indian red",
        "red",
        "orchid",
        "pink",
        "green",
        "olive drab",
        "wheat",
        "tan",
        "yellow",
    )


class OptionsDialog(tk.Toplevel):
    """Tkinter dialog window for manipulating of user configuration data.

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
        # self.title(MESSAGES["options_title"])
        self.geometry(
            "+{}+{}".format(self.master.master.winfo_x(), self.master.master.winfo_y())
        )

    def setup_bindings(self):
        """Binds relevant events to related callback."""
        self.bind("<Destroy>", self.on_destroy_options)

    def setup_widgets(self):
        """Creates and places all the options' widgets."""
        self.message = tk.Label(self, text="", anchor="center")
        self.message.pack()

        #         "SNAPPING_IS_ON": tk.IntVar(),
        #         "SCREENSHOT_TO_GRAYSCALE": tk.IntVar(),

        quit_button = tk.Button(
            self,
            text=_("Cancel"),
            activeforeground=Options.HIGHLIGHTED_COLOR,
            command=self.destroy,
        )
        quit_button.pack()

    def on_destroy_options(self, event):
        """Brings back root window and destroys options dialog."""
        self.master.master.update()
        self.master.master.deiconify()
        self.destroy()

    def change_setting(self, name="", value=None):
        self.master.controller.app.run_task("change_setting", name, value)
        self.message.config(text=MESSAGES["setting_changed"])


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
        self.master.change_setting(name=self.name, value=value)
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

    def __init__(self, master=None, name="", initial=False, text=""):
        """Sets master attribute and configs check button widget from provided arguments

        after super __init__ is called.

        Also sets command callback.

        :param master: parent widget
        :param master: :class:`.tk.Toplevel`
        :param name: settings name to change
        :param name: str
        :param initial: starting value
        :param initial: bool
        :param text: explanation text for this check button
        :param text: str
        """
        super().__init__(master)
        self.master = master
        self.name = name
        self.var = tk.IntVar()
        self.config(text=text, variable=self.var, command=self.on_update_value)
        self.select() if initial else self.deselect()

    def on_update_value(self, *args):
        self.master.change_setting(name=self.name, value=bool(self.var.get()))
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

    def __init__(self, master=None, name="", initial="", choices=()):
        """Sets master attribute and configs choice widget from provided arguments

        after super __init__ is called.

        Also sets command callback.

        :param master: parent widget
        :param master: :class:`.tk.Toplevel`
        :param name: settings name to change
        :param name: str
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

    def on_update_value(self, *args):
        self.master.change_setting(name=self.name, value=self.var.get())
        return "break"
