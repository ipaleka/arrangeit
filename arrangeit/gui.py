from tkinter import Tk, Frame, StringVar

from pynput import mouse


def get_initialized_tk_root():
    """Initializes and returns Tkinter root window.

    :returns: :class:`tkinter.Tk` window instance
    """
    return Tk()


def get_mouse_listener(callback):
    """Initializes mouse listener by binding it to provided ``callback`` and returns it.

    :returns: :class:`mouse.Listener` instance
    """
    return mouse.Listener(on_move=callback)


class GuiApplication(Frame):
    """Tkinter frame showing current window from the data provided through player.

    :var master: parent Tkinter window
    :type master: :class:`Tk` root window instance
    :var player: controller object providing windows data
    :type player: type(:class:`BasePlayer`) instance (platform specific)
    """

    master = None
    player = None

    def __init__(self, master=None, player=None):
        """Sets master and player attributes from provided arguments

        after super __init__ is called. Then sets the packer and
        calls :func:`create_widgets` method.
        """
        super().__init__(master)
        self.master = master
        self.player = player
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """Creates and packs all the frame's widgets."""

        self.title = StringVar()

        # self.title_label = tk.Label(self, textvariable=self.title)
        # self.title_label.pack(side="top")

        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "player.next\n(click me)"
        # self.hi_there["command"] = self.player.next
        # self.hi_there.pack(side="top")

        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                       command=self.player.quit)
        # self.quit.pack(side="bottom")

        # bg_image = tk.PhotoImage(file=fname)
        # # get the width and height of the image
        # w = bg_image.width()
        # h = bg_image.height()
        # # size the window so the image will fill it
        # root.geometry("%dx%d+50+30" % (w, h))
        # cv = tk.Canvas(width=w, height=h)
        # cv.pack(side='top', fill='both', expand='yes')
        # cv.create_image(0, 0, image=bg_image, anchor='nw')
        # # add canvas text at coordinates x=15, y=20
        # # anchor='nw' implies upper left corner coordinates
        # cv.create_text(15, 20, text="Python Greetings", fill="red", anchor='nw')
