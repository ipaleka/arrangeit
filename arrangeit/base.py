from arrangeit import utils
from arrangeit.data import WindowModel, WindowsCollection
from arrangeit.guicommon import get_tkinter_root, get_mouse_listener, GuiApplication


class BaseApp(object):
    """Base App class holding common code for all the platforms.

    :var collector: object responsible for collecting windows data
    :type collector: type(:class:`BaseCollector`) instance (platform specific)
    :var player: object responsible for presenting collected windows data
    :type player: type(:class:`BasePlayer`) instance (platform specific)
    """

    gui = None
    collector = None
    player = None

    def __init__(self, *args, **kwargs):
        """Instantiates platform specific Gui, Collector and Player classes."""
        self.gui = self.setup_gui()()
        self.collector = self.setup_collector()()
        self.player = self.setup_player()(gui_app=self.gui.app)

    def setup_gui(self):
        """Returns platform specific Gui class."""
        return utils.get_component_class("Gui")

    def setup_collector(self):
        """Returns platform specific Collector class."""
        return utils.get_component_class("Collector")

    def setup_player(self):
        """Returns platform specific Player class."""
        return utils.get_component_class("Player")

    def run(self):
        """Collects data, prepare them for view and finally shows gui application."""
        self.collector.run()
        self.player.run(self.collector.collection.generator())
        self.gui.run()


class BaseGui(object):
    """Base Gui class holding common code for all the platforms.

    :var app: Tkinter application showing main window
    :type app: :class:`GuiApplication` instance
    :var listener: Tkinter application showing main window
    :type listener: :class:`GuiApplication` instance
    """

    app = None
    listener = None

    def __init__(self):
        """Initializes empty model and calls :func:`BasePlayer.setup`."""
        self.setup()

    def setup(self):
        """Initializes Tkinter GuiApplication with root window and self as arguments.

        Sets app attribute to newly created Tkinter application.
        Prevents root window to show by calling its `withdraw` method.
        Tkinter root window from now may be accessed by `[self].app.master` attribute.
        """
        root = get_tkinter_root()
        self.setup_root_window(root)
        self.app = GuiApplication(master=root, controller=self)
        root.withdraw()

    def setup_root_window(self, root):
        """Sets provided root window appearance common for all platforms."""
        pass
        # root.geometry("140x100")
        # root.overrideredirect(True)

        # root.wm_attributes("-type", "splash")
        # root.wm_attributes("-alpha", 0.7)  # doesn't work without -type splash; -type is X Windows only
        # root.wm_attributes("-topmost", True)
        # # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/cursors.html
        # root.config(cursor='ul_angle')  # for resizing 'lr_angle', for released cursor 'left_ptr'

    def run(self):
        """Initializes and starts mouse listener, shows master and starts main loop."""
        self.listener = get_mouse_listener(self.on_mouse_move)
        self.listener.start()  # self.listener.stop() to stop
        self.app.master.update()
        self.app.master.deiconify()
        self.mainloop()

    def on_mouse_move(self, x, y):
        """Moves root Tkinter window to provided mouse coordinates.

        :var x: current horizontal axis mouse position in pixels
        :type x: int
        :var y: current vertical axis mouse position in pixels
        :type y: int
        """
        self.app.master.geometry("+{}+{}".format(x, y))

    def mainloop(self):
        self.app.mainloop()


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


class BasePlayer(object):
    """Base Player class holding common code for all the platforms.

    :var model: model holding window data
    :type model: :class:`WindowModel` instance
    :var generator: generator for retrieving model instances from collection
    :type generator: Generator[WindowModel, None, None]
    :var gui_app: Tkinter application showing main window
    :type gui_app: :class:`GuiApplication` instance
    """

    model = None
    generator = None
    gui_app = None

    def __init__(self, gui_app):
        """Initializes empty model and sets `gui_app` attribute

        from provided :class:`GuiApplication` instance.
        """
        self.gui_app = gui_app
        self.model = WindowModel()

    def run(self, generator):
        """Starts the player by calling :func:`BasePlayer.next` for the first time

        after player's ``generator`` attribute is set to provided generator (``next``
        uses it for getting the current window data).
        """
        self.generator = generator
        self.next()

    def next(self):
        """Sets player ``model`` attribute from the value yielded from ``generator``

        and populate gui widgets with new model data.1
        """
        self.model = next(self.generator)
        self.gui_app.title.set(self.model.title)
