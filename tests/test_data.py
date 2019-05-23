from types import GeneratorType

import pytest

from arrangeit import constants
from arrangeit.data import WindowModel, WindowsCollection


WINDOW_MODEL_ATTRS = ["wid", "rect", "resizable", "title", "name", "icon", "workspace"]
SAMPLE_RECT = (45, 54, 304, 405)
SAMPLE_MODEL_VALUES = [
    {"wid": 101},
    {"rect": SAMPLE_RECT},
    {"resizable": True},
    {"title": "foo"},
    {"name": "bar"},
    {"icon": constants.BLANK_ICON},
    {"workspace": 2001},
    {
        "wid": 502,
        "rect": (4, 5, 25, 25),
        "resizable": True,
        "title": "bar",
        "name": "foo",
        "icon": constants.BLANK_ICON,
        "workspace": 1002,
    },
]


class TestWindowModel(object):
    """Testing class for :py:class:`arrangeit.data.WindowModel` class."""

    ## WindowModel
    @pytest.mark.parametrize("attr", WINDOW_MODEL_ATTRS)
    def test_WindowModel_inits_attr_as_None_or_empty_tuple(self, attr):
        if attr != "rect":
            assert getattr(WindowModel, attr) is None
        else:
            assert getattr(WindowModel, attr) == ()

    def test_WindowModel_inits_changed_as_empty_tuple(self):
        assert WindowModel.changed == ()

    def test_WindowModel_inits_changed_ws_as_None(self):
        assert WindowModel.changed_ws == None

    ## WindowModel.__init__
    def test_WindowModel_initialization_calls_setup(self, mocker):
        mocked = mocker.patch("arrangeit.data.WindowModel.setup")
        WindowModel()
        mocked.assert_called_once()

    ## WindowModel.setup
    @pytest.mark.parametrize("values", SAMPLE_MODEL_VALUES)
    def test_WindowModel_setup_calls_get_value_if_valid_type_for_all(
        self, mocker, values
    ):
        mocked = mocker.patch("arrangeit.data.get_value_if_valid_type")
        wm = WindowModel()
        wm.setup(**values)
        assert mocked.call_count == 2 * len(WINDOW_MODEL_ATTRS)

    @pytest.mark.parametrize("values", SAMPLE_MODEL_VALUES)
    def test_WindowModel_setup_sets_attrs_if_provided(self, mocker, values):
        wm = WindowModel()
        wm.setup(**values)
        for key, val in values.items():
            assert getattr(wm, key) == val

    @pytest.mark.parametrize("values", SAMPLE_MODEL_VALUES)
    def test_WindowModel_setup_sets_None_for_values_not_provided(self, mocker, values):
        wm = WindowModel()
        wm.setup(**values)
        for key in WINDOW_MODEL_ATTRS:
            if key not in values.keys():
                assert getattr(wm, key) is None

    @pytest.mark.parametrize(
        "values",
        [
            {"wid": 101},
            {"rect": (55, 55, 100, 200)},
            {"resizable": True},
            {"title": "some title"},
            {"name": "name foo"},
            {"icon": constants.BLANK_ICON},
            {"workspace": 1002},
        ],
    )
    def test_WindowModel_setup_sets_attrs_for_valid_type(self, mocker, values):
        wm = WindowModel()
        wm.setup(**values)
        for key, val in values.items():
            assert getattr(wm, key) == val

    @pytest.mark.parametrize(
        "values",
        [
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
        ],
    )
    def test_WindowModel_setup_set_None_or_empty_for_invalid_type(self, mocker, values):
        good = {
            "wid": 101,
            "rect": (55, 55, 100, 200),
            "resizable": True,
            "title": "some title",
            "name": "name foo",
            "icon": constants.BLANK_ICON,
            "workspace": 1002,
        }
        wm = WindowModel(**good)
        wm.setup(**values)
        for key, _ in values.items():
            if key != "rect":
                assert getattr(wm, key) is None
            else:
                assert getattr(wm, key) == ()

    ## WindowModel.wh_from_ending_xy
    @pytest.mark.parametrize(
        "x,y,old_x,old_y",
        [(200, 300, 100, 200), (100, 100, 50, 50), (1500, 200, 1400, 100)],
    )
    def test_WindowModel_wh_from_ending_xy_for_greater_xy(self, x, y, old_x, old_y):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(x=old_x, y=old_y)
        wh = model.wh_from_ending_xy(x, y)
        assert wh == (x - old_x, y - old_y)

    @pytest.mark.parametrize(
        "x,y,old_x,old_y",
        [(200, 300, 201, 200), (100, 100, 50, 500), (1500, 200, 1600, 300)],
    )
    def test_WindowModel_wh_from_ending_xy_for_invalid_xy(self, x, y, old_x, old_y):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(x=old_x, y=old_y)
        wh = model.wh_from_ending_xy(x, y)
        assert wh == (None, None)

    ## WindowModel.set_changed
    @pytest.mark.parametrize("ws", [1000, 0, 2002, 1])
    def test_WindowModel_set_changed_sets_changed_ws_for_provided_ws(self, ws):
        model = WindowModel(workspace=3009)
        model.set_changed(ws=ws)
        assert model.changed_ws == ws

    @pytest.mark.parametrize("ws", [1000.0, 0.0, "2002", "1"])
    def test_WindowModel_set_changed_sets_changed_ws_to_None_for_invalid(self, ws):
        model = WindowModel(workspace=3009)
        model.set_changed(ws=ws)
        assert model.changed_ws is None

    @pytest.mark.parametrize(
        "values",
        [
            {"ws": 7001, "x": 500},
            {"ws": 9001, "x": 500, "y": 400},
            {"ws": 0, "rect": (100, 100, 100, 100)},
        ],
    )
    def test_WindowModel_set_changed_sets_changed_ws_and_changed(self, values):
        model = WindowModel(rect=SAMPLE_RECT, workspace=2002)
        model.set_changed(**values)
        new = list(model.rect)
        new_ws = None
        for elem, value in values.items():
            if elem == "ws":
                new_ws = value
            elif elem == "rect":
                new = value[:]
            else:
                new[constants.WINDOW_RECT_ELEMENTS.index(elem)] = value
        assert model.changed == tuple(new)
        assert model.changed_ws == new_ws

    @pytest.mark.parametrize(
        "values",
        [
            {"x": 100},
            {"y": 200},
            {"x": 100, "y": 50, "w": 40, "h": 100},
            {"w": 300},
            {"h": 400},
            {"w": 300, "x": 50},
        ],
    )
    def test_WindowModel_set_changed_creates_from_rect_elements_rect(self, values):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(**values)
        new = list(model.rect)
        for elem, value in values.items():
            new[constants.WINDOW_RECT_ELEMENTS.index(elem)] = value
        assert model.changed == tuple(new)

    @pytest.mark.parametrize(
        "values",
        [
            {"x": 100},
            {"y": 200},
            {"x": 100, "y": 50, "w": 40},
            {"w": 300},
            {"w": 300, "x": 50},
        ],
    )
    def test_WindowModel_set_changed_creates_from_rect_elements_changed(self, values):
        model = WindowModel(rect=SAMPLE_RECT)
        changed = list(SAMPLE_RECT)
        changed[3] = 444
        model.changed = tuple(changed)
        model.set_changed(**values)
        new = list(model.rect)
        for elem, value in values.items():
            new[constants.WINDOW_RECT_ELEMENTS.index(elem)] = value
        new[3] = 444
        assert model.changed == tuple(new)

    @pytest.mark.parametrize(
        "values",
        [
            {"x": 100.0},
            {"y": "a"},
            {"w": WindowModel},
            {"h": WindowModel()},
            {"w": 50.0, "x": 50},
            {"xy": 100},
            {"wh": 10},
            {"xywh": 1000},
            {"foo": 999},
        ],
    )
    def test_WindowModel_set_changed_creates_empty_tuple_for_invalid(self, values):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(**values)
        assert model.changed == ()

    @pytest.mark.parametrize(
        "values", [{"rect": (10, 0, 0, 200)}, {"rect": (300, 50, 155, 200)}]
    )
    def test_WindowModel_set_changed_creates_from_rect(self, values):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(**values)
        assert model.changed == values["rect"]

    @pytest.mark.parametrize(
        "values",
        [
            {"rect": ("a", 0, 0, 200)},
            {"rect": (300, 155, 200)},
            {"rect": (30.0, 0, 155, 200)},
        ],
    )
    def test_WindowModel_set_changed_creates_empty_tuple_invalid_rect(self, values):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(**values)
        assert model.changed == ()

    ## WindowModel.x
    def test_WindowModel_x_gets_x_from_rect(self):
        model = WindowModel(rect=SAMPLE_RECT)
        assert model.x == model.rect[0]

    ## WindowModel.y
    def test_WindowModel_y_gets_y_from_rect(self):
        model = WindowModel(rect=SAMPLE_RECT)
        assert model.y == model.rect[1]

    ## WindowModel.w
    def test_WindowModel_w_gets_width_from_rect(self):
        model = WindowModel(rect=SAMPLE_RECT)
        assert model.w == model.rect[2]

    ## WindowModel.h
    def test_WindowModel_h_gets_height_from_rect(self):
        model = WindowModel(rect=SAMPLE_RECT)
        assert model.h == model.rect[3]

    ## WindowModel.ws
    def test_WindowModel_ws_is_alias_for_workspace(self):
        model = WindowModel(workspace=5002)
        assert model.ws == model.workspace


class TestWindowsCollection(object):
    """Testing class for :py:class:`arrangeit.data.WindowsCollection` class."""

    ## WindowsCollection
    def test_WindowsCollection_inits_____members_as_None(self):
        assert WindowsCollection._members is None

    ## WindowsCollection.__init__
    def test_WindowsCollection_initialization_sets_empty__members(self):
        assert isinstance(WindowsCollection()._members, list)
        assert len(WindowsCollection()._members) == 0

    ## WindowsCollection.size
    def test_WindowsCollection_size_is_property(self):
        assert isinstance(type(WindowsCollection()).size, property)

    def test_WindowsCollection_size_returns__members_length(self):
        collection = WindowsCollection()
        assert collection._members == []
        assert collection.size == 0
        collection._members = [WindowModel(), WindowModel()]
        assert collection.size == 2

    ## WindowsCollection.clear
    def test_WindowsCollection_clear_empties__members(self):
        collection = WindowsCollection()
        assert collection._members == []
        collection.add(WindowModel())
        collection.add(WindowModel())
        assert collection.size == 2
        collection.clear()
        assert collection.size == 0

    ## WindowsCollection.sort
    @pytest.mark.skip(reason="waiting for tkinter widgets functionality")
    @pytest.mark.parametrize("wses", [(1004, 1003, 1004, 1004, 1006), (0, 3, 1, 0, 1)])
    def test_WindowsCollection_sort_functionality(self, wses):
        assert False

    ## WindowsCollection.get_windows_list
    def test_WindowsCollection_get_windows_calls_generator(self, mocker):
        mocked = mocker.patch("arrangeit.data.WindowsCollection.generator")
        WindowsCollection().get_windows_list()
        mocked.assert_called()

    def test_WindowsCollection_get_windows_list_returns_list_of_windows(self):
        collection = WindowsCollection()
        instance1 = WindowModel(wid=100, title="foo", icon=constants.BLANK_ICON)
        instance2 = WindowModel(wid=200, title="bar", icon=constants.BLANK_ICON)
        collection.add(instance1)
        collection.add(instance2)
        windows = collection.get_windows_list()
        assert windows == [
            (100, "foo", constants.BLANK_ICON),
            (200, "bar", constants.BLANK_ICON),
        ]

    ## WindowsCollection.add
    @pytest.mark.parametrize("arg", [0, -0.1, "hej", object, WindowModel])
    def test_WindowsCollection_add_raises_for_invalid_argument(self, arg):
        with pytest.raises(ValueError):
            WindowsCollection().add(arg)

    def test_WindowsCollection_add_appends_one_element_to__members(self):
        collection = WindowsCollection()
        assert collection.size == 0
        collection.add(WindowModel())
        assert collection.size == 1

    def test_WindowsCollection_generator_type(self):
        assert isinstance(WindowsCollection().generator(), GeneratorType)

    def test_WindowsCollection_generator_next_yields_value(self):
        collection = WindowsCollection()
        assert collection.size == 0
        instance1 = WindowModel()
        instance2 = WindowModel()
        collection.add(instance1)
        collection.add(instance2)
        generator = collection.generator()
        assert next(generator) == instance1
        assert next(generator) == instance2
        with pytest.raises(StopIteration):
            next(generator)


@pytest.mark.asyncio
class TestAsyncWindowsCollection(object):
    """Testing class for :py:class:`arrangeit.data.WindowsCollection` async methods."""

    ## WindowModel.get_model_by_wid
    async def test_WindowsCollection_get_model_by_wid_valid_wid(self):
        collection = WindowsCollection()
        collection.add(WindowModel(wid=100))
        model = WindowModel(wid=200)
        collection.add(model)
        collection.add(WindowModel(wid=300))
        returned = await collection.get_model_by_wid(200)
        assert returned == model

    @pytest.mark.asyncio
    async def test_WindowsCollection_get_model_by_wid_invalid_wid(self):
        collection = WindowsCollection()
        collection.add(WindowModel(wid=100))
        collection.add(WindowModel(wid=200))
        returned = await collection.get_model_by_wid(300)
        assert returned is None

    @pytest.mark.asyncio
    async def test_WindowsCollection_get_model_by_wid_empty_collection(self):
        collection = WindowsCollection()
        returned = await collection.get_model_by_wid(300)
        assert returned is None
