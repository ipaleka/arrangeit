from arrangeit.base import BaseApp


class App(BaseApp):
    """Main app class with MS Windows specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

