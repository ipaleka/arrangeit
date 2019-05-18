from arrangeit.base import BaseController


class Controller(BaseController):
    """Controller class with GNU/Linux specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_root_window(self, root):
        """Sets provided root appearance attributes specific for GNU/Linux."""
        root.wm_attributes("-type", "splash")
        super().setup_root_window(root)
