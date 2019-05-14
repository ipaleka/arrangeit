import platform

import pytest

from arrangeit.windows.collector import Collector


@pytest.mark.skipif(platform.system() != "Windows", reason="MS Windows only tests")
class TestWindowsCollector(object):
    """Testing class for :py:class:`arrangeit.windows.collector.Collector` class."""
