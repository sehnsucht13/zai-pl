# Copyright 2021 by Yavor Konstantinov <ykonstantinov1@gmail.com>

# This file is part of zai-pl.

# zai-pl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# zai-pl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with zai-pl. If not, see <https://www.gnu.org/licenses/>.

"""
Module contains several classes used to represent internal objects within the
interpreter.
"""
from enum import Enum, auto
from zai.env import Scope
from zai.internal_error import InternalTypeError
from abc import ABC, abstractmethod


class ObjectType(Enum):
    """
    Enum used to represent the different types of internal objects.
    """

    INT = auto()
    FLOAT = auto()
    STR = auto()
    ID = auto()
    BOOL = auto()
    FUNC = auto()
    NATIVE_FUNC = auto()
    CLASS_DEF = auto()
    CLASS_INSTANCE = auto()
    CLASS_METHOD = auto()
    RETURN = auto()
    NIL = auto()
    BREAK = auto()
    CONTINUE = auto()
    ARRAY = auto()
    MODULE = auto()

    def __str__(self):
        type_to_str = {
            "INT": "integer",
            "FLOAT": "float",
            "STR": "string",
            "ID": "variable name",
            "BOOL": "boolean",
            "FUNC": "function",
            "NATIVE_FUNC": "native function",
            "CLASS_DEF": "class definition",
            "CLASS_INSTANCE": "class instance",
            "CLASS_METHOD": "class method",
            "NIL": "nil",
            "ARRAY": "array",
            "MODULE": "module namespace",
        }
        return type_to_str[self.name]


class InternalObject(ABC):
    """
    Base class for all internal objects used in the interpreter.
    """

    @abstractmethod
    def __str__(self):
        pass


# All atomic objects
class NilObject(InternalObject):
    """
    Internal object used to represent nil/null values.
    """

    def __init__(self):
        self.obj_type = ObjectType.NIL

    def __str__(self):
        return "nil"

    def __repr__(self):
        return "NIL_OBJ"

    def __eq__(self, other):
        assert other is not None, "Other is none in __eq__ function for nil object."
        return BoolObject(self.obj_type == other.obj_type)

    def __ne__(self, other):
        return ~(self.__eq__(other))

    def __lt__(self, other):
        raise InternalTypeError("<", self.obj_type, other.obj_type)

    def __le__(self, other):
        raise InternalTypeError("<=", self.obj_type, other.obj_type)

    def __gt__(self, other):
        raise InternalTypeError(">", self.obj_type, other.obj_type)

    def __ge__(self, other):
        raise InternalTypeError(">=", self.obj_type, other.obj_type)

    def __add__(self, other):
        raise InternalTypeError("+", self.obj_type, other.obj_type)

    def __sub__(self, other):
        raise InternalTypeError("-", self.obj_type, other.obj_type)

    def __mul__(self, other):
        raise InternalTypeError("*", self.obj_type, other.obj_type)

    def __truediv__(self, other):
        raise InternalTypeError("/", self.obj_type, other.obj_type)

    def __bool__(self):
        return False

    def __and__(self, other):
        return BoolObject(bool(self) and bool(other))

    def __or__(self, other):
        return BoolObject(bool(self) or bool(other))

    def __neg__(self):
        raise InternalTypeError("-", self.obj_type)

    def __invert__(self):
        return BoolObject(True)


class BoolObject(InternalObject):
    """
    Internal object used to represent a return value from a function.
    """

    def __init__(self, bool_val):
        self.value = bool_val
        self.obj_type = ObjectType.BOOL

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "BOOL_OBJ {}".format(self.value)

    def __eq__(self, other):
        assert other is not None, "Other value in bool internal object __eq__ is none"
        return BoolObject(self.obj_type == other.obj_type and self.value == other.value)

    def __ne__(self, other):
        # Using the invert operator(~) will return a new boolean object.
        return ~(self.__eq__(other))

    def __neg__(self):
        return BoolObject(-self.value)

    def __invert__(self):
        return BoolObject(not self.value)

    def __lt__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return BoolObject(self.value < other.value)
        else:
            raise InternalTypeError("<", self.obj_type, other.obj_type)

    def __le__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return BoolObject(self.value <= other.value)
        else:
            raise InternalTypeError("<=", self.obj_type, other.obj_type)

    def __gt__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return BoolObject(self.value > other.value)
        else:
            raise InternalTypeError(">", self.obj_type, other.obj_type)

    def __ge__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return BoolObject(self.value >= other.value)
        else:
            raise InternalTypeError(">=", self.obj_type, other.obj_type)

    def __add__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return IntObject(self.value + other.value)
        else:
            raise InternalTypeError("+", self.obj_type, other.obj_type)

    def __sub__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return IntObject(self.value - other.value)
        else:
            raise InternalTypeError("-", self.obj_type, other.obj_type)

    def __mul__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return IntObject(self.value * other.value)
        else:
            raise InternalTypeError("*", self.obj_type, other.obj_type)

    def __truediv__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return IntObject(self.value / other.value)
        else:
            raise InternalTypeError("/", self.obj_type, other.obj_type)

    def __and__(self, other):
        return BoolObject(bool(self) and bool(other))

    def __or__(self, other):
        return BoolObject(bool(self) or bool(other))

    def __bool__(self):
        return self.value


class StringObject(InternalObject):
    """
    Internal object used to represent strings within the interpreter.
    """

    def __init__(self, string_val):
        self.value = string_val
        self.str_len = len(string_val)
        self.obj_type = ObjectType.STR

    def __repr__(self):
        return "STR_OBJ {}".format(self.value)

    def __str__(self):
        return self.value

    def __eq__(self, other):
        assert other is not None, "Other variable is none in __eq__ function for string object."
        return BoolObject(self.obj_type == other.obj_type and self.value == other.value)

    def __ne__(self, other):
        return ~self.__eq__(other)

    def __lt__(self, other):
        if other.obj_type == ObjectType.STR:
            return BoolObject(self.value < other.value)
        else:
            raise InternalTypeError("<", self.obj_type, other.obj_type)

    def __le__(self, other):
        if other.obj_type == ObjectType.STR:
            return BoolObject(self.value <= other.value)
        else:
            raise InternalTypeError("<=", self.obj_type, other.obj_type)

    def __gt__(self, other):
        pass
        if other.obj_type == ObjectType.STR:
            return BoolObject(self.value > other.value)
        else:
            raise InternalTypeError(">", self.obj_type, other.obj_type)

    def __ge__(self, other):
        if other.obj_type == ObjectType.STR:
            return BoolObject(self.value >= other.value)
        else:
            raise InternalTypeError(">=", self.obj_type, other.obj_type)

    def __add__(self, other):
        if other.obj_type == ObjectType.STR:
            return StringObject(self.value + other.value)
        else:
            raise InternalTypeError("+", self.obj_type, other.obj_type)

    def __sub__(self, other):
        raise InternalTypeError("-", self.obj_type, other.obj_type)

    def __mul__(self, other):
        if other.obj_type == ObjectType.INT:
            return StringObject(self.value * other.value)
        else:
            raise InternalTypeError("*", self.obj_type, other.obj_type)

    def __truediv__(self, other):
        raise InternalTypeError("/", self.obj_type, other.obj_type)

    def __and__(self, other):
        return BoolObject(bool(self) and bool(other))

    def __or__(self, other):
        return BoolObject(bool(self) or bool(other))

    def __neg__(self):
        raise InternalTypeError("-", self.obj_type)

    def __invert__(self):
        return BoolObject(not bool(self))

    def __bool__(self):
        if self.str_len == 0:
            return False
        return True


class FloatObject(InternalObject):
    """
    Numeric internal object used to store floats.
    """

    def __init__(self, value):
        self.value = value
        self.obj_type = ObjectType.FLOAT

    def __repr__(self):
        return "FLOAT_OBJ {}".format(self.value)

    def __str__(self):
        return "{}".format(self.value)

    def __add__(self, other):
        if other.obj_type in [ObjectType.FLOAT, ObjectType.INT]:
            return FloatObject(self.value + other.value)

        raise InternalTypeError("+", self.obj_type, other.obj_type)

    def __sub__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.FLOAT]:
            return FloatObject(self.value - other.value)

        raise InternalTypeError("-", self.obj_type, other.obj_type)

    def __mul__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.FLOAT]:
            return FloatObject(self.value * other.value)
        else:
            raise InternalTypeError("*", self.obj_type, other.obj_type)

    def __truediv__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.FLOAT]:
            return FloatObject(self.value / other.value)

        raise InternalTypeError("/", self.obj_type, other.obj_type)

    def __lt__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.FLOAT]:
            return BoolObject(self.value < other.value)

        raise InternalTypeError("<", self.obj_type, other.obj_type)

    def __le__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.FLOAT]:
            return BoolObject(self.value <= other.value)
        raise InternalTypeError("<=", self.obj_type, other.obj_type)

    def __gt__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.FLOAT]:
            return BoolObject(self.value > other.value)

        raise InternalTypeError(">", self.obj_type, other.obj_type)

    def __ge__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.FLOAT]:
            return BoolObject(self.value >= other.value)
        raise InternalTypeError(">=", self.obj_type, other.obj_type)

    def __neg__(self):
        return IntObject(-self.value)

    def __invert__(self):
        return BoolObject(not self.value)

    # These do not override the "and"/"or" keywords but instead override "&" and "|"
    def __and__(self, other):
        return BoolObject(bool(self) and bool(other))

    def __or__(self, other):
        return BoolObject(bool(self) or bool(other))

    def __bool__(self):
        return bool(self.value)


class IntObject(InternalObject):
    """
    Numeric internal object used to store integers.
    """

    def __init__(self, value):
        self.value = value
        self.obj_type = ObjectType.INT

    def __repr__(self):
        return "INT_OBJ {}".format(self.value)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        assert other is not None, "Other variable is None in __eq__ method for numeric objects."
        return BoolObject(self.obj_type == other.obj_type and self.value == other.value)

    def __ne__(self, other):
        return ~(self.__eq__(other))

    def __add__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return IntObject(self.value + other.value)

        raise InternalTypeError("+", self.obj_type, other.obj_type)

    def __sub__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return IntObject(self.value - other.value)

        raise InternalTypeError("-", self.obj_type, other.obj_type)

    def __mul__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return IntObject(self.value * other.value)
        elif other.obj_type in ObjectType.STR:
            return StringObject(other.value * self.value)
        else:
            raise InternalTypeError("*", self.obj_type, other.obj_type)

    def __truediv__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return IntObject(self.value / other.value)

        raise InternalTypeError("/", self.obj_type, other.obj_type)

    def __lt__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return BoolObject(self.value < other.value)

        raise InternalTypeError("<", self.obj_type, other.obj_type)

    def __le__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return BoolObject(self.value <= other.value)
        raise InternalTypeError("<=", self.obj_type, other.obj_type)

    def __gt__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return BoolObject(self.value > other.value)

        raise InternalTypeError(">", self.obj_type, other.obj_type)

    def __ge__(self, other):
        if other.obj_type in [ObjectType.INT, ObjectType.BOOL]:
            return BoolObject(self.value >= other.value)
        raise InternalTypeError(">=", self.obj_type, other.obj_type)

    def __neg__(self):
        return IntObject(-self.value)

    def __invert__(self):
        return BoolObject(not self.value)

    # These do not override the "and"/"or" keywords but instead override "&" and "|"
    def __and__(self, other):
        return BoolObject(bool(self) and bool(other))

    def __or__(self, other):
        return BoolObject(bool(self) or bool(other))

    def __bool__(self):
        return bool(self.value)


class ArrayObject(InternalObject):
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
        arr_str = "["
        for idx in range(0, self.size - 1):
            arr_str += str(self.elements[idx]) + ", "
        arr_str += str(self.elements[self.size - 1])
        arr_str += "]"
        return arr_str

    def __eq__(self, other):
        assert other is not None, "Other variable in __eq__ function is None."
        if self.obj_type == other.obj_type:
            # Check if size of both arrays are equal
            if self.size == other.size:
                # Deep comparison of each element inside
                for idx in range(0, self.size):
                    if self.elements[idx] != other.elements[idx]:
                        return BoolObject(False)
                return BoolObject(True)
            else:
                return BoolObject(False)
        else:
            return BoolObject(False)

    def __lt__(self, other):
        raise InternalTypeError("<", self.obj_type, other.obj_type)

    def __le__(self, other):
        raise InternalTypeError("<=", self.obj_type, other.obj_type)

    def __ne__(self, other):
        return not (self.__eq__(other))

    def __gt__(self, other):
        raise InternalTypeError(">", self.obj_type, other.obj_type)

    def __ge__(self, other):
        raise InternalTypeError(">=", self.obj_type, other.obj_type)

    def __add__(self, other):
        if other.obj_type == ObjectType.ARRAY:
            self.elements.extend(other.elements)
        else:
            self.elements.append(other)

    def __sub__(self, other):
        raise InternalTypeError("-", self.obj_type, other.obj_type)

    def __mul__(self, other):
        raise InternalTypeError("*", self.obj_type, other.obj_type)

    def __truediv__(self, other):
        raise InternalTypeError("/", self.obj_type, other.obj_type)

    def __and__(self, other):
        return BoolObject(bool(self) and bool(other))

    def __or__(self, other):
        return BoolObject(bool(self) or bool(other))

    def __neg__(self):
        raise InternalTypeError(
            "-",
            self.obj_type,
        )

    def __invert__(self):
        return BoolObject(not self.__bool__())

    def __bool__(self):
        if self.size == 0:
            return False
        return True


class ReturnObject(InternalObject):
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
        assert other is not None, "Other variable in __eq__ method for a return object is None."
        return BoolObject(self.obj_type == other.obj_type and self.value == other.value)


class BreakObject(InternalObject):
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


class ContinueObject(InternalObject):
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


class FuncObject(InternalObject):
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
        return "<function object {}>".format(self.name)
        # return "FUNC_OBJ: Name: {}, Args: {}, Arity: {}".format(
        #     self.name, self.args, self.arity,
        # )


class NativeFuncObject(InternalObject):
    """
    Internal object used to represent a function.
    """

    def __init__(self, func):
        self.obj_type = ObjectType.NATIVE_FUNC
        self.name = func.__name__
        self.arity = func.__code__.co_argcount
        self.body = func

    def __str__(self):
        return "<native function object {}>".format(self.name)


class ClassDefObject(InternalObject):
    def __init__(self, class_name, class_methods):
        """setup class object"""
        self.obj_type = ObjectType.CLASS_DEF
        self.class_name = class_name
        self.class_methods = class_methods

    def __str__(self):
        return "<class definition object {}>".format(self.class_name)


class ModuleObject(InternalObject):
    def __init__(self, module_name, module_path, module_contents, import_as=None):
        """Internal object representing an imported module."""
        self.name = module_name
        self.import_as = import_as
        self.path = module_path
        self.namespace = module_contents
        self.obj_type = ObjectType.MODULE

    def __str__(self):
        if self.import_as != self.name:
            return "<module {} imported as {}>".format(self.name, self.import_as)
        else:
            return "<module {}>".format(self.name)


class ClassMethodObject(InternalObject):
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
        return "<class method object {}>".format(self.name)


class ClassInstanceObject(InternalObject):
    def __init__(self, class_name, class_methods):
        """Object representing a class instance."""
        self.obj_type = ObjectType.CLASS_INSTANCE
        self.class_name = class_name
        self.namespace = Scope(None)

        # Register all class methods in the internal environment
        for method in class_methods:
            self.namespace.initialize_variable(
                method.name,
                ClassMethodObject(method.name, method.args, method.body, self.namespace),
            )

    def __str__(self):
        return "<class instance object {}>".format(self.class_name)

    def get_field(self, field_name):
        return self.namespace.get_variable(field_name)
