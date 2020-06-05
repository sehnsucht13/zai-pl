from object_type import ObjectType


class Internal_Object:
    def __init__(self,):
        "Parent class of all internal objects."
        raise NotImplementedError()


class Num_Object(Internal_Object):
    def __init__(self, value):
        "Numeric object"
        self.obj_type = ObjectType.NUM
        self.value = value


class String_Object(Internal_Object):
    def __init__(self, string_val):
        "String object"
        self.value = string_val
        self.obj_type = ObjectType.STR


class Bool_Object(Internal_Object):
    def __init__(self, bool_val):
        "Boolean Value object."
        self.bool_val = bool_val
        self.obj_type = ObjectType.BOOL
