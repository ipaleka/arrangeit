import platform

import pytest

from arrangeit.darwin.collector import Collector


@pytest.mark.skipif(platform.system() != "Darwin", reason="Mac OS only tests")
class TestDarwinCollector(object):
    """Testing class for :py:class:`arrangeit.darwin.collector.Collector` class."""

