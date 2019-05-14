from arrangeit.base import BaseCollector


class Collector(BaseCollector):
    """Collecting windows class with MS Windows specific code."""

    def is_applicable(self, window_type):
        pass

    def is_valid_state(self, window_type, window_state):
        pass

    def is_resizable(self, window_type):
        pass

    def get_windows(self):
        pass

    def check_window(self, win):
        pass

    def __call__(self):
        pass

