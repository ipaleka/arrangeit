from arrangeit.base import BaseApp


class App(BaseApp):
    """Main app class with MS Windows specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move_and_resize(self, wid):
        pass

    def move(self, wid):
        pass
