"""
Module contains several classes used to represent internal objects within the interpreter.
"""
from enum import Enum, auto
from yapl.env import Scope


class ObjectType(Enum):
    """
    Enum used to represent the different types of internal objects.
    """

    NUM = auto()
    STR = auto()
    ID = auto()
    BOOL = auto()
    FUNC = auto()
    CLASS_DEF = auto()
    CLASS_INSTANCE = auto()
    CLASS_METHOD = auto()
    RETURN = auto()
    NIL = auto()
    BREAK = auto()
    CONTINUE = auto()


class Internal_Object:
    """
    Base class for all internal objects used in the interpreter.
    """

    def __init__(self,):
        raise NotImplementedError()


class Num_Object(Internal_Object):
    """
    Numeric internal object used to store integers.
    """

    def __init__(self, value):
        self.value = value
        self.obj_type = ObjectType.NUM

    def __repr__(self):
        return "NUM_OBJ {}".format(self.value)

    def __str__(self):
        return "NUM_OBJ {}".format(self.value)

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.obj_type == other.obj_type and self.value == other.value


class String_Object(Internal_Object):
    """
    Internal object used to represent strings within the interpreter.
    """

    def __init__(self, string_val):
        self.value = string_val
        self.obj_type = ObjectType.STR

    def __repr__(self):
        return "STR_OBJ {}".format(self.value)

    def __str__(self):
        return "STR_OBJ {}".format(self.value)

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.obj_type == other.obj_type and self.value == other.value


class Return_Object(Internal_Object):
    """
    Internal object used to represent return objects within the interpreter.
    """

    def __init__(self, return_val=None):
        self.value = return_val
        self.obj_type = ObjectType.RETURN

    def __str__(self):
        return "RETURN_OBJ {}".format(self.value)

    def __repr__(self):
        return "RETURN_OBJ {}".format(self.value)

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.obj_type == other.obj_type and self.value == other.value


class Nil_Object(Internal_Object):
    """
    Internal object used to represent nil/null values.
    """

    def __init__(self):
        self.obj_type = ObjectType.NIL

    def __str__(self):
        return "RETURN_OBJ"

    def __repr__(self):
        return "RETURN_OBJ"

    def __eq__(self, other):
        return self.obj_type == other.obj_type


class Break_Object(Internal_Object):
    """
    Internal object used to break statements produced during code execution.
    """

    def __init__(self):
        self.obj_type = ObjectType.BREAK

    def __str__(self):
        return "BREAK_OBJ"

    def __repr__(self):
        return "BREAK_OBJ"

    def __eq__(self, other):
        return self.obj_type == other.obj_type


class Continue_Object(Internal_Object):
    """
    Internal object used to continue statements produced during code execution.
    """

    def __init__(self):
        self.obj_type = ObjectType.CONTINUE

    def __str__(self):
        return "CONTINUE_OBJ"

    def __repr__(self):
        return "CONTINUE_OBJ"

    def __eq__(self, other):
        return self.obj_type == other.obj_type


class Bool_Object(Internal_Object):
    """
    Internal object used to represent a return value from a function.
    """

    def __init__(self, bool_val):
        self.value = bool_val
        self.obj_type = ObjectType.BOOL

    def __str__(self):
        return "BOOL_OBJ {}".format(self.value)

    def __repr__(self):
        return "BOOL_OBJ {}".format(self.value)

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.obj_type == other.obj_type and self.value == other.value


class Func_Object(Internal_Object):
    """
    Internal object used to represent a function.
    """

    def __init__(self, name, arg_symbols, body, env):
        self.obj_type = ObjectType.FUNC
        self.name = name
        self.args = arg_symbols
        self.arity = len(arg_symbols)
        self.body = body
        # Reference to the current env
        self.env = env

    def __str__(self):
        return "FUNC_OBJ: Name: {}, Args: {}, Arity: {}".format(
            self.name, self.args, self.arity,
        )


class Class_Def_Object(Internal_Object):
    def __init__(self, class_name, class_methods):
        "setup class object"
        self.obj_type = ObjectType.CLASS_DEF
        self.class_name = class_name
        self.class_methods = class_methods

    def __str__(self):
        return "CLASS_OBJ: Name: {}".format(self.class_name)


class Class_Method_Object(Internal_Object):
    """
    Internal object used to represent a class function.
    """

    def __init__(self, name, arg_symbols, body, class_env):
        self.obj_type = ObjectType.CLASS_METHOD
        self.name = name
        self.args = arg_symbols
        self.arity = len(arg_symbols)
        self.body = body
        # Reference to the class env
        self.class_env = class_env

    def __str__(self):
        return "CLASS_METHOD_OBJ: Name: {}, Args: {}, Arity: {}".format(
            self.name, self.args, self.arity,
        )


class Class_Instance_Object(Internal_Object):
    def __init__(self, class_name, class_methods):
        "Object representing a class instance."
        self.obj_type = ObjectType.CLASS_INSTANCE
        self.class_name = class_name
        self.internal_namespace = Scope(None)

        # Register all class methods in the internal environment
        for method in class_methods:
            self.internal_namespace.add_symbol(
                method.name,
                Class_Method_Object(
                    method.name, method.args, method.body, self.internal_namespace
                ),
                True,
            )
        # "field" is a test variable used to check access before implementing assignment of
        # class instance fields.
        self.internal_namespace.add_symbol("field", Num_Object(13), True)

        # print(self.internal_namespace.scope)

    def get_field(self, field_name):
        return self.internal_namespace.lookup_symbol(field_name)


def pprint_internal_object(internal_obj):
    """
    Pretty print an internal object depending on it's type.
    """
    if is_atom(internal_obj):
        print(internal_obj.value)
    elif internal_obj.obj_type == ObjectType.FUNC:
        output_str = "<function object {}>".format(internal_obj.name)
        print(output_str)
    elif internal_obj.obj_type == ObjectType.CLASS_DEF:
        output_str = "<class definition object {}>".format(internal_obj.class_name)
        print(output_str)
    elif internal_obj.obj_type == ObjectType.CLASS_INSTANCE:
        output_str = "<class instance object {}>".format(internal_obj.class_name)
        print(output_str)


def is_truthy(internal_object):
    """ Check if an internal object is truthy. Returns True or False."""
    # Truthiness will be the same as the one in python
    if internal_object.obj_type in [ObjectType.BOOL, ObjectType.STR, ObjectType.NUM]:
        return bool(internal_object.value)


def is_atom(obj):
    """
    Check if an object is an atom(Boolean, Integer or string).
    """
    if obj is None:
        return False
    return obj.obj_type in [ObjectType.BOOL, ObjectType.NUM, ObjectType.STR]
