from arrangeit import utils
from arrangeit.data import WindowModel, WindowsCollection
from arrangeit.view import get_tkinter_root, get_mouse_listener, ViewApplication
from arrangeit.utils import quarter_by_smaller


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
        self.controller = self.setup_controller()()
        self.collector = self.setup_collector()()

    def setup_controller(self):
        """Returns platform specific Controller class."""
        return utils.get_component_class("Controller")

    def setup_collector(self):
        """Returns platform specific Collector class."""
        return utils.get_component_class("Collector")

    def run(self):
        """Collects data, prepare them for view and finally shows view application."""
        self.collector.run()
        self.controller.run(self.collector.collection.generator())


class BaseController(object):
    """Base Controller class holding common code for all the platforms.

    :var model: model holding window data
    :type model: :class:`WindowModel` instance
    :var BaseController.generator: generator for retrieving model instances from collection
    :type BaseController.generator: Generator[WindowModel, None, None]
    :var view: Tkinter application showing main window
    :type view: :class:`ViewApplication` instance
    :var listener: Tkinter application showing main window
    :type listener: :class:`ViewApplication` instance
    """

    model = None
    generator = None
    view = None
    listener = None

    def __init__(self):
        """Initializes empty model and calls :func:`BaseController.setup`."""
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
        """Sets provided root window appearance common for all platforms."""
        width, height = quarter_by_smaller(
            root.winfo_screenwidth(), root.winfo_screenheight()
        )
        root.geometry("{}x{}".format(width, height))
        root.overrideredirect(True)
        root.wm_attributes("-alpha", 0.7)
        root.wm_attributes("-topmost", True)
        # # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/cursors.html
        # for resizing 'lr_angle', for released cursor 'left_ptr'
        root.config(cursor="ul_angle")

    def run(self, generator):
        """Syncs data, initializes and starts listener, shows root and enters main loop.

        Sets generator attribute to provided generator and sets window data
        by calling :func:`BaseController.next` for the first time.
        """
        self.generator = generator
        self.next()
        self.listener = get_mouse_listener(self.on_mouse_move)
        self.listener.start()  # self.listener.stop() to stop
        self.view.master.update()
        self.view.master.deiconify()
        self.mainloop()

    def next(self):
        """Sets controller ``model`` attribute from the value yielded from ``generator``

        and populate gui widgets with new model data.1
        """
        self.model = next(self.generator)
        self.view.title.set(self.model.title)

    def on_mouse_move(self, x, y):
        """Moves root Tkinter window to provided mouse coordinates.

        :var x: current horizontal axis mouse position in pixels
        :type x: int
        :var y: current vertical axis mouse position in pixels
        :type y: int
        """
        self.view.master.geometry("+{}+{}".format(x, y))

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
