from arrangeit import utils

class App(object):
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

    def setup(self):
        self.collector()

    # def play(self):
    #     self.player()


def main():
    app = App()
    app.setup()


if __name__ == "__main__":
    main()