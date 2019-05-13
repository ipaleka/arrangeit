from arrangeit import utils
from arrangeit.data import WindowModel


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
        raise NotImplementedError

    # def play(self):
    #     self.player()


class BaseCollector(object):
    """Base Collector class holding common code for all the platforms."""
    model = None

    def __init__(self):
        self.model = WindowModel()

    def __call__(self):
        pass

    # def __iter__(self):
    #     for elem in self._datastructure:
    #         if elem.visible:
    #             yield elem.value


class BasePlayer(object):
    """Base Player class holding common code for all the platforms."""

    def __init__(self):
        pass

    def __call__(self):
        pass

