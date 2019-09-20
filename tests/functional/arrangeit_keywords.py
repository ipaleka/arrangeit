# import gi
import os
import sys

import autopy
from pynput.mouse import Button, Controller


# gi.require_version("Wnck", "3.0")
# from gi.repository import Wnck

sys.path.insert(0, os.path.abspath("../.."))

# from arrangeit.linux.collector import Collector
RESOURCES_PATH = "resources/1600x900/"


def release_cursor():
    mouse = Controller()
    mouse.press(Button.middle)
    mouse.release(Button.middle)


def left_mouse_click_on_position(pos):
    mouse = Controller()
    mouse.position = tuple(pos)
    mouse.click(Button.left)


def take_screenshot():
    screen = autopy.bitmap.capture_screen()
    screen.save("screen.png")


def locate_image(filename):
    screen = autopy.bitmap.capture_screen()
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        RESOURCES_PATH,
        "{}.png".format(filename),
    )
    print(path)
    button = autopy.bitmap.Bitmap.open(path)
    # print(button)
    return screen.find_bitmap(button)


# def locate_button(name="options"):
#     screen = autopy.bitmap.capture_screen()
#     # screen.save("screen.png")
#     path = os.path.join(os.path.dirname(__file__), "{}.png".format(name))
#     button = autopy.bitmap.Bitmap.open(path)
#     print(button)
#     return screen.find_bitmap(button)


if __name__ == "__main__":
    pos = locate_image("button-quit")
    print(pos)
