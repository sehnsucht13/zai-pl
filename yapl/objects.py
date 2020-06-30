from yapl.object_type import ObjectType


class Internal_Object:
    """
    Base class for all internal objects used in the interpreter.
    """

    def __init__(self,):
        raise NotImplementedError()


class Num_Object(Internal_Object):
    def __init__(self, value):
        "Numeric object used to store integers."
        self.value = value
        self.obj_type = ObjectType.NUM

    def __repr__(self):
        return "NUM_OBJ {}".format(self.value)

    def __str__(self):
        return "NUM_OBJ {}".format(self.value)


class String_Object(Internal_Object):
    def __init__(self, string_val):
        """
        Internal object used to represent strings within the interpreter.
        """
        self.value = string_val
        self.obj_type = ObjectType.STR

    def __repr__(self):
        return "STR_OBJ {}".format(self.value)

    def __str__(self):
        return "STR_OBJ {}".format(self.value)


class Bool_Object(Internal_Object):
    def __init__(self, bool_val):
        """
        Internal object used to represent boolean values within the interpreter.
        """
        self.value = bool_val
        self.obj_type = ObjectType.BOOL

    def __str__(self):
        return "BOOL_OBJ {}".format(self.value)

    def __repr__(self):
        return "BOOL_OBJ {}".format(self.value)


class Func_Object(Internal_Object):
    def __init__(self, name, arg_symbols, body, env):
        """
        Internal object used to represent a function.
        """
        self.obj_type = ObjectType.FUNC
        self.name = name
        self.args = arg_symbols
        self.arity = len(arg_symbols)
        self.body = body
        # Reference to the current env
        self.env = env

    def __str__(self):
        return "FUNC_OBJ: Name: {}, Args: {}, Arity: {}, Body: {}".format(
            self.name, self.args, self.arity, self.body
        )


def is_atom(obj):
    """
    Check if an object is an atom(Boolean, Integer or string).
    """
    if obj is None:
        return False
    return obj.obj_type in [ObjectType.BOOL, ObjectType.NUM, ObjectType.STR]


def pprint_internal_object(internal_obj):
    """
    Pretty print an internal object depending on it's type.
    """
    if is_atom(internal_obj):
        print(internal_obj.value)
    elif internal_obj.obj_type == ObjectType.FUNC:
        output_str = "<function object {}>".format(internal_obj.name)
        print(output_str)
