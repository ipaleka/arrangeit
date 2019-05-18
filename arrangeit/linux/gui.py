from arrangeit.base import BaseGui


class Gui(BaseGui):
    """GUI class with GNU/Linux specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_root_window(self, root):
        """Sets provided root appearance attributes specific for GNU/Linux."""
        pass
        # root.wm_attributes("-type", "splash")
        # root.wm_attributes("-alpha", 0.7)  # doesn't work without -type splash; -type is X Windows only
