from arrangeit.base import BaseController
from arrangeit.data import WindowModel
from arrangeit.settings import Settings


## test_data
SAMPLE_RECT = (45, 54, 304, 405)
SAMPLE_MODEL_VALUES = [
    {"wid": 101},
    {"rect": SAMPLE_RECT},
    {"resizable": True},
    {"title": "foo"},
    {"name": "bar"},
    {"icon": Settings.BLANK_ICON},
    {"workspace": 2001},
    {
        "wid": 502,
        "rect": (4, 5, 25, 25),
        "resizable": True,
        "title": "bar",
        "name": "foo",
        "icon": Settings.BLANK_ICON,
        "workspace": 1002,
    },
]
ATTRS_FOR_VALID_TYPE = [
    {"wid": 101},
    {"rect": (55, 55, 100, 200)},
    {"resizable": True},
    {"title": "some title"},
    {"name": "name foo"},
    {"icon": Settings.BLANK_ICON},
    {"workspace": 1002},
]
ATTRS_INVALID_TYPE = [
    {"wid": 101.25},
    {"wid": "foo"},
    {"rect": ("a", 55, 100, 200)},
    {"rect": (55, 100, 200)},
    {"rect": (55, 100, 200, 500, 100)},
    {"resizable": "yes"},
    {"resizable": 0},
    {"resizable": -1},
    {"resizable": 1.0},
    {"title": 22},
    {"title": 22.5},
    {"title": 5},
    {"name": 78.34},
    {"name": WindowModel()},
    {"icon": "name"},
    {"workspace": "name"},
    {"workspace": 5.0},
]
VALID_MODEL_ATTRS = {
    "wid": 101,
    "rect": (55, 55, 100, 200),
    "resizable": True,
    "title": "some title",
    "name": "name foo",
    "icon": Settings.BLANK_ICON,
    "workspace": 1002,
}
INVALID_SINGLE_ATTR = [
    {"x": 100.0},
    {"y": "a"},
    {"w": WindowModel},
    {"h": WindowModel()},
    {"w": 50.0, "x": 50},
    {"xy": 100},
    {"wh": 10},
    {"xywh": 1000},
    {"foo": 999},
]
MODEL_SAME_VALUE = [
    {"x": SAMPLE_RECT[0]},
    {"y": SAMPLE_RECT[1]},
    {"x": SAMPLE_RECT[0], "y": SAMPLE_RECT[1], "w": SAMPLE_RECT[2]},
    {"w": SAMPLE_RECT[2]},
    {"w": SAMPLE_RECT[2], "x": SAMPLE_RECT[0]},
    {"rect": SAMPLE_RECT},
]
MODEL_INVALID_RECT = [
    {"rect": ("a", 0, 0, 200)},
    {"rect": (300, 155, 200)},
    {"rect": (30.0, 0, 155, 200)},
]
WINDOWSCOLLECTION_SORT_SAMPLES = [
    (((1004, 0), (1003, 1), (1004, 2), (1004, 3), (1006, 4)), [0, 2, 3, 4, 1]),
    (((0, 0), (2, 1), (1, 2), (0, 3), (1, 4)), [0, 3, 2, 4, 1]),
    (((2, 0), (1, 1), (1, 2), (4, 3), (2, 4)), [0, 4, 3, 1, 2]),
    (((2, 0), (1, 1), (2, 2), (0, 3), (2, 4)), [0, 2, 4, 3, 1]),
    (((2, 0), (1, 1), (2, 2)), [0, 2, 1]),
    (((0, 0), (1, 1), (2, 2)), [0, 1, 2]),
    (((0, 0),), [0]),
    (((0, 0), (1, 1)), [0, 1]),
    (((1, 0), (0, 1), (0, 2)), [0, 1, 2]),  # activates default value for next()
]
REPOPULATE_FOR_WID_SAMPLE = [
    ((100, 200, 300, 400, 500), 400, 200, [400, 500, 200, 300]),
    ((100, 200, 300, 400, 500, 600, 700, 800), 800, 700, [800, 700]),
    ((1, 2, 3, 4, 5, 6, 7, 8), 5, 4, [5, 6, 7, 8, 4]),
    ((1, 2, 3, 4, 5, 6, 7), 2, 1, [2, 3, 4, 5, 6, 7, 1]),
    ((1, 2, 3), 3, 1, [3, 1, 2]),
]
WINDOWSCOLLECTION_EXPORT = [
    (
        (
            {
                "wid": 501,
                "rect": (40, 50, 250, 425),
                "resizable": True,
                "title": "bar",
                "name": "foo",
                "icon": Settings.BLANK_ICON,
                "workspace": 1002,
            },
            (45, 55, 250, 425),
            1005,
        ),
        (
            {
                "wid": 502,
                "rect": (400, 500, 200, 300),
                "resizable": True,
                "title": "bar",
                "name": "foobar",
                "icon": Settings.BLANK_ICON,
                "workspace": 1004,
            },
            (400, 550, 300, 400),
            1004,
        ),
    ),
    (
        (
            {
                "wid": 503,
                "rect": (400, 500, 200, 300),
                "resizable": True,
                "title": "bar",
                "name": "foobar",
                "icon": Settings.BLANK_ICON,
                "workspace": 1004,
            },
            (400, 550, 300, 400),
            1004,
        ),
    ),
    (
        (
            {
                "wid": 504,
                "rect": (354, 50, 250, 425),
                "resizable": True,
                "title": "bar",
                "name": "foo",
                "icon": Settings.BLANK_ICON,
                "workspace": 1002,
            },
            (),
            1009,
        ),
    ),
    (
        (
            {
                "wid": 505,
                "rect": (427, 50, 250, 425),
                "resizable": True,
                "title": "bar",
                "name": "foo",
                "icon": Settings.BLANK_ICON,
                "workspace": 1002,
            },
            (),
            None,
        ),
    ),
]
WIN_COLLECTION_SNAP_CHANGED = [
    (
        (
            (1001, (10, 20, 500, 400), ()),
            (1002, (10, 20, 30, 40), (100, 200, 540, 200)),
        ),
        (
            {
                1001: [
                    (
                        (0, 10, 520, 30),
                        (500, 10, 520, 430),
                        (0, 410, 520, 430),
                        (0, 10, 20, 430),
                    )
                ],
                1002: [
                    (
                        (90, 190, 650, 210),
                        (630, 190, 650, 410),
                        (90, 390, 650, 410),
                        (90, 190, 110, 410),
                    )
                ],
            }
        ),
    )
]
WIN_COLLECTION_SNAP_SAMPLES = [
    (
        (
            (1001, 10, 20, 500, 400),
            (1001, 80, 200, 300, 200),
            (1002, 100, 200, 540, 200),
        ),
        (
            {
                1001: [
                    (
                        (0, 10, 520, 30),
                        (500, 10, 520, 430),
                        (0, 410, 520, 430),
                        (0, 10, 20, 430),
                    ),
                    (
                        (70, 190, 390, 210),
                        (370, 190, 390, 410),
                        (70, 390, 390, 410),
                        (70, 190, 90, 410),
                    ),
                ],
                1002: [
                    (
                        (90, 190, 650, 210),
                        (630, 190, 650, 410),
                        (90, 390, 650, 410),
                        (90, 190, 110, 410),
                    )
                ],
            }
        ),
    )
]

## test_utils
SAMPLE_SNAPPING_SOURCES_FOR_RECT = [
    (
        (10, 10, 100, 100),
        ((0, 0, 120, 20), (100, 0, 120, 120), (0, 100, 120, 120), (0, 0, 20, 120)),
    ),
    (
        (100, 10, 200, 300),
        ((90, 0, 310, 20), (290, 0, 310, 320), (90, 300, 310, 320), (90, 0, 110, 320)),
    ),
]
SAMPLE_CHECK_INTERSECTION = [
    (
        ((90, 0, 310, 20), (290, 0, 310, 320), (90, 300, 310, 320), (90, 0, 110, 320)),
        [
            (
                (0, 10, 520, 30),
                (500, 10, 520, 430),
                (0, 410, 520, 430),
                (0, 10, 20, 430),
            ),
            (
                (70, 190, 390, 210),
                (370, 190, 390, 410),
                (70, 390, 390, 410),
                (70, 190, 90, 410),
            ),
        ],
        (
            ((90, 0, 310, 20), (0, 10, 520, 30)),
            ((90, 0, 310, 20), (0, 10, 520, 30)),
            ((90, 0, 310, 20), (0, 10, 520, 30)),
            False,
            ((90, 0, 110, 320), (70, 190, 90, 410)),
        ),
    ),
    (
        (
            (
                (90, 190, 360, 210),
                (340, 190, 360, 410),
                (90, 390, 360, 410),
                (90, 190, 110, 410),
            )
        ),
        [
            (
                (390, 390, 560, 410),
                (540, 390, 560, 710),
                (390, 690, 560, 710),
                (390, 390, 410, 710),
            ),
            (
                (590, 390, 860, 410),
                (840, 390, 860, 910),
                (590, 890, 860, 910),
                (590, 390, 610, 910),
            ),
            (
                (390, 390, 760, 410),
                (740, 390, 760, 810),
                (390, 790, 760, 810),
                (390, 390, 410, 810),
            ),
        ],
        (False, False, False, False, False),
    ),
    (
        (
            (
                (
                    (390, 390, 910, 410),
                    (890, 390, 910, 910),
                    (390, 890, 910, 910),
                    (390, 390, 410, 910),
                )
            )
        ),
        [
            (
                (
                    (40, 30, 160, 50),
                    (140, 30, 160, 150),
                    (40, 130, 160, 150),
                    (40, 30, 60, 150),
                )
            ),
            (
                (
                    (990, 1190, 1310, 1210),
                    (1290, 1190, 1310, 1610),
                    (990, 1590, 1310, 1610),
                    (990, 1190, 1010, 1610),
                )
            ),
            (
                (
                    (
                        (385, 40, 605, 60),
                        (585, 40, 605, 460),
                        (385, 440, 605, 460),
                        (385, 40, 405, 460),
                    )
                )
            ),
        ],
        (
            ((390, 390, 410, 910), (385, 40, 405, 460)),
            ((390, 390, 410, 910), (385, 40, 405, 460)),
            False,
            False,
            ((390, 390, 410, 910), (385, 40, 405, 460)),
        ),
    ),
]
INTERSECTS_SAMPLES = [
    ((90, 0, 310, 20), (0, 10, 520, 30), True),
    ((90, 300, 310, 320), (0, 10, 520, 30), False),
    ((90, 0, 310, 20), (500, 10, 520, 440), False),
    ((290, 0, 310, 320), (500, 10, 520, 430), False),
    ((90, 300, 310, 320), (500, 10, 520, 430), False),
    ((0, 10, 520, 30), (370, 190, 390, 410), False),
    ((50, 50, 570, 70), (300, 60, 400, 80), True),
]

## test_base
def mock_main_loop(mocker):
    mocker.patch("arrangeit.base.get_tkinter_root")
    mocker.patch("arrangeit.base.ViewApplication")
    mocker.patch("arrangeit.base.BaseController.mainloop")
    mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
    mocker.patch("pynput.mouse.Listener")
    mocker.patch("pynput.mouse.Controller")
    mocker.patch("arrangeit.base.BaseApp.run_task")
    mocker.patch(
        "arrangeit.base.BaseApp.grab_window_screen",
        return_value=(mocker.MagicMock(), (0, 0)),
    )


def get_mocked_root(mocker):
    mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
    mocker.patch("arrangeit.base.ViewApplication")
    return mocker.patch("arrangeit.base.get_tkinter_root")


def get_mocked_viewapp(mocker):
    mocker.patch("arrangeit.base.get_tkinter_root")
    mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
    return mocker.patch("arrangeit.base.ViewApplication")


def mocked_viewapp(mocker):
    mocker.patch("arrangeit.base.get_tkinter_root")
    mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
    mocker.patch("arrangeit.base.ViewApplication")


def mocked_next(mocker):
    mocker.patch("arrangeit.base.get_tkinter_root")
    mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
    mocker.patch("arrangeit.base.ViewApplication")
    mocker.patch("arrangeit.base.BaseController.next")


def get_controller_with_mocked_app(mocker):
    app = mocker.MagicMock()
    app.grab_window_screen.return_value = (mocker.MagicMock(), (0, 0))
    return BaseController(app)


def run_controller_with_mocked_app(mocker):
    controller = get_controller_with_mocked_app(mocker)
    controller.run(mocker.MagicMock())
