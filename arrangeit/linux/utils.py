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

from arrangeit import __appname__


def user_data_path():
    """Returns GNU/Linux platform specific path for saving user's data.

    It first try with .local/share in user home directory, and if there's
    no such directory returns .arrangeit directory in user home directory.

    :returns: str path
    """
    local = os.path.join("~", ".local", "share")
    if os.path.exists(os.path.expanduser(local)):
        return os.path.expanduser(os.path.join(local, __appname__))
    return os.path.expanduser(os.path.join("~", ".{}".format(__appname__)))
