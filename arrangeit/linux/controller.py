from arrangeit.base import BaseController


class Controller(BaseController):
    """Controller class with GNU/Linux specific code."""

    def __init__(self, app):
        super().__init__(app)

    def setup_root_window(self, root):
        """Sets provided root appearance attributes specific for GNU/Linux."""
        root.wm_attributes("-type", "splash")
        super().setup_root_window(root)
