import sys
from platform import system
from gettext import gettext as _
from importlib import import_module
from itertools import islice, chain, product

from PIL import ImageFilter, ImageTk


def platform_path():
    """Returns lowercased string holding platform name."""
    return system().lower()


def platform_user_data_path():
    """Retrieves platform specific user data directory path."""
    module = import_module("arrangeit.{}.utils".format(platform_path()))
    return getattr(module, "user_data_path")()


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
        sys.exit(_("arrangeit can't run on your platform. :("))
    return getattr(module, name)


def get_component_class(name, platform=None):
    """Helper method for retrieving platform specific App class.

    :param platform: platform name
    :type platform: string
    :returns: class with provided `name` from the platform specific package
    """
    return get_class(name, platform=platform)


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


def append_to_collection(element, collection):
    """Simple helper function to append provided elem to provided collection.

    This function is used as callback argument for win32gui.EnumWindows
    and it requires True to be returned.

    :param element: element to add
    :type element: int
    :param collection: collection to add element to
    :type collection: list
    :returns: True
    """
    collection.append(element)
    return True


def quarter_by_smaller(width, height):
    """Helper method for retrieving one-forth for given ``width`` and ``height``

    with aspect ratio of 16:9.

    Starting point for calculation is the smaller value - the presumption
    is that monitors could be stacked in left-to-right **or** top-to-bottom manner.

    :param width: total desktop area width
    :type width: int
    :param height: total desktop area height
    :type height: int
    :returns: (int, int)
    """
    if width > height:
        return (int((height / 4) * 16 / 9), height // 4)
    return (width // 4, int((width / 4) * 9 / 16))


def increased_by_fraction(value, fraction):
    """Helper method for increasing provided value by provided fraction.

    :param value: value to increase
    :type value: int
    :param fraction: fraction of a whole to increase value by
    :type fraction: float
    :returns: int
    """
    return round(value * (1.0 + fraction))


def _get_snapping_source_by_ordinal(rect, snap, ordinal=0):
    """Returns snapping rectangle by ordinal from 0 as horizontal top

    clockwise to vertical left as 3.

    :returns: tuple (x0, y0, x1, y1)
    """
    if ordinal == 0:
        return (
            rect[0] - snap,
            rect[1] - snap,
            rect[0] + rect[2] + snap,
            rect[1] + snap,
        )
    elif ordinal == 1:
        return (
            rect[0] + rect[2] - snap,
            rect[1] - snap,
            rect[0] + rect[2] + snap,
            rect[1] + rect[3] + snap,
        )
    elif ordinal == 2:
        return (
            rect[0] - snap,
            rect[1] + rect[3] - snap,
            rect[0] + rect[2] + snap,
            rect[1] + rect[3] + snap,
        )
    elif ordinal == 3:
        return (
            rect[0] - snap,
            rect[1] - snap,
            rect[0] + snap,
            rect[1] + rect[3] + snap,
        )


def get_snapping_sources_for_rect(rect, snap, corner=None):
    """Returns snapping rectangles formated as (x0,y0,x0,y0) from provided rect.

    Snapping rectangle is created around window connected edge points pair with
    height (or width) of 2*SNAP_PIXELS and width (or height) of related window side.

    All four rectangles are returned for default corner of None.
    If corner is provided then it returns two adjacent rectangles for related provided
    corner (horizontal first, vertical second) where ordinal 0 is top-left corner,
    with clockwise ordering to bottom-left corner which is ordinal 3.

    :param rect: window rectangle (x, y, width, height)
    :type rect: (int, int, int, int)
    :param snap: snapping distance in pixels
    :type snap: int
    :returns: four-tuple or two-tuple of (x0, y0, x1, y1)
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


def intersects(source, target):
    """Checks does provided rectangle source intersect with provided target rectangle.

    Provided rectangles **don't** intersect if at least one of following statements
    is true:

    - bottom side of source is above top side of target
    - bottom side of target is above top side of source
    - left side of source is placed on the right side of the target right edge
    - left side of target is placed on the right side of the source right edge

    :param source: rectangle (x0, y0, x1, y1)
    :type source: (int, int, int, int)
    :param target: rectangle (x0, y0, x1, y1)
    :type target: (int, int, int, int)
    :returns: Boolean
    """
    return not (
        source[3] < target[1]
        or target[3] < source[1]
        or source[0] > target[2]
        or target[0] > source[2]
    )


def check_intersection(sources, targets):
    """Returns first pair that intersects from sources and targets list of four-tuples.

    Sources is either four-tuple representing whole window or two-tuple representing
    specific corner of the window (from first top-left clockwise to forth bottom-left).

    We are interested in intersection of odd or even pairs of sources and targets.
    It means that sources[0] or sources[2] should intersect with
    targets[n][0] or targets[n][2], respectively sources[1] or sources[3]
    should intersect with targets[n][1] or targets[n][3].

    So we create iterator that first cycle through all even elements pairs and
    then through all odd elements pairs. Stops iteration when first intersected pair
    is found and returns that pair.

    :param sources: two-tuple or four-tuple of (x0, y0, x1, y1)
    :type sources: tuple
    :param targets: collection of four-tuples (x0, y0, x1, y1)
    :type targets: list of four-tuples
    :returns: two-tuple ((x0,y0,x1,y1),(x0,y0,x1,y1)) or False
    """
    return next(
        (
            pair
            for pair in chain(
                product(
                    islice(sources, 0, None, 2), islice(chain(*targets), 0, None, 2)
                ),
                product(
                    islice(sources, 1, None, 2), islice(chain(*targets), 1, None, 2)
                ),
            )
            if intersects(*pair)
        ),
        False,
    )


def offset_for_intersecting_pair(rectangles, snap):
    """Calculates and returns offset (x, y) for provided overlapping pair of rectangles.

    Offset is value we should add or substract so rectangles overlapping sides fit.
    The only value checking here is for provided `rectangles` parameter as it could
    be False as the result of call to other function. If it's not we imply that
    provided pair is snapping rectangle with the same width or height.
    `snap` parameter is provided just for doublechecking reason.

    :param rectangles: intersecting pair of rectangles
    :type rectangles: two-tuple ((x0,y0,x1,y1),(x0,y0,x1,y1))
    :param snap: snapping value in pixels
    :type snap: int
    :returns: tuple (x,y)
    """
    if not rectangles:
        return (0, 0)

    return (
        (rectangles[1][0] - rectangles[0][0], 0)
        if rectangles[0][2] - rectangles[0][0]
        == rectangles[1][2] - rectangles[1][0]
        == snap * 2
        else (0, rectangles[1][1] - rectangles[0][1])
    )


def get_prepared_screenshot(image):
    """Filters provided image and converts it to format suitable for Tkinter.

    SCREENSHOT_BLUR_PIXELS defines blur depth in pixels.

    :param image: raw screenshot image
    :type image: :class:`PIL.Image.Image
    :returns: :class:`PIL.ImageTk.PhotoImage
    """
    from arrangeit.settings import Settings

    if Settings.SCREENSHOT_TO_GRAYSCALE:
        return ImageTk.PhotoImage(
            image.convert("L").filter(
                ImageFilter.BoxBlur(Settings.SCREENSHOT_BLUR_PIXELS)
            )
        )
    return ImageTk.PhotoImage(
        image.filter(ImageFilter.BoxBlur(Settings.SCREENSHOT_BLUR_PIXELS))
    )

