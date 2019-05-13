class WindowModel(object):
    """Class holding window data."""
    xy = None
    size = None
    wid = None
    title = None

    def __init__(self, *args, **kwargs):
        self.setup(*args, **kwargs)

    def setup(self, *args, **kwargs):
        self.xy = kwargs.get('xy', None)
        self.size = kwargs.get('size', None)
        self.wid = kwargs.get('wid', None)
        self.title = kwargs.get('title', None)
