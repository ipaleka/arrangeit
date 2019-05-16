from arrangeit.base import BaseApp


class App(BaseApp):
    """Main app class with GNU/Linux specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)

