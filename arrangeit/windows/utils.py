# arrangeit - cross-platform desktop utility for easy windows management
# Copyright (C) 1999-2019 Ivica Paleka

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import sys

from arrangeit import __appname__


def extract_name_from_bytes_path(path):
    """Returns name without directory structure and extension from given path.

    :param path: full path to file
    :type path: bytes
    :returns: str
    """
    return os.path.splitext(os.path.basename(path))[0].decode(sys.getdefaultencoding())


def user_data_path():
    """Returns MS Windows specific path for saving user's data."""
    return os.path.expanduser(os.path.join("~", __appname__))
