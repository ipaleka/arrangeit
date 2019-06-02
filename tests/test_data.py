from types import GeneratorType

import pytest

from arrangeit.settings import Settings
from arrangeit.data import WindowModel, WindowsCollection

from .fixtures import (
    SAMPLE_RECT,
    SAMPLE_MODEL_VALUES,
    ATTRS_FOR_VALID_TYPE,
    ATTRS_INVALID_TYPE,
    VALID_MODEL_ATTRS,
    INVALID_SINGLE_ATTR,
    MODEL_SAME_VALUE,
    MODEL_INVALID_RECT,
    WINDOWSCOLLECTION_SORT_SAMPLES,
    REPOPULATE_FOR_WID_SAMPLE,
    WINDOWSCOLLECTION_EXPORT,
)

WINDOW_MODEL_ATTRS = ["wid", "rect", "resizable", "title", "name", "icon", "workspace"]


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

    @pytest.mark.parametrize("values", ATTRS_FOR_VALID_TYPE)
    def test_WindowModel_setup_sets_attrs_for_valid_type(self, mocker, values):
        wm = WindowModel()
        wm.setup(**values)
        for key, val in values.items():
            assert getattr(wm, key) == val

    @pytest.mark.parametrize("values", ATTRS_INVALID_TYPE)
    def test_WindowModel_setup_set_None_or_empty_for_invalid_type(self, mocker, values):
        wm = WindowModel(**VALID_MODEL_ATTRS)
        wm.setup(**values)
        for key, _ in values.items():
            if key != "rect":
                assert getattr(wm, key) is None
            else:
                assert getattr(wm, key) == ()

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
                new[Settings.WINDOW_MODEL_RECT_ELEMENTS.index(elem)] = value
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
            new[Settings.WINDOW_MODEL_RECT_ELEMENTS.index(elem)] = value
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
            new[Settings.WINDOW_MODEL_RECT_ELEMENTS.index(elem)] = value
        new[3] = 444
        assert model.changed == tuple(new)

    @pytest.mark.parametrize("values", MODEL_SAME_VALUE)
    def test_WindowModel_set_changed_not_changing_same_value(self, values):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(**values)
        assert model.changed == ()

    @pytest.mark.parametrize("values", INVALID_SINGLE_ATTR)
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

    @pytest.mark.parametrize("values", MODEL_INVALID_RECT)
    def test_WindowModel_set_changed_creates_empty_tuple_invalid_rect(self, values):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(**values)
        assert model.changed == ()

    ## WindowModel.clear_changed
    def test_WindowModel_clear_changed_sets_changed_to_empty_tuple(self, mocker):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(rect=(200, 200, 200, 200))
        assert model.changed == (200, 200, 200, 200)
        model.clear_changed()
        assert model.changed == ()

    def test_WindowModel_clear_changed_sets_changed_ws_to_None(self, mocker):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(ws=1002)
        assert model.changed_ws == 1002
        model.clear_changed()
        assert model.changed_ws == None

    ## WindowModel.is_ws_changed
    @pytest.mark.parametrize(
        "changed_ws,ws,expected",
        [
            (None, 1001, False),
            (1002, 1002, False),
            (1002, 1001, True),
            (0, 0, False),
            (0, 1, True),
        ],
    )
    def test_WindowModel_is_ws_changed_functionality(self, changed_ws, ws, expected):
        model = WindowModel(workspace=ws)
        model.set_changed(ws=changed_ws)
        assert model.is_ws_changed is expected

    ## WindowModel.changed_x
    def test_WindowModel_changed_x_gets_x_from_changed(self):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(x=1000)
        assert model.changed_x == model.changed[0]

    def test_WindowModel_changed_x_gets_x_from_rect(self):
        model = WindowModel(rect=SAMPLE_RECT)
        assert model.changed_x == model.rect[0]

    ## WindowModel.changed_y
    def test_WindowModel_changed_y_gets_y_from_changed(self):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(y=1000)
        assert model.changed_y == model.changed[1]

    def test_WindowModel_changed_y_gets_y_from_rect(self):
        model = WindowModel(rect=SAMPLE_RECT)
        assert model.changed_y == model.rect[1]

    ## WindowModel.changed_w
    def test_WindowModel_changed_w_gets_w_from_changed(self):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(w=1000)
        assert model.changed_w == model.changed[2]

    def test_WindowModel_changed_w_gets_w_from_rect(self):
        model = WindowModel(rect=SAMPLE_RECT)
        assert model.changed_w == model.rect[2]

    ## WindowModel.changed_h
    def test_WindowModel_changed_h_gets_h_from_changed(self):
        model = WindowModel(rect=SAMPLE_RECT)
        model.set_changed(h=1000)
        assert model.changed_h == model.changed[3]

    def test_WindowModel_changed_h_gets_h_from_rect(self):
        model = WindowModel(rect=SAMPLE_RECT)
        assert model.changed_h == model.rect[3]

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
    @pytest.mark.parametrize("ws_wid,expected", WINDOWSCOLLECTION_SORT_SAMPLES)
    def test_WindowsCollection_sort_functionality(self, ws_wid, expected):
        collection = WindowsCollection()
        for elem in ws_wid:
            collection.add(WindowModel(workspace=elem[0], wid=elem[1]))
        collection.sort()
        assert expected == [model.wid for model in list(collection.generator())]

    ## WindowsCollection.get_windows_list
    def test_WindowsCollection_get_windows_calls_generator(self, mocker):
        mocked = mocker.patch("arrangeit.data.WindowsCollection.generator")
        WindowsCollection().get_windows_list()
        mocked.assert_called()

    def test_WindowsCollection_get_windows_list_returns_list_of_windows(self):
        collection = WindowsCollection()
        instance1 = WindowModel(wid=100, title="foo", icon=Settings.BLANK_ICON)
        instance2 = WindowModel(wid=200, title="bar", icon=Settings.BLANK_ICON)
        collection.add(instance1)
        collection.add(instance2)
        windows = collection.get_windows_list()
        assert windows == [
            (100, "foo", Settings.BLANK_ICON),
            (200, "bar", Settings.BLANK_ICON),
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

    ## WindowModel.get_model_by_wid
    def test_WindowsCollection_get_model_by_wid_valid_wid(self):
        collection = WindowsCollection()
        collection.add(WindowModel(wid=100))
        model = WindowModel(wid=200)
        collection.add(model)
        collection.add(WindowModel(wid=300))
        returned = collection.get_model_by_wid(200)
        assert returned == model

    def test_WindowsCollection_get_model_by_wid_invalid_wid(self):
        collection = WindowsCollection()
        collection.add(WindowModel(wid=100))
        collection.add(WindowModel(wid=200))
        returned = collection.get_model_by_wid(300)
        assert returned is None

    def test_WindowsCollection_get_model_by_wid_empty_collection(self):
        collection = WindowsCollection()
        returned = collection.get_model_by_wid(300)
        assert returned is None

    ## WindowModel.repopulate_for_wid
    @pytest.mark.parametrize(
        "elements,wid,remove_before,expected", REPOPULATE_FOR_WID_SAMPLE
    )
    def test_WindowsCollection_repopulate_for_wid_functionality(
        self, elements, wid, remove_before, expected
    ):
        collection = WindowsCollection()
        for elem in elements:
            collection.add(WindowModel(wid=elem))
        collection.repopulate_for_wid(wid, remove_before)
        assert expected == [model.wid for model in list(collection.generator())]

    ## WindowsCollection.export
    @pytest.mark.parametrize("elements", WINDOWSCOLLECTION_EXPORT)
    def test_WindowsCollection_export(self, elements):
        collection = WindowsCollection()
        for elem in elements:
            model = WindowModel(**elem[0])
            model.set_changed(rect=elem[1], ws=elem[2])
            collection.add(model)
        data = collection.export()
        assert len(data) == len(elements)
        assert all(len(elem) == 5 for elem in data)
        assert all(len(elem[0]) == 4 for elem in data)
        assert all(isinstance(elem[1], bool) for elem in data)
        assert all(isinstance(elem[2], str) for elem in data)
        assert all(isinstance(elem[3], str) for elem in data)
        assert all(isinstance(elem[4], int) for elem in data)
        assert all(
            elem[0] == elements[i][1] or elements[i][0]["rect"]
            for i, elem in enumerate(data)
        )
        assert all(
            elem[4] == elements[i][2] or elements[i][0]["workspace"]
            for i, elem in enumerate(data)
        )
