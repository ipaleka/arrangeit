import pytest

from arrangeit import constants


class TestConstants(object):
    """Unit testing class checking availability of global constants."""

    @pytest.mark.parametrize(
        "constant,typ",
        [
            ("WINDOW_SHIFT_PIXELS", int),
        ],
    )
    def test_constants_for_name_and_typ(self, constant, typ):
        assert getattr(constants, constant) is not None
        assert isinstance(getattr(constants, constant), typ)