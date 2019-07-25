# arrangeit - cross-platform desktop utility for easy windows management
# Copyright (C) 1999-2019 Ivica Paleka

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import logging
import os
import sys
from collections import namedtuple
from importlib import import_module
from itertools import chain, islice, product
from platform import system

from PIL import Image, ImageFilter, ImageOps, ImageTk

Rectangle = namedtuple("Rectangle", "x0 y0 x1 y1")

MESSAGES = {"platform_error": "arrangeit can't run on your platform. :("}


## PLATFORM
def platform_path():
    """Returns lowercased string holding platform name."""
    return system().lower()


def platform_user_data_path():
    """Retrieves platform specific user data directory path."""
    module = import_module("arrangeit.{}.utils".format(platform_path()))
    return getattr(module, "user_data_path")()


## SETUP
def get_class(name, platform):
    """Helper method for retrieving platform specific class instance

    for given ``name`` and ``platform``.

    If provided ``platform`` is None then we use :func:`platform_path`.

    If class can't be imported that means host system
    isn't implemented (yet...) and so we sys.exit with a message.

    :param name: function name suffix
    :type name: string
    :param platform: platform name
    :type platform: string or None
    :returns: class instance from the platform specific package
    """
    try:
        module = import_module(
            "arrangeit.{}.{}".format(
                platform if platform is not None else platform_path(), name.lower()
            )
        )
    except ImportError:
        logging.exception("Load module platform_error")
        sys.exit(MESSAGES["platform_error"])
    return getattr(module, name)


def get_component_class(name, platform=None):
    """Helper method for retrieving platform specific App class.

    :param platform: platform name
    :type platform: string
    :returns: class with provided ``name`` from the platform specific package
    """
    return get_class(name, platform=platform)


## HELPERS
def get_cursor_name(corner, with_arrow=False):
    """Returns cursor name for provided corner.

    :param corner: corner number
    :type corner: int
    :param with_arrow: indicating should cursor contain an arrow
    :type with_arrow: Boolean
    :returns: str
    """
    if with_arrow:
        return (
            "top_left_corner",
            "top_right_corner",
            "bottom_right_corner",
            "bottom_left_corner",
        )[corner]
    return ("ul_angle", "ur_angle", "lr_angle", "ll_angle")[corner]


def get_prepared_screenshot(image, blur_size=2, grayscale=False):
    """Filters provided image and converts it to format suitable for Tkinter.

    SCREENSHOT_BLUR_PIXELS defines blur depth in pixels.

    :param image: raw screenshot image
    :type image: :class:`PIL.Image.Image`
    :param blur_size: how many pixels in all directions will be blured
    :type blur_size: int
    :param grayscale: should image be converted to grayscale
    :type grayscale: Boolean
    :returns: :class:`PIL.ImageTk.PhotoImage`
    """
    if grayscale:
        return ImageTk.PhotoImage(
            image.convert("L").filter(ImageFilter.BoxBlur(blur_size))
        )
    return ImageTk.PhotoImage(image.filter(ImageFilter.BoxBlur(blur_size)))


def get_resized_image(filename, size):
    """Opens and resizes image with provided filename to provided size.

    :param filename: resource file name
    :type filename: str
    :param size: width and height to resize image to
    :type size: tuple
    :returns: :class:`PIL.Image`
    """
    return ImageTk.PhotoImage(
        Image.open(get_resource_path(filename)).resize(size, Image.LANCZOS)
    )


def get_resource_path(filename):
    """Returns full path to resource with provided filename.

    :param filename: resource file name
    :type filename: str
    :returns: str
    """
    return os.path.join(os.path.dirname(__file__), "resources", filename)


def get_value_if_valid_type(value, typ):
    """Returns provided value if it's of provided type

    or returns None if it's not. If value is None then None is returned.
    If provided value and typ are collections then each element is checked.

    :param value: value to check for type
    :type value: Python type
    :param typ: type to check on ``value``
    :type typ: Python type
    :returns: value or None
    """
    if isinstance(value, (tuple, list)):
        if not isinstance(typ, (tuple, list)) or len(value) != len(typ):
            return ()
        return (
            value if all(isinstance(val, typ[i]) for i, val in enumerate(value)) else ()
        )
    return value if isinstance(value, typ) else None


def increased_by_fraction(value, fraction):
    """Helper method for increasing provided value by provided fraction.

    :param value: value to increase
    :type value: int
    :param fraction: fraction of a whole to increase value by
    :type fraction: float
    :returns: int
    """
    return round(value * (1.0 + fraction))


def open_image(filename, background="white", colorized=False, foreground="red"):
    """Returns Pillow image instance from provided name and colorizes it if set.

    Provided ``black`` and ``white`` are used for colorize filter.

    :param filename: image filename
    :type filename: str
    :param background: image background color
    :type background: str
    :param colorized: should return image be highlighted
    :type colorized: Boolean
    :param foreground: image foreground color
    :type foreground: str
    :returns: :class:`PIL.Image`
    """
    image = Image.open(get_resource_path(filename)).convert("L")
    return ImageOps.colorize(image, foreground if colorized else "black", background)


def quarter_by_smaller(width, height, size=3):
    """Helper method for retrieving one-forth (default) for given ``width`` and ``height``

    with aspect ratio of 16:9.

    Starting point for calculation is the smaller value - the presumption
    is that monitors could be stacked in left-to-right **or** top-to-bottom manner.

    :param width: total desktop area width
    :type width: int
    :param height: total desktop area height
    :type height: int
    :param size: window size from 1 to 4
    :type size: int
    :var denominator: window size denominator from 6 to 3
    :type denominator: int
    :returns: (int, int)
    """
    denominator = (6, 5, 4, 3)[size - 1] if size in range(1, 5) else 4
    if width > height:
        return (int((height / denominator) * 16 / 9), height // denominator)
    return (width // denominator, int((width / denominator) * 9 / 16))


def set_icon(widget):
    """Sets application icon to provided widget window.

    :param widget: Tkinter toplevel widget
    :type widget: :class:`tk.Toplevel` or :class:`tk.Tk`
    """
    widget.tk.call(
        "wm",
        "iconphoto",
        widget._w,
        ImageTk.PhotoImage(file=get_resource_path("icon128.png")),
    )


## SNAPPING
def _get_snapping_source_by_ordinal(rect, snap, ordinal=0):
    """Returns snapping rectangle by ordinal from 0 as horizontal top

    clockwise to vertical left as 3.

    :returns: :class:`Rectangle`
    """
    if ordinal == 0:
        return Rectangle(
            rect[0] - snap, rect[1] - snap, rect[0] + rect[2] + snap, rect[1] + snap
        )
    elif ordinal == 1:
        return Rectangle(
            rect[0] + rect[2] - snap,
            rect[1] - snap,
            rect[0] + rect[2] + snap,
            rect[1] + rect[3] + snap,
        )
    elif ordinal == 2:
        return Rectangle(
            rect[0] - snap,
            rect[1] + rect[3] - snap,
            rect[0] + rect[2] + snap,
            rect[1] + rect[3] + snap,
        )
    elif ordinal == 3:
        return Rectangle(
            rect[0] - snap, rect[1] - snap, rect[0] + snap, rect[1] + rect[3] + snap
        )


def _intersects(source, target):
    """Checks does provided rectangle source intersect with provided target rectangle.

    Provided rectangles **don't** intersect if at least one of following statements
    is true:

    - bottom side of source is above top side of target
    - bottom side of target is above top side of source
    - left side of source is placed on the right side of the target right edge
    - left side of target is placed on the right side of the source right edge

    :param source: rectangle (x0, y0, x1, y1)
    :type source: :class:`Rectangle`
    :param target: rectangle (x0, y0, x1, y1)
    :type target: :class:`Rectangle`
    :returns: Boolean
    """
    return not (
        source.y1 < target.y0
        or target.y1 < source.y0
        or source.x0 > target.x1
        or target.x0 > source.x1
    )


def _offset_for_intersecting_pair(rectangles, snap):
    """Calculates and returns offset (x, y) for provided overlapping pair of rectangles.

    Offset is value we should add or substract so rectangles overlapping sides fit.
    The only value checking here is for provided ``rectangles`` parameter as it could
    be False as the result of call to other function. If it's not we imply that
    provided pair is snapping rectangle with the same width or height.
    ``snap`` parameter is provided just for doublechecking reason.

    :param rectangles: intersecting pair of rectangles
    :type rectangles: (:class:`Rectangle`, :class:`Rectangle`)
    :param snap: snapping value in pixels
    :type snap: int
    :returns: tuple (x,y)
    """
    if not rectangles:
        return (0, 0)

    return (
        (rectangles[1].x0 - rectangles[0].x0, 0)
        if rectangles[0].x1 - rectangles[0].x0
        == rectangles[1].x1 - rectangles[1].x0
        == snap * 2
        else (0, rectangles[1].y0 - rectangles[0].y0)
    )


def check_intersections(sources, targets):
    """Returns first pairs that intersects from sources and targets list of Rectangles.

    Sources is either four-tuple representing whole window or two-tuple representing
    specific corner of the window (from first top-left clockwise to forth bottom-left).

    We are interested in intersection of odd or even pairs of sources and targets.
    It means that sources[0] or sources[2] should intersect with
    targets[n][0] or targets[n][2], respectively sources[1] or sources[3]
    should intersect with targets[n][1] or targets[n][3].

    So we create iterator that first cycle through all even elements pairs and
    then through all odd elements pairs. Stops iteration when first intersected pair
    is found. Returns either single pair (even or odd) or tuple of both.

    :param sources: two-tuple or four-tuple of root window snapping rectangles
    :type sources: tuple of :class:`Rectangle`
    :param targets: collection of other windows snapping rectangles
    :type targets: list of :class:`Rectangle`
    :param even: horizontal intersection pair or False
    :type even: (:class:`Rectangle`, :class:`Rectangle`)
    :param odd: vertical intersection pair or False
    :type odd: (:class:`Rectangle`, :class:`Rectangle`)
    :returns: :class:`Rectangle` or (:class:`Rectangle`,:class:`Rectangle`) or False
    """
    even = next(
        (
            pair
            for pair in product(
                islice(sources, 0, None, 2), islice(chain(*targets), 0, None, 2)
            )
            if _intersects(*pair)
        ),
        False,
    )
    odd = next(
        (
            pair
            for pair in product(
                islice(sources, 1, None, 2), islice(chain(*targets), 1, None, 2)
            )
            if _intersects(*pair)
        ),
        False,
    )

    if not even or not odd:
        return even or odd
    return (even, odd)


def get_snapping_sources_for_rect(rect, snap, corner=None):
    """Returns snapping rectangles formated as Rectangle(x0,y0,x0,y0) from provided rect.

    Snapping rectangle is created around window connected edge points pair with
    height (or width) of 2*SNAP_PIXELS and width (or height) of related window side.

    All four rectangles are returned for default corner of None.
    If corner is provided then it returns two adjacent rectangles for related provided
    corner (horizontal first, vertical second) where ordinal 0 is top-left corner,
    with clockwise ordering to bottom-left corner which is ordinal 3.

    :param rect: window defined by (x, y, width, height)
    :type rect: (int, int, int, int)
    :param snap: snapping distance in pixels
    :type snap: int
    :returns: two or four-tuple of :class:`Rectangle`
    """
    if corner == 0:
        return (
            _get_snapping_source_by_ordinal(rect, snap, 0),
            _get_snapping_source_by_ordinal(rect, snap, 3),
        )
    if corner == 1:
        return (
            _get_snapping_source_by_ordinal(rect, snap, 0),
            _get_snapping_source_by_ordinal(rect, snap, 1),
        )
    if corner == 2:
        return (
            _get_snapping_source_by_ordinal(rect, snap, 2),
            _get_snapping_source_by_ordinal(rect, snap, 1),
        )
    if corner == 3:
        return (
            _get_snapping_source_by_ordinal(rect, snap, 2),
            _get_snapping_source_by_ordinal(rect, snap, 3),
        )
    elif corner is None:
        return tuple((_get_snapping_source_by_ordinal(rect, snap, i) for i in range(4)))


def offset_for_intersections(rectangles, snap):
    """Checks if single or both axes intersect and returns related offset(s).

    :param rectangles: one or two intersecting pair of rectangles
    :type rectangles: :class:`Rectangle` or (:class:`Rectangle`, :class:`Rectangle`)
    :param snap: snapping value in pixels
    :type snap: int
    :returns: tuple (x,y)
    """
    if not rectangles:
        return (0, 0)

    if isinstance(rectangles[0], Rectangle):  # single pair provided
        return _offset_for_intersecting_pair(rectangles, snap)

    return (
        _offset_for_intersecting_pair(rectangles[1], snap)[0],
        _offset_for_intersecting_pair(rectangles[0], snap)[1],
    )
