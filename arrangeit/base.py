from arrangeit import utils
from arrangeit.data import WindowModel, WindowsCollection
from arrangeit.gui import get_initialized_tk_root, get_mouse_listener, GuiApplication


class BaseApp(object):
    """Base App class holding common code for all the platforms.

    :var collector: object responsible for collecting windows data
    :type collector: type(:class:`BaseCollector`) instance (platform specific)
    :var player: object responsible for presenting collected windows data
    :type player: type(:class:`BasePlayer`) instance (platform specific)
    """

    collector = None
    player = None

    def __init__(self, *args, **kwargs):
        """Instantiates platform specific Collector and Player classes."""
        self.collector = self.setup_collector()()
        self.player = self.setup_player()()

    def setup_collector(self):
        """Returns platform specific Collector class."""
        return utils.get_collector()

    def setup_player(self):
        """Returns platform specific Player class."""
        return utils.get_player()

    def run(self):
        """Runs ``collector`` to collect data and then runs ``player``

        with instantiated collector's collection generator as argument.
        """
        self.collector.run()
        self.player.run(self.collector.collection.generator())


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
    :var gui: Tkinter application showing main window
    :type gui: :class:`GuiApplication` instance
    :var listener: Tkinter application showing main window
    :type listener: :class:`GuiApplication` instance
    """

    model = None
    generator = None
    gui = None
    listener = None

    def __init__(self):
        """Initializes empty model and calls :func:`BasePlayer.setup`."""
        self.model = WindowModel()
        self.setup()

    def setup(self):
        """Initializes Tkinter GuiApplication with root window and self as arguments.

        Sets gui attribute to newly created Tkinter application.
        Prevents root window to show by calling its `withdraw` method.
        """
        root = get_initialized_tk_root()
        self.setup_root_window(root)
        self.gui = GuiApplication(master=root, player=self)
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


    def run(self, generator):
        """Starts the player by calling :func:`BasePlayer.next` for the first time

        after player's ``generator`` attribute is set to provided generator (``next``
        uses it for getting the current window data).
        Then calls the :func:`get_mouse_listener` method responsible for the mouse
        listener creation and binding, sets `listener` attribute and starts listener.
        Finally shows the root/master Tkinter window and calls player's `mainloop`.
        """
        self.generator = generator
        self.next()
        self.listener = get_mouse_listener(self.on_mouse_move)
        self.listener.start()  #self.listener.stop() to stop
        self.gui.master.update()
        self.gui.master.deiconify()
        self.mainloop()

    def next(self):
        """Sets player ``model`` attribute from the value yielded from ``generator``

        and populate gui widgets with new model data.1
        """
        self.model = next(self.generator)
        self.gui.title.set(self.model.title)

    def on_mouse_move(self, x, y):
        """Moves root Tkinter window to provided mouse coordinates.

        :var x: current horizontal axis mouse position in pixels
        :type x: int
        :var y: current vertical axis mouse position in pixels
        :type y: int
        """
        self.gui.master.geometry("+{}+{}".format(x, y))

    def mainloop(self):
        self.gui.mainloop()