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

import zai.objects


def object_type(internal_object):
    """
    Return the type of an internal object as a string. If the type is
    unknown, return 'nil'.
    """
    if internal_object.obj_type == zai.objects.ObjectType.ARRAY:
        return zai.objects.StringObject("array")
    elif internal_object.obj_type == zai.objects.ObjectType.NUM:
        return zai.objects.StringObject("number")
    elif internal_object.obj_type == zai.objects.ObjectType.STR:
        return zai.objects.StringObject("string")
    elif internal_object.obj_type == zai.objects.ObjectType.NIL:
        return zai.objects.StringObject("nil")
    elif internal_object.obj_type == zai.objects.ObjectType.MODULE:
        return zai.objects.StringObject("module")
    elif internal_object.obj_type == zai.objects.ObjectType.BOOL:
        return zai.objects.StringObject("boolean")
    elif internal_object.obj_type == zai.objects.ObjectType.FUNC:
        return zai.objects.StringObject("function")
    elif internal_object.obj_type == zai.objects.ObjectType.CLASS_DEF:
        return zai.objects.StringObject("class_def")
    elif internal_object.obj_type == zai.objects.ObjectType.CLASS_INSTANCE:
        return zai.objects.StringObject("class_instance")
    elif internal_object.obj_type == zai.objects.ObjectType.CLASS_METHOD:
        return zai.objects.StringObject("class_method")
    else:
        return zai.objects.NilObject()


def str_len(internal_object):
    """
    Determine the length of a string. If the object passed to this function is
    not a string object, return nil.
    """
    if internal_object.obj_type == zai.objects.ObjectType.STR:
        return zai.objects.NumObject(internal_object.str_len)
    else:
        return zai.objects.NilObject()


def mod(operand1, operand2):
    """
    Find the modulus of operand1 and operand2. Return nil if arguments
    are not numbers.
    """
    if operand1.obj_type == zai.objects.ObjectType.NUM and operand2.obj_type == zai.objects.ObjectType.NUM:
        if operand1.value == 0 or operand2.value == 0:
            return zai.objects.NilObject()
        else:
            return zai.objects.NumObject(operand1.value % operand2.value)
    else:
        return zai.objects.NilObject()


def power(base, exponent):
    """
    Return the argument base raised to the power represented by exponent.
    """
    if base.obj_type == zai.objects.ObjectType.NUM and exponent.obj_type == zai.objects.ObjectType.NUM:
        return zai.objects.NumObject(pow(base.value, exponent.value))
    else:
        return zai.objects.NilObject()


def register_functions():
    """
    Transform all native function defined within this module into internal objects
    which can be called by the interpreter.
    """
    registered_functions = list()
    registered_functions.append(zai.objects.NativeFuncObject(str_len))
    registered_functions.append(zai.objects.NativeFuncObject(object_type))
    registered_functions.append(zai.objects.NativeFuncObject(power))
    registered_functions.append(zai.objects.NativeFuncObject(mod))

    return registered_functions
