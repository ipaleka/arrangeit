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
# along with this program. If not, see <https://www.gnu.org/licenses/>

import types


"""
Helper module to test inner functions

http://code.activestate.com/recipes/580716-unit-testing-nested-functions/
"""


def freeVar(val):
    def nested():
        return val

    return nested.__closure__[0]


def nested(outer, innerName, **freeVars):
    if isinstance(outer, (types.FunctionType, types.MethodType)):
        outer = outer.__getattribute__("__code__")
    for const in outer.co_consts:
        if isinstance(const, types.CodeType) and const.co_name == innerName:
            return types.FunctionType(
                const,
                globals(),
                None,
                None,
                tuple(freeVar(freeVars[name]) for name in const.co_freevars),
            )
