import pytest

from arrangeit.data import WindowModel


WINDOW_MODEL_ATTRS = ['xy', 'size', 'wid', 'title']
SAMPLE_MODEL_VALUES = [
    {"xy": (45, 54)},
    {"size": (104, 105)},
    {"wid": 101},
    {"title": "foo"},
    {"xy": (4, 5), "size": (25, 25), "wid": 502, "title": "bar"},
]


class TestWindowModel(object):
    """Testing class for :py:mod:`arrangeit.model` module."""

    ## WindowModel
    @pytest.mark.parametrize("attr", WINDOW_MODEL_ATTRS)
    def test_WindowModel_inits_attr_as_None(self, attr):
        assert getattr(WindowModel, attr) is None

    ## WindowModel.__init__
    def test_WindowModel_initialization_calls_setup(self, mocker):
        mocker.patch("arrangeit.data.WindowModel.setup")
        WindowModel()
        WindowModel.setup.assert_called_once()

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
