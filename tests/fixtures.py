from arrangeit.data import WindowModel
from arrangeit.settings import Settings
from arrangeit.utils import Rectangle

## test_data
SAMPLE_RECT = (45, 54, 304, 405)
SAMPLE_MODEL_VALUES = [
    {"wid": 101},
    {"rect": SAMPLE_RECT},
    {"resizable": True},
    {"restored": True},
    {"title": "foo"},
    {"name": "bar"},
    {"icon": Settings.BLANK_ICON},
    {"workspace": 2001},
    {
        "wid": 502,
        "rect": (4, 5, 25, 25),
        "resizable": True,
        "restored": True,
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
    {"restored": True},
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
    {"restored": "no"},
    {"restored": 9},
    {"restored": -85},
    {"restored": 2.0},
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
    "restored": True,
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
                "restored": True,
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
                "restored": True,
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
                "restored": True,
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
                "restored": True,
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
                "restored": True,
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
WIN_COLLECTION_SNAP_SAMPLES_EXCLUDING = [
    (
        ((1001, 10, 20, 500, 400), (1001, 80, 200, 300, 200)),
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
                ]
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
SAMPLE_CHECK_INTERSECTIONS = [
    (
        (
            Rectangle(90, 0, 310, 20),
            Rectangle(290, 0, 310, 320),
            Rectangle(90, 300, 310, 320),
            Rectangle(90, 0, 110, 320),
        ),
        [
            (
                Rectangle(0, 10, 520, 30),
                Rectangle(500, 10, 520, 430),
                Rectangle(0, 410, 520, 430),
                Rectangle(0, 10, 20, 430),
            ),
            (
                Rectangle(70, 190, 390, 210),
                Rectangle(370, 190, 390, 410),
                Rectangle(70, 390, 390, 410),
                Rectangle(70, 190, 90, 410),
            ),
        ],
        (
            (
                ((90, 0, 310, 20), (0, 10, 520, 30)),
                ((90, 0, 110, 320), (70, 190, 90, 410)),
            ),
            (
                ((90, 0, 310, 20), (0, 10, 520, 30)),
                ((90, 0, 110, 320), (70, 190, 90, 410)),
            ),
            ((90, 0, 310, 20), (0, 10, 520, 30)),
            False,
            ((90, 0, 110, 320), (70, 190, 90, 410)),
        ),
    ),
    (
        (
            (
                Rectangle(90, 190, 360, 210),
                Rectangle(340, 190, 360, 410),
                Rectangle(90, 390, 360, 410),
                Rectangle(90, 190, 110, 410),
            )
        ),
        [
            (
                Rectangle(390, 390, 560, 410),
                Rectangle(540, 390, 560, 710),
                Rectangle(390, 690, 560, 710),
                Rectangle(390, 390, 410, 710),
            ),
            (
                Rectangle(590, 390, 860, 410),
                Rectangle(840, 390, 860, 910),
                Rectangle(590, 890, 860, 910),
                Rectangle(590, 390, 610, 910),
            ),
            (
                Rectangle(390, 390, 760, 410),
                Rectangle(740, 390, 760, 810),
                Rectangle(390, 790, 760, 810),
                Rectangle(390, 390, 410, 810),
            ),
        ],
        (False, False, False, False, False),
    ),
    (
        (
            (
                (
                    Rectangle(390, 390, 910, 410),
                    Rectangle(890, 390, 910, 910),
                    Rectangle(390, 890, 910, 910),
                    Rectangle(390, 390, 410, 910),
                )
            )
        ),
        [
            (
                (
                    Rectangle(40, 30, 160, 50),
                    Rectangle(140, 30, 160, 150),
                    Rectangle(40, 130, 160, 150),
                    Rectangle(40, 30, 60, 150),
                )
            ),
            (
                (
                    Rectangle(990, 1190, 1310, 1210),
                    Rectangle(1290, 1190, 1310, 1610),
                    Rectangle(990, 1590, 1310, 1610),
                    Rectangle(990, 1190, 1010, 1610),
                )
            ),
            (
                (
                    (
                        Rectangle(385, 40, 605, 60),
                        Rectangle(585, 40, 605, 460),
                        Rectangle(385, 440, 605, 460),
                        Rectangle(385, 40, 405, 460),
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
    (Rectangle(90, 0, 310, 20), Rectangle(0, 10, 520, 30), True),
    (Rectangle(90, 300, 310, 320), Rectangle(0, 10, 520, 30), False),
    (Rectangle(90, 0, 310, 20), Rectangle(500, 10, 520, 440), False),
    (Rectangle(290, 0, 310, 320), Rectangle(500, 10, 520, 430), False),
    (Rectangle(90, 300, 310, 320), Rectangle(500, 10, 520, 430), False),
    (Rectangle(0, 10, 520, 30), Rectangle(370, 190, 390, 410), False),
    (Rectangle(50, 50, 570, 70), Rectangle(300, 60, 400, 80), True),
]
OFFSET_INTERSECTING_PAIR_SAMPLES = {
    0: [
        ((Rectangle(1732, 36, 1752, 316), Rectangle(1725, 22, 1745, 868)), (-7, 0)),
        ((Rectangle(257, 52, 747, 72), Rectangle(169, 51, 1123, 71)), (0, -1)),
        ((Rectangle(1112, 206, 1132, 486), Rectangle(1113, 51, 1133, 791)), (1, 0)),
        ((Rectangle(166, 114, 186, 394), Rectangle(169, 51, 189, 791)), (3, 0)),
        ((Rectangle(143, 276, 633, 296), Rectangle(58, 267, 1012, 287)), (0, -9)),
        ((Rectangle(489, 29, 989, 49), Rectangle(269, 36, 1215, 56)), (0, 7)),
    ],
    1: [
        ((Rectangle(233, 641, 733, 661), Rectangle(138, 636, 804, 656)), (0, -5)),
        ((Rectangle(1283, 254, 1303, 544), Rectangle(1276, 56, 1296, 1040)), (-7, 0)),
        ((Rectangle(197, 655, 697, 675), Rectangle(138, 636, 804, 656)), (0, -19)),
        ((Rectangle(572, 314, 592, 604), Rectangle(574, 153, 594, 696)), (2, 0)),
    ],
    2: [
        ((Rectangle(335, 624, 835, 644), Rectangle(247, 635, 913, 655)), (0, 11)),
        ((Rectangle(202, 460, 702, 480), Rectangle(167, 444, 833, 464)), (0, -16)),
        ((Rectangle(811, 461, 831, 751), Rectangle(813, 444, 833, 987)), (2, 0)),
        ((Rectangle(470, 384, 490, 674), Rectangle(469, 394, 489, 937)), (-1, 0)),
    ],
    3: [
        ((Rectangle(1062, 204, 1082, 494), Rectangle(1078, 119, 1098, 854)), (16, 0)),
        ((Rectangle(159, 158, 179, 448), Rectangle(163, 119, 183, 854)), (4, 0)),
        ((Rectangle(465, 850, 965, 870), Rectangle(163, 834, 1098, 854)), (0, -16)),
        ((Rectangle(1505, 938, 2005, 958), Rectangle(1323, 924, 2959, 944)), (0, -14)),
    ],
}
ROOT_SNAPPING_RECTANGLES_SOURCES = (
    Rectangle(819, 297, 1278, 301),
    Rectangle(1274, 297, 1278, 557),
    Rectangle(819, 553, 1278, 557),
    Rectangle(819, 297, 823, 557),
)
