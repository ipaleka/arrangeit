import gi
import os
import sys

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck

sys.path.insert(0, os.path.abspath("../.."))

from arrangeit.linux.collector import Collector

import autopy


def take_screenshot():
    screen = autopy.bitmap.capture_screen()
    screen.save("screen.png")

# def locate_button(name="options"):
#     screen = autopy.bitmap.capture_screen()
#     # screen.save("screen.png")
#     path = os.path.join(os.path.dirname(__file__), "{}.png".format(name))
#     button = autopy.bitmap.Bitmap.open(path)
#     print(button)
#     return screen.find_bitmap(button)


# if __name__ == "__main__":
#     collector = Collector()
#     import time

#     time.sleep(5)
#     print([win.get_name() for win in collector.get_windows()])
#     print("\n\n")
#     print(locate_button())
