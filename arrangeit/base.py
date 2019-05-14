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
        self.collection = WindowsCollection()

    def applicable(self, window_type):
        """Method must be overridden."""
        raise NotImplementedError

    def valid_state(self, window_type, window_state):
        """Method must be overridden."""
        raise NotImplementedError

    def resizable(self, window_type):
        """Method must be overridden."""
        raise NotImplementedError

    def __call__(self):
        """Method must be overridden."""
        raise NotImplementedError


class BasePlayer(object):
    """Base Player class holding common code for all the platforms."""
    model = None

    def __init__(self):
        self.model = WindowModel()

    def __call__(self):
        pass

