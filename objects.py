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


def is_atom(object):
    """ Check if an object is an atom."""
    if object is None:
        return False
    return object.obj_type in [ObjectType.BOOL, ObjectType.NUM, ObjectType.STR]
