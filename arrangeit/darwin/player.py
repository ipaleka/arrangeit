from arrangeit.base import BasePlayer


class Player(BasePlayer):
    """Player class with Mac OS specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

