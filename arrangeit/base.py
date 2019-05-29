import os
import json
from gettext import gettext as _

from arrangeit.settings import Settings
from arrangeit.data import WindowModel, WindowsCollection
from arrangeit.utils import (
    get_component_class,
    quarter_by_smaller,
    platform_user_data_path,
)
from arrangeit.view import (
    click_left,
    get_mouse_listener,
    get_tkinter_root,
    get_screenshot_widget,
    move_cursor,
    ViewApplication,
)


class BaseApp(object):
    """Base App class holding common code for all the platforms.

    :var BaseApp.controller: object that connects data and presentation
    :type BaseApp.controller: type(:class:`BaseController`) instance (platform specific)
    :var BaseApp.collector: object responsible for collecting windows data
    :type BaseApp.collector: type(:class:`BaseCollector`) instance (platform specific)
    """

    controller = None
    collector = None

    def __init__(self, *args, **kwargs):
        """Instantiates platform specific Controller and Collector classes."""
        self.controller = self.setup_controller()(self)
        self.collector = self.setup_collector()()

    def setup_controller(self):
        """Returns platform specific Controller class."""
        return get_component_class("Controller")

    def setup_collector(self):
        """Returns platform specific Collector class."""
        return get_component_class("Collector")

    def run(self):
        """Collects data, prepare them for view and finally shows view application."""
        self.collector.run()
        self.controller.run(self.collector.collection.generator())

    def run_task(self, task, *args):
        """Runs provided task with provided args

        :param task: task name
        :type task: str
        """
        return getattr(self, task)(*args)

    def grab_window_screen(self, model):
        """Method must be overridden."""
        raise NotImplementedError

    def move_and_resize(self, *args):
        """Method must be overridden."""
        raise NotImplementedError

    def move(self, *args):
        """Method must be overridden."""
        raise NotImplementedError

    def move_to_workspace(self, *args):
        """Method must be overridden."""
        raise NotImplementedError

    def rerun_from_window(self, wid, remove_before):
        """Restart positioning routine from the window with provided wid

        without already positioned/skipped windows.

        :param wid: windows identifier
        :type wid: int
        """
        self.collector.collection.repopulate_for_wid(wid, remove_before)

    def save_default(self, *args):
        """Saves collection to default filename in user's directory.

        Creates application's user data directory if it not exists.
        """
        print(_("Finished: saving to default file"))
        directory = platform_user_data_path()
        if not os.path.exists(directory):
            os.mkdir(directory)

        with open(os.path.join(directory, "default.json"), "w") as default:
            json.dump(self.collector.collection.export(), default)


class BaseController(object):
    """Base Controller class holding common code for all the platforms.

    :var BaseController.app: platform specific parent app
    :type BaseController.app: type(:class:`BaseApp`) instance
    :var model: model holding window data
    :type model: :class:`WindowModel` instance
    :var BaseController.generator: generator for retrieving model instances from collection
    :type BaseController.generator: Generator[WindowModel, None, None]
    :var BaseController.view: Tkinter application showing main window
    :type BaseController.view: :class:`ViewApplication` instance
    :var listener: Tkinter application showing main window
    :type listener: :class:`ViewApplication` instance
    :var state: controller's state (LOCATE, RESIZE or OTHER)
    :type state: int
    :var screenshot_widget: widget holding background image
    :type screenshot_widget: :class:`tk.Label`
    :var screenshot: screenshot image of the window model
    :type screenshot: :class:`tk.PhotoImage`
    """

    app = None
    model = None
    generator = None
    view = None
    listener = None
    state = None
    screenshot_widget = None
    screenshot = None

    def __init__(self, app):
        """Sets app attribute to provided argument, model attribute to new empty model

        and calls :func:`BaseController.setup`.
        """
        self.app = app
        self.model = WindowModel()
        self.setup()

    ## CONFIGURATION
    def setup(self):
        """Initializes Tkinter ViewApplication with root window and self as arguments.

        Creates and place screenshot widget below view frame, used to hold window image.
        Sets view attribute to newly created Tkinter application.
        Prevents root window to show by calling its `withdraw` method.
        Tkinter root window from now may be accessed by `[self].view.master` attribute.
        """
        root = get_tkinter_root()
        self.setup_root_window(root)
        self.screenshot_widget = get_screenshot_widget(root)
        self.view = ViewApplication(master=root, controller=self)
        root.withdraw()

    def setup_root_window(self, root):
        """Sets provided root window appearance common for all platforms.

        :param root: root tkinter window
        :type root: :class:`tkinter.Tk` instance
        """
        root.wm_attributes("-alpha", Settings.ROOT_ALPHA)
        root.wm_attributes("-topmost", True)

    def set_default_geometry(self, root):
        """Sets provided root window width and height

        calculated from available width and height for screen as quarter of
        the smaller element. Returned width and height have 16:9 aspect ratio.

        :param root: root tkinter window
        :type root: :class:`tkinter.Tk` instance
        :var width: root width in pixels
        :type width: int
        :var height: root height in pixels
        :type height: int
        """
        width, height = quarter_by_smaller(
            root.winfo_screenwidth(), root.winfo_screenheight()
        )
        root.geometry("{}x{}".format(width, height))

    def prepare_view(self):
        """Populates view's workspaces and windows list widgets.

        Very first window is our main window so we skip it in listing.
        """
        self.view.workspaces.add_workspaces(
            self.app.collector.get_available_workspaces()
        )
        self.view.windows.add_windows(
            self.app.collector.collection.get_windows_list()[1:]
        )

    def set_screenshot(self):
        """Creates and places screenshot of model window as background image.

        If we can't include window decoration in image then offset is returned
        and we place image shifted by offset amount of pixels to related axis.

        :var offset: offset (x, y)
        :type offset: (int, int)
        """
        self.screenshot, offset = self.app.grab_window_screen(self.model)
        self.screenshot_widget.configure(image=self.screenshot)
        self.screenshot_widget.place(
            x=offset[0] + Settings.SCREENSHOT_SHIFT_PIXELS,
            y=offset[1] + Settings.SCREENSHOT_SHIFT_PIXELS,
        )

    ## DOMAIN LOGIC
    def run(self, generator):
        """Prepares view, syncs data, starts listener and enters main loop.

        Calls `prepare_view` to create workspaces and windows list widgets.
        Sets generator attribute to provided generator and sets window data
        by calling :func:`BaseController.next` for the first time.
        Calls view application startup routine to show root and calculate
        visible parameters.
        Calls `click_left` and so activates Tkinter root window.
        """
        self.prepare_view()

        self.generator = generator
        self.next(first_time=True)

        self.listener = get_mouse_listener(self.on_mouse_move)
        self.listener.start()

        self.view.startup()

        click_left()  # TODO try with Wnck.Window.activate on GNU/Linux instead

        self.mainloop()

    def next(self, first_time=False):
        """Sets controller ``model`` attribute from the value yielded from ``generator``

        and populates view widgets with new model data.
        Also changes and moves cursor and root window to model's window position.
        Grabs and sets screenshot image of the model's window.
        If there are no values left in collection then saves and exits app.
        Switches workspace if it's changed.

        :var old_workspace: old model's workspace number
        :type old_workspace: ind
        :var first_time: is method called for the very first time
        :type first_time: Boolean
        :returns: Boolean
        """
        old_workspace = self.model.changed_ws or self.model.workspace
        try:
            self.model = next(self.generator)
        except StopIteration:
            self.app.run_task("save_default")
            self.shutdown()
            return True

        if not first_time:
            self.state = Settings.LOCATE  # we need state to be None during startup
            self.remove_listed_window(self.model.wid)
            if self.model.workspace != old_workspace:
                self.switch_workspace()

        self.set_screenshot()
        self.set_default_geometry(self.view.master)
        self.place_on_top_left()

        self.view.update_widgets(self.model)

        return False

    def update(self, x, y):
        """Calls corresponding state related update method.

        Sets state to LOCATE if this is the very first call to this method.

        :param x: current horizontal axis mouse position in pixels
        :type x: int
        :param y: current vertical axis mouse position in pixels
        :type y: int
        """
        if self.state is None:
            self.state = Settings.LOCATE

        elif self.state == Settings.LOCATE:
            return self.update_positioning(x, y)

        elif self.state == Settings.RESIZE:
            return self.update_resizing(x, y)

    def update_positioning(self, x, y):
        """Updates model with provided cursor position in LOCATE state

        and takes action in regard to model type.

        :param x: current horizontal axis mouse position in pixels
        :type x: int
        :param y: current vertical axis mouse position in pixels
        :type y: int
        """
        self.model.set_changed(x=x, y=y)
        if not self.model.resizable:
            if self.model.changed or self.model.is_ws_changed:
                self.app.run_task("move", self.model.wid)
            self.next()
        else:
            self.state = Settings.RESIZE
            self.place_on_right_bottom()

    def update_resizing(self, x, y):
        """Updates model with provided cursor position in RESIZE state

        and calls move and resize task if window has changed.
        Switches to next model anyway.

        :param x: current horizontal axis mouse position in pixels
        :type x: int
        :param y: current vertical axis mouse position in pixels
        :type y: int
        """
        w, h = self.model.wh_from_ending_xy(x, y)
        self.model.set_changed(w=w, h=h)
        if self.model.changed or self.model.is_ws_changed:
            self.app.run_task("move_and_resize", self.model.wid)
        self.next()

    def listed_window_activated(self, wid):
        """Calls task that restarts positioning routine from provided window id

        not including windows prior to current model.

        :param wid: windows identifier
        :type wid: int
        """
        self.app.run_task("rerun_from_window", wid, self.model.wid)
        self.view.windows.clear_list()
        self.view.windows.add_windows(
            self.app.collector.collection.get_windows_list()[1:]
        )
        if self.state == Settings.OTHER:
            self.recapture_mouse()
        self.generator = self.app.collector.collection.generator()
        self.next(first_time=True)

    def workspace_activated(self, number):
        """Activates workspace with number equal to provided number.

        :param number: our custom workspace number (screen*1000 + workspace)
        :type number: int
        """
        self.app.run_task("move_to_workspace", self.view.master.winfo_id(), number)
        self.model.set_changed(ws=number)
        if self.state == Settings.OTHER:
            self.recapture_mouse()

    ## COMMANDS
    def change_position(self, x, y):
        """Changes root window position to provided x and y.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        self.view.master.geometry("+{}+{}".format(x, y))

    def change_size(self, x, y):
        """Changes root window size in regard to provided bottom left x and y

        related to model.changed's x and y.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        if (
            x > self.model.changed_x + Settings.WINDOW_MIN_WIDTH
            and y > self.model.changed_y + Settings.WINDOW_MIN_HEIGHT
        ):
            self.view.master.geometry(
                "{}x{}".format(
                    x - self.model.changed_x + Settings.WINDOW_SHIFT_PIXELS,
                    y - self.model.changed_y + Settings.WINDOW_SHIFT_PIXELS,
                )
            )
        else:
            self.view.master.geometry(
                "{}x{}".format(Settings.WINDOW_MIN_WIDTH, Settings.WINDOW_MIN_HEIGHT)
            )

    def listed_window_activated_by_digit(self, number):
        """Activates listed window by its ordinal in list presented by provided number.

        :param number: number of 1 to 16 representing ordinal in list
        :type number: int
        :var windows: available workspaces in view
        :type windows: :class:`WorkspacesCollection`
        """
        windows = self.view.windows.winfo_children()
        if len(windows) >= number:
            self.listed_window_activated(windows[number - 1].wid)

    def place_on_top_left(self):
        """Changes and moves cursor to model's top left position.

        Cursor is changed to default config. Also calls `on_mouse_move` to force
        moving if the app is just instantiated.
        """
        self.view.master.config(cursor="ul_angle")
        move_cursor(self.model.x, self.model.y)
        self.on_mouse_move(self.model.x, self.model.y)

    def place_on_right_bottom(self):
        """Changes and moves cursor to model's bottom right position

        and so indirectly resizes master. Cursor is changed to resize config.
        """
        self.view.master.config(cursor="lr_angle")
        move_cursor(
            self.model.changed_x + self.model.w, self.model.changed_y + self.model.h
        )

    def remove_listed_window(self, wid):
        """Destroys window widget from windows list and refreshes the list afterward.

        :param wid: id of window that will be destroyed
        :type wid: int
        """
        try:
            next(
                widget
                for widget in self.view.windows.winfo_children()
                if widget.wid == wid
            ).destroy()
        except StopIteration:
            pass
        self.view.windows.place_children()

    def release_mouse(self):
        """Stops positioning/resizing routine and releases mouse."""
        self.view.unbind_events()
        self.view.master.config(cursor="left_ptr")
        self.state = Settings.OTHER
        self.listener.stop()

    def recapture_mouse(self):
        """Creates and starts mouse listener and starts positioning/resizing routine."""
        self.view.setup_bindings()
        self.view.master.config(cursor="ul_angle")
        self.state = Settings.LOCATE
        move_cursor(self.view.master.winfo_x(), self.view.master.winfo_y())
        self.listener = get_mouse_listener(self.on_mouse_move)
        self.listener.start()

    def shutdown(self):
        """Stops mouse listener and destroys Tkinter root window."""
        self.listener.stop()
        self.view.master.destroy()

    def skip_current_window(self):
        """Calls `next` and then destroys that new window from the windows list."""
        self.next()

    def switch_workspace(self):
        """Activates workspace and moves root window onto it."""
        self.app.run_task(
            "move_to_workspace", self.view.master.winfo_id(), self.model.workspace
        )

    def workspace_activated_by_digit(self, number):
        """Activates workspace with humanized number equal to provided number.

        :param number: number of 1 to 9 representing workspace
        :type number: int
        :var workspaces: available workspaces in view
        :type workspaces: :class:`WorkspacesCollection`
        """
        workspaces = self.view.workspaces.winfo_children()
        if len(workspaces) >= number:
            self.workspace_activated(workspaces[number - 1].number)

    ## EVENTS CALLBACKS
    def on_key_pressed(self, event):
        """Calls method related to pressed key.

        :param event: catched event
        :type event: Tkinter event
        """
        if event.keysym in ("Escape",):
            self.shutdown()

        elif event.keysym in ("Return", "KP_Enter"):
            self.update(
                self.view.master.winfo_pointerx(), self.view.master.winfo_pointery()
            )

        elif event.keysym in ("Space", "Tab"):
            self.skip_current_window()

        elif event.keysym in ("Control_L",):
            self.release_mouse()

        elif event.keysym in [str(i) for i in range(1, 10)]:
            self.workspace_activated_by_digit(int(event.keysym))

        elif event.keysym in ["KP_{}".format(i) for i in range(1, 10)]:
            self.workspace_activated_by_digit(int(event.keysym[-1]))

        elif event.keysym in ["F{}".format(i) for i in range(1, 17)]:
            self.listed_window_activated_by_digit(int(event.keysym[1:]))

        return "break"

    def on_mouse_move(self, x, y):
        """Moves root Tkinter window to provided mouse coordinates.

        Adds negative Settings.WINDOW_SHIFT_PIXELS to mouse position for better presentation.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        if self.state in (None, Settings.LOCATE):
            self.change_position(x, y)

        elif self.state == Settings.RESIZE:
            self.change_size(x, y)

    def on_mouse_left_down(self, event):
        """Calls :class:`BaseController.update` with current cursor position

        :param event: catched event
        :type event: Tkinter event
        """
        self.update(
            self.view.master.winfo_pointerx(), self.view.master.winfo_pointery()
        )
        return "break"

    def on_mouse_middle_down(self, event):
        """Switches to third state.

        :param event: catched event
        :type event: Tkinter event
        """
        self.release_mouse()
        return "break"

    def on_mouse_right_down(self, event):
        """Skips the current model.

        :param event: catched event
        :type event: Tkinter event
        """
        self.skip_current_window()
        return "break"

    ## MAIN LOOP
    def mainloop(self):
        self.view.mainloop()


class BaseCollector(object):
    """Base Collector class holding common code for all the platforms.

    :var collection: collection of :class:`WindowModel` instances
    :type collection: :class:`WindowsCollection` instance
    """

    collection = None

    def __init__(self):
        """Initiates ``collection`` as empty :class:`WindowsCollection` instance."""
        self.collection = WindowsCollection()

    def is_applicable(self, window_type):
        """Method must be overridden."""
        raise NotImplementedError

    def is_valid_state(self, window_type, window_state):
        """Method must be overridden."""
        raise NotImplementedError

    def is_resizable(self, window_type):
        """Method must be overridden."""
        raise NotImplementedError

    def get_windows(self):
        """Method must be overridden."""
        raise NotImplementedError

    def check_window(self, win):
        """Method must be overridden."""
        raise NotImplementedError

    def add_window(self, win):
        """Method must be overridden."""
        raise NotImplementedError

    def get_workspace_number(self, workspace):
        """Method must be overridden."""
        raise NotImplementedError

    def get_workspace_number_for_window(self, win):
        """Method must be overridden."""
        raise NotImplementedError

    def get_available_workspaces(self):
        """Method must be overridden."""
        raise NotImplementedError

    def run(self):
        """Populates ``collection`` with WindowModel instances

        created from the windows list provided by :func:`get_windows`
        after they are checked for compliance with :func:`check_window`
        by calling :func:`add_window`.

        :var win: current window instance/handle in the loop
        :type win: platform specific window object or handle (Wnck.Window, hwnd, ...)
        """
        for win in self.get_windows():
            if self.check_window(win):
                self.add_window(win)
        win = None
        self.collection.sort()
