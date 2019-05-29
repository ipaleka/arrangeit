import sys
from platform import system
from gettext import gettext as _
from importlib import import_module
from itertools import islice, chain, product


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


def get_snapping_sources_for_rect(rect, snap):
    """Returns four snapping rectangles from provided rect formated as (x0,y0,x0,y0).

    Snapping rectangle is created around window connected edge points pair with
    height (or width) of 2*SNAP_PIXELS and width (or height) of related window side.

    :param rect: window rectangle (x, y, width, height)
    :type rect: (int, int, int, int)
    :param snap: snapping distance in pixels
    :type snap: int
    :returns: four-tuple of (x0, y0, x1, y1)
    """
    return (
        (rect[0] - snap, rect[1] - snap, rect[0] + rect[2] + snap, rect[1] + snap),
        (
            rect[0] + rect[2] - snap,
            rect[1] - snap,
            rect[0] + rect[2] + snap,
            rect[1] + rect[3] + snap,
        ),
        (
            rect[0] - snap,
            rect[1] + rect[3] - snap,
            rect[0] + rect[2] + snap,
            rect[1] + rect[3] + snap,
        ),
        (rect[0] - snap, rect[1] - snap, rect[0] + snap, rect[1] + rect[3] + snap),
    )


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
    """Returns first pair that intersects by checking sources four-tuple and targets

    list of four-tuples.

    We are interested in intersection of odd or even pairs of sources and targets.
    It means that sources[0] or sources[2] should intersect with
    targets[n][0] or targets[n][2], respectively sources[1] or sources[3]
    should intersect with targets[n][1] or targets[n][3].

    So we create iterator that first cycle through all even elements pairs and
    then through all odd elements pairs. Stops iteration when first intersected pair
    is found and returns that pair.

    :param sources: four-tuple of (x0, y0, x1, y1)
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
