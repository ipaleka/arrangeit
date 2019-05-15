from arrangeit import utils
from arrangeit.data import WindowModel, WindowsCollection


class BaseApp(object):
    """Base App class holding common code for all the platforms."""

    collector = None
    player = None

    def __init__(self):
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
        """Method must be overridden."""
        raise NotImplementedError


class BaseCollector(object):
    """Base Collector class holding common code for all the platforms."""

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

    def __call__(self):
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
    """Base Player class holding common code for all the platforms."""

    model = None

    def __init__(self):
        self.model = WindowModel()

    def __call__(self):
        pass
