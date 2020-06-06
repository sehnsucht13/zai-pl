from object_type import ObjectType


class Internal_Object:
    def __init__(self,):
        "Parent class of all internal objects."
        raise NotImplementedError()


class Num_Object(Internal_Object):
    def __init__(self, value):
        "Numeric object"
        self.value = value
        self.obj_type = ObjectType.NUM


class String_Object(Internal_Object):
    def __init__(self, string_val):
        "String object"
        self.value = string_val
        self.obj_type = ObjectType.STR


class Bool_Object(Internal_Object):
    def __init__(self, bool_val):
        "Boolean Value object."
        self.value = bool_val
        self.obj_type = ObjectType.BOOL


class Function_Object(Internal_Object):
    def __init__(self, name, arg_symbols, body, env):
        """Internal object used to represent a function."""
        self.obj_type = ObjectType.FUNC
        self.name = name
        self.args = arg_symbols
        self.arity = len(arg_symbols)
        self.body = body
        self.env = env


def is_atom(object):
    """ Check if an object is an atom."""
    if object is None:
        return False
    return object.obj_type in [ObjectType.BOOL, ObjectType.NUM, ObjectType.STR]
