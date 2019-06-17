import queue

from pynput.mouse import Controller, Listener


class Mouse(object):
    """Class responsible for listening and controlling system-wide mouse events.

    :var queue: mouse events queue
    :type queue: :class:`queue.Queue`
    :var listener: separate thread listening for mouse events
    :type listener: :class:`Listener`
    """

    queue = None
    listener = None

    def __init__(self):
        """Instatiates and sets queue."""
        self.queue = queue.Queue()

    def cursor_position(self):
        """Returns current cursor position.

        :returns: (int, int)
        """
        return Controller().position

    def get_item(self):
        """Gets next item in queue and returns it.

        :returns: (x,y) or bool or None
        """
        try:
            return self.queue.get(block=False)
        except queue.Empty:
            return None

    def move_cursor(self, x, y):
        """Moves cursor position to a point defined by provided x and y."""
        Controller().position = (x, y)

    def on_move(self, x, y):
        """Puts provided x and y in queue as position tuple.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        self.queue.put((x, y))

    def on_scroll(self, x, y, dx, dy):
        """Puts scroll direction as Boolean value in queue.

        We are interested only in in dy that holds either +1 or -1 value, so we
        converted that to Boolean value.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        :param dx: scroll vector on x axis
        :type dx: int
        :param dy: scroll vector on y axis
        :type dy: int
        """
        self.queue.put(dy > 0)

    def start(self):
        """Initializes and starts listener for move and scroll events."""
        self.listener = Listener(
            on_move=self.on_move, on_scroll=self.on_scroll
        )
        self.listener.start()

    def stop(self):
        """Stops listener."""
        self.listener.stop()
