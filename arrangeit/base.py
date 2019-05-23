import asyncio
import threading
from inspect import iscoroutinefunction

from arrangeit import constants
from arrangeit.data import WindowModel, WindowsCollection
from arrangeit.utils import get_component_class, quarter_by_smaller
from arrangeit.view import (
    click_left,
    get_mouse_listener,
    get_tkinter_root,
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
        """Runs provided task with provided args asynchronously in separate thread.

        :param task: task name
        :type task: str
        """
        self.run_in_separate_thread(task, *args)

    def run_in_separate_thread(self, task, *args):
        """Initializes and starts a new Thread instance with `run_asynchronously` target

        callback and provided task name and args as arguments.

        :param task: task name
        :type task: str
        """
        threading.Thread(target=self.run_asynchronously, args=(task, *args)).start()

    def run_asynchronously(self, task, *args):
        """Executes asynchronous callback having provided name with provided args

        in a newly created asyncio event loop if such callback exists.

        :param task: task name
        :type task: str
        :var callback: callback having name of the `task` argument
        :type callback: async type(:class:`BaseApp`) method
        """
        callback = getattr(self, task, None)
        if iscoroutinefunction(callback):
            asyncio.new_event_loop().run_until_complete(callback(*args))

    async def save_default(self, *args):
        await asyncio.sleep(0.1)
        print("finished: save_default with args ", args)

    async def move_and_resize(self, *args):
        """Method must be overridden."""
        raise NotImplementedError

    async def move(self, *args):
        """Method must be overridden."""
        raise NotImplementedError


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
    """

    app = None
    model = None
    generator = None
    view = None
    listener = None
    state = None

    def __init__(self, app):
        """Sets app attribute to provided argument, model attribute to new empty model

        and calls :func:`BaseController.setup`.
        """
        self.app = app
        self.model = WindowModel()
        self.setup()

    def setup(self):
        """Initializes Tkinter ViewApplication with root window and self as arguments.

        Sets view attribute to newly created Tkinter application.
        Prevents root window to show by calling its `withdraw` method.
        Tkinter root window from now may be accessed by `[self].view.master` attribute.
        """
        root = get_tkinter_root()
        self.setup_root_window(root)
        self.view = ViewApplication(master=root, controller=self)
        root.withdraw()

    def setup_root_window(self, root):
        """Sets provided root window appearance common for all platforms.

        :param root: root tkinter window
        :type root: :class:`tkinter.Tk` instance
        """
        root.wm_attributes("-alpha", constants.ROOT_ALPHA)
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
        """Populates view's workspaces and windows list widgets."""
        self.view.workspaces.add_workspaces(
            self.app.collector.get_available_workspaces()
        )
        self.view.windows.add_windows(self.app.collector.collection.get_windows_list())

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

        click_left()

        self.mainloop()

    def next(self, first_time=False):
        """Sets controller ``model`` attribute from the value yielded from ``generator``

        and populates view widgets with new model data.
        Also changes and moves cursor and root window to model's window position.
        If there are no values left in collection then saves and exits app.

        :param first_time: is method called for the very first time
        :type first_time: Boolean
        :returns: Boolean
        """
        try:
            self.model = next(self.generator)
        except StopIteration:
            self.app.run_task("save_default")
            self.shutdown()
            return True

        if not first_time:  # we need state to be None in startup
            self.state = constants.LOCATE
        self.set_default_geometry(self.view.master)
        self.place_on_top_left()

        self.view.update_widgets(self.model)

        return False

    def update(self, x, y):
        """Updates model with provided cursor position in regard to state

        and takes action in regard to state and model type.
        As we call `click_left` under `run`, so this method is called upon start
        when state has value of None - we set it to constants.LOCATE right here.

        NOTE this method probably needs refactoring

        :var x: current horizontal axis mouse position in pixels
        :type x: int
        :var y: current vertical axis mouse position in pixels
        :type y: int
        """
        if self.state is None:
            self.state = constants.LOCATE

        elif self.state == constants.LOCATE:
            self.model.set_changed(x=x, y=y)
            if not self.model.resizable:
                self.remove_window(self.model.wid)
                self.app.run_task("move", self.model.wid)
                self.next()
            else:
                self.state = constants.RESIZE
                self.place_on_right_bottom()

        elif self.state == constants.RESIZE:
            w, h = self.model.wh_from_ending_xy(x, y)
            self.model.set_changed(w=w, h=h)
            self.remove_window(self.model.wid)
            if self.model.changed:  # could be ()
                self.app.run_task("move_and_resize", self.model.wid)
            self.next()

    def skip_current_window(self):
        """Calls `next` and then destroys that new window from the windows list."""
        if not self.next():
            self.remove_window(self.model.wid)

    def workspace_activated(self, number):
        """"""
        pass

    def window_activated(self, wid):
        """"""
        pass

    def remove_window(self, wid):
        """Destroys window widget from windows list.

        :var wid: id of window that will be destroyed
        :type wid: int
        """
        for widget in self.view.windows.winfo_children():
            if widget.wid == wid:
                widget.destroy()
                break

    def place_on_top_left(self):
        """Changes and moves cursor to model's top left position.

        NOTE for released cursor 'left_ptr'
        http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/cursors.html

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
            self.model.changed[0] + self.model.w, self.model.changed[1] + self.model.h
        )

    def change_position(self, x, y):
        """Changes root window position to provided x and y.

        :var x: absolute horizontal axis mouse position in pixels
        :type x: int
        :var y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        self.view.master.geometry(
            "+{}+{}".format(
                x - constants.WINDOW_SHIFT_PIXELS, y - constants.WINDOW_SHIFT_PIXELS
            )
        )

    def change_size(self, x, y):
        """Changes root window size in regard to provided bottom left x and y

        related to model.changed's x and y.

        :var x: absolute horizontal axis mouse position in pixels
        :type x: int
        :var y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        if (
            x > self.model.changed[0] + constants.WINDOW_MIN_WIDTH
            and y > self.model.changed[1] + constants.WINDOW_MIN_HEIGHT
        ):
            self.view.master.geometry(
                "{}x{}".format(
                    x - self.model.changed[0] + constants.WINDOW_SHIFT_PIXELS * 2,
                    y - self.model.changed[1] + constants.WINDOW_SHIFT_PIXELS * 2,
                )
            )
        else:
            self.view.master.geometry(
                "{}x{}".format(
                    constants.WINDOW_MIN_WIDTH + constants.WINDOW_SHIFT_PIXELS * 2,
                    constants.WINDOW_MIN_HEIGHT + constants.WINDOW_SHIFT_PIXELS * 2,
                )
            )

    def on_mouse_move(self, x, y):
        """Moves root Tkinter window to provided mouse coordinates.

        Adds negative constants.WINDOW_SHIFT_PIXELS to mouse position for better presentation.

        :var x: absolute horizontal axis mouse position in pixels
        :type x: int
        :var y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        if self.state in (None, constants.LOCATE):
            self.change_position(x, y)

        elif self.state == constants.RESIZE:
            self.change_size(x, y)

    def on_key_pressed(self, event):
        """Calls method related to pressed key.

        :var event: catched event
        :type event: Tkinter event
        """
        if event.keysym in ("Escape",):
            self.shutdown()

        elif event.keysym in ("Return",):
            self.update(
                self.view.master.winfo_pointerx(), self.view.master.winfo_pointery()
            )

        elif event.keysym in ("Space", "Tab"):
            self.skip_current_window()

        elif event.keysym in [str(i) for i in range(1, 10)]:
            self.workspace_activated(int(event.keysym))

        elif event.keysym in ["KP_{}".format(i) for i in range(1, 10)]:
            self.workspace_activated(int(event.keysym[-1]))

        elif event.keysym in ["F{}".format(i) for i in range(1, 17)]:
            self.window_activated(int(event.keysym[1:]))

        return "break"

    def on_mouse_left_down(self, event):
        """Calls update_model with current cursor position

        if controller is in constants.LOCATE or constants.RESIZE state.

        :var event: catched event
        :type event: Tkinter event
        """
        self.update(
            self.view.master.winfo_pointerx(), self.view.master.winfo_pointery()
        )
        return "break"

    def on_mouse_middle_down(self, event):
        """Middle button down acts like left button has been pressed."""
        return self.on_mouse_left_down(event)

    def on_mouse_right_down(self, event):
        """Skips the current model.

        :var event: catched event
        :type event: Tkinter event
        """
        self.skip_current_window()
        return "break"

    def shutdown(self):
        """Stops mouse listener and destroys Tkinter root window."""
        self.listener.stop()
        self.view.master.destroy()

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

    def get_available_workspaces(self, win):
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
