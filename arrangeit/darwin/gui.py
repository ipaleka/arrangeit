from arrangeit.base import BaseGui


class Gui(BaseGui):
    """GUI class with Mac OS specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_root_window(self, root):
        """Sets provided root appearance attributes specific for Mac OS."""
        pass
