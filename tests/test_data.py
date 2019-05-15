import pytest

from arrangeit.data import WindowModel, WindowsCollection


WINDOW_MODEL_ATTRS = ["wid", "rect", "resizable", "title", "name"]
SAMPLE_MODEL_VALUES = [
    {"wid": 101},
    {"rect": (45, 54, 304, 405)},
    {"resizable": True},
    {"title": "foo"},
    {"name": "bar"},
    {
        "wid": 502,
        "rect": (4, 5, 25, 25),
        "resizable": True,
        "title": "bar",
        "name": "foo",
    },
]


class TestWindowModel(object):
    """Testing class for :py:class:`arrangeit.data.WindowModel` class."""

    ## WindowModel
    @pytest.mark.parametrize("attr", WINDOW_MODEL_ATTRS)
    def test_WindowModel_inits_attr_as_None(self, attr):
        assert getattr(WindowModel, attr) is None

    ## WindowModel.__init__
    def test_WindowModel_initialization_calls_setup(self, mocker):
        mocked = mocker.patch("arrangeit.data.WindowModel.setup")
        WindowModel()
        mocked.assert_called_once()

    ## WindowModel.setup
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


class TestWindowsCollection(object):
    """Testing class for :py:class:`arrangeit.data.WindowsCollection` class."""

    ## WindowModel
    def test_WindowsCollection_inits_____members_as_None(self):
        assert WindowsCollection._members is None

    ## WindowsCollection.__init__
    def test_WindowsCollection_initialization_sets_empty__members(self):
        assert isinstance(WindowsCollection()._members, list)
        assert len(WindowsCollection()._members) == 0

    def test_WindowsCollection_size_is_property(self):
        assert isinstance(type(WindowsCollection()).size, property)

    def test_WindowsCollection_size_returns__members_length(self):
        collection = WindowsCollection()
        assert collection._members == []
        assert collection.size == 0
        collection._members = [WindowModel(), WindowModel()]
        assert collection.size == 2

    def test_WindowsCollection_clear_empties__members(self):
        collection = WindowsCollection()
        assert collection._members == []
        collection.add(WindowModel())
        collection.add(WindowModel())
        assert collection.size == 2
        collection.clear()
        assert collection.size == 0

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
        from types import GeneratorType

        assert isinstance(WindowsCollection().generator(), GeneratorType)

    def test_next_on_WindowsCollection_generator_yields_value(self):
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
