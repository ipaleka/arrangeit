import os
import sys
import uuid

import autopy
import platform
from pynput.mouse import Button, Controller

sys.path.insert(0, os.path.abspath("../.."))


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


def save_screen(screen):
    screen.save("screen_{}.png".format(str(uuid.uuid4())))


def locate_image(filename):
    screen = autopy.bitmap.capture_screen()
    node = platform.node()
    if node in ("winvm",):
        save_screen(screen)
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "resources/{}/".format(node),
        "{}.png".format(filename),
    )
    button = autopy.bitmap.Bitmap.open(path)
    return screen.find_bitmap(button)
