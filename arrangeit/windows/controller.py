from arrangeit.base import BaseController


class Controller(BaseController):
    """Controller class with MS Windows specific code."""

    def __init__(self, app):
        super().__init__(app)

    def setup_root_window(self, root):
        """Sets provided root appearance attributes specific for MS Windows."""
        root.overrideredirect(True)
        super().setup_root_window(root)
