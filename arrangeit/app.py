from platform import system
from importlib import import_module


class App:
    collector = None

    def __init__(self):
        self.collector = self.setup_collector()

    def platform_path(self):
        return system().lower()

    def setup_collector(self):
        collector = import_module('arrangeit.{}.collector'.format(self.platform_path()))
        return collector.Collector()

    def setup(self):
        self.collector()



def main():
    app = App()
    app.setup()


if __name__ == "__main__":
    main()