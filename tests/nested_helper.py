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

