from arrangeit.base import BaseCollector

class Collector(BaseCollector):
    """Collecting windows class with MS Windows specific code."""

    def applicable(self, window_type):
        pass

    def valid_state(self, window_type, window_state):
        pass

    def resizable(self, window_type):
        pass

    def __call__(self):
        pass

