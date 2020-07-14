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
    ARRAY = auto()
    MODULE = auto()


class Internal_Object:
    """
    Base class for all internal objects used in the interpreter.
    """

    def __init__(self,):
        raise NotImplementedError()


# All atomic objects
class Nil_Object(Internal_Object):
    """
    Internal object used to represent nil/null values.
    """

    def __init__(self):
        self.obj_type = ObjectType.NIL

    def __str__(self):
        return "NIL_OBJ"

    def __repr__(self):
        return "NIL_OBJ"

    def __eq__(self, other):
        return self.obj_type == other.obj_type

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __neg__(self):
        pass

    def __invert__(self):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass


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
        if other is None:
            return False
        else:
            return self.obj_type == other.obj_type and self.value == other.value

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __neg__(self):
        pass

    def __invert__(self):
        pass


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
        if other is None:
            return False
        else:
            return self.obj_type == other.obj_type and self.value == other.value

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __neg__(self):
        pass

    def __invert__(self):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass


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
        # print("comparison from object", self, other)
        if other is None:
            return False
        else:
            return self.obj_type == other.obj_type and self.value == other.value

    def __add__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.BOOL]:
            return Num_Object(self.value + other.value)

    def __sub__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.BOOL]:
            return Num_Object(self.value - other.value)

    def __mul__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.BOOL]:
            return Num_Object(self.value * other.value)
        elif other.obj_type in ObjectType.STR:
            return String_Object(other.value * self.value)

    def __truediv__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.BOOL]:
            return Num_Object(self.value / other.value)

    def __lt__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.BOOL]:
            return Num_Object(self.value < other.value)

    def __le__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.BOOL]:
            return Num_Object(self.value <= other.value)

    def __gt__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.BOOL]:
            return Num_Object(self.value > other.value)

    def __ge__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.BOOL]:
            return Num_Object(self.value >= other.value)

    def __eq__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.BOOL]:
            return Bool_Object(self.value == other.value)

    def __ne__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.BOOL]:
            return Bool_Object(self.value != other.value)

    def __neg__(self):
        return Num_Object(-self.value)

    def __invert__(self):
        return Bool_Object(not self.value)

    # These do not override the "and"/"or" keywords but instead override "&" and "|"
    def __and__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.STR]:
            return Bool_Object(bool(self.value) and bool(other.value))
        elif other.obj_type == ObjectType.BOOL:
            return Bool_Object(bool(self.value) and other.value)

    def __or__(self, other):
        if other.obj_type in [ObjectType.NUM, ObjectType.STR]:
            return Bool_Object(bool(self.value) and bool(other.value))
        elif other.obj_type == ObjectType.BOOL:
            return Bool_Object(bool(self.value) and other.value)


class Array_Object(Internal_Object):
    """
    Array internal object used to store a variable amount of elements.
    """

    def __init__(self, elements):
        self.elements = elements
        self.size = len(elements)
        self.obj_type = ObjectType.ARRAY

    def __repr__(self):
        return "ARRAY_OBJ elements: {}, size: {}".format(self.elements, self.size)

    def __str__(self):
        return "ARRAY_OBJ elements: {}, size: {}".format(self.elements, self.size)

    def __eq__(self, other):
        if other is None:
            return False
        else:
            if self.obj_type == other.obj_type:
                # Check if size of both arrays are equal
                if self.size == other.size:
                    # Deep comparison of each element inside
                    for idx in range(0, self.size):
                        if self.elements[idx] != other.elements[idx]:
                            return False
                    return True
                else:
                    return False
            else:
                return False

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __neg__(self):
        pass

    def __invert__(self):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass


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
        if other is None:
            return False
        else:
            return self.obj_type == other.obj_type and self.value == other.value


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


class Module_Object(Internal_Object):
    def __init__(self, filename, module_contents):
        "Internal object representing an imported module."
        self.name = filename
        self.namespace = module_contents
        self.obj_type = ObjectType.MODULE

    def __str__(self):
        return "MODULE_OBJ: Name: {}, contents: {}".format(
            self.class_name, self.namespace.scope
        )


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
