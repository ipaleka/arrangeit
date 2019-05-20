from arrangeit.constants import ROOT_ALPHA, WINDOW_SHIFT_PIXELS, LOCATE, RESIZE, OTHER
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

    :var BaseController.controller: object that connects data and presentation
    :type BaseController.controller: type(:class:`BaseController`) instance (platform specific)
    :var BaseController.collector: object responsible for collecting windows data
    :type BaseController.collector: type(:class:`BaseCollector`) instance (platform specific)
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

    def move_window(self, wid):
        print("move_window")
        pass

    def move_and_resize_window(self, wid):
        print("move_and_resize_window")
        pass


class BaseController(object):
    """Base Controller class holding common code for all the platforms.

    :var app: platform specific parent app
    :type app: type(:class:`BaseApp`) instance
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
    state = LOCATE

    def __init__(self, app):
        """Sets app attribute and empty model and calls :func:`BaseController.setup`."""
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

    def set_root_geometry(self, root):
        """Sets provided root window width and height

        calculated from available width and height for screen
        as quarter of the smaller element.
        Returned width and height have 16:9 aspect ratio.

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

    def setup_root_window(self, root):
        """Sets provided root window appearance common for all platforms.

        :param root: root tkinter window
        :type root: :class:`tkinter.Tk` instance
        """
        self.set_root_geometry(root)
        root.wm_attributes("-alpha", ROOT_ALPHA)
        root.wm_attributes("-topmost", True)
        # TODO for resizing 'lr_angle', for released cursor 'left_ptr'
        #      http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/cursors.html
        root.config(cursor="ul_angle")

    def get_cursor_position(self):
        """Returns current cursor position by calculating it from master data.

        :returns: (int, int) representing x and y coordinates
        """
        return (
            self.view.master.winfo_pointerx() - self.view.master.winfo_rootx(),
            self.view.master.winfo_pointery() - self.view.master.winfo_rooty(),
        )

    def run(self, generator):
        """Syncs data, initializes and starts listener, shows root and enters main loop.

        Sets generator attribute to provided generator and sets window data
        by calling :func:`BaseController.next` for the first time.
        Initially calls `on_mouse_move` with current cursor position as arguments.
        Calls `focus_set` on view frame so key and mouse events may be activated.
        """
        self.generator = generator
        self.next()

        self.listener = get_mouse_listener(self.on_mouse_move)
        self.listener.start()
        # self.listener.stop() to stop - can't restart it afterward, create new instead
        self.view.master.update()
        self.view.master.deiconify()
        self.view.focus_set()
        click_left()
        self.mainloop()

    def next(self):
        """Sets controller ``model`` attribute from the value yielded from ``generator``

        and populates view widgets with new model data.
        Also moves cursor and root window to model's window position.
        If there are no values left in collection then calls
        :func:`BaseController.save_default` and :func:`BaseController.shutdown`

        :returns: Boolean
        """
        try:
            self.model = next(self.generator)
        except StopIteration:
            self.save_default()
            self.shutdown()
            return True

        self.view.title.set(self.model.title)

        self.state = LOCATE
        self.place_above_model()
        return False

    def update(self, x, y):
        """Updates model with provided cursor position in regard to state

        and takes action in regard to state and model type.

        :var x: current horizontal axis mouse position in pixels
        :type x: int
        :var y: current vertical axis mouse position in pixels
        :type y: int
        """
        if self.state == LOCATE:
            self.model.set_changed(x=x, y=y)
            if not self.model.resizable:
                self.app.move_window(wid=self.model.wid)  # TODO async
                self.next()
            else:
                self.state = RESIZE

        elif self.state == RESIZE:
            w, h = self.model.wh_from_ending_xy(x, y)
            self.model.set_changed(w=w, h=h)
            self.app.move_and_resize_window(self.model.wid)  # TODO async
            self.next()

    def place_above_model(self):
        """Moves cursor and master on model's x and y position."""
        move_cursor(self.model.x, self.model.y)
        self.on_mouse_move(self.model.x, self.model.y)

    def on_mouse_move(self, x, y):
        """Moves root Tkinter window to provided mouse coordinates.

        Adds negative WINDOW_SHIFT_PIXELS to mouse position for better presentation.

        :var x: current horizontal axis mouse position in pixels
        :type x: int
        :var y: current vertical axis mouse position in pixels
        :type y: int
        """
        self.view.master.geometry(
            "+{}+{}".format(x - WINDOW_SHIFT_PIXELS, y - WINDOW_SHIFT_PIXELS)
        )

    def on_escape_key_pressed(self, event):
        """Calls shutdown method."""
        print("escape down")
        self.shutdown()
        return "break"

    def on_mouse_left_down(self, event):
        """Calls update_model with current cursor position

        if controller is in LOCATE or RESIZE state.

        :var event: catched event
        :type event: Tkinter event
        """
        self.update(
            self.view.master.winfo_pointerx(), self.view.master.winfo_pointery()
        )
        return "break"

    def on_mouse_right_down(self, event):
        """Skips the current model.

        :var event: catched event
        :type event: Tkinter event
        """
        print("right down")
        self.next()
        return "break"

    def shutdown(self):
        """Stops mouse listener and destroys Tkinter root window."""
        self.listener.stop()
        self.view.master.destroy()

    def mainloop(self):
        self.view.mainloop()

    def save_default(self):
        print("save default")
        pass


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
