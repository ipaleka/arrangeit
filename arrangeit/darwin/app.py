from arrangeit.base import BaseApp


class App(BaseApp):
    """Main app class with Mac OS specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
