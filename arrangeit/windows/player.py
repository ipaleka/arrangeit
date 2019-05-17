from arrangeit.base import BasePlayer


class Player(BasePlayer):
    """Player class with MS Windows specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, generator):
        super().run(generator)
