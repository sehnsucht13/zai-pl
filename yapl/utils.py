import os
from yapl.objects import ObjectType


def get_module_path():
    """
    Retrieve the interpreter's module path from the environment.
    """
    module_paths = list()
    # retrieve the current working directory and the interpreter path specified
    # in the environment
    curr_path = os.getcwd()
    environ_path = os.environ.get("YAPL_PATH").split(":")

    # Remove any strings containing only whitespace and combine with current working
    # directory path.
    environ_path = list(filter(None, environ_path))
    environ_path.append(curr_path)
    return environ_path


def read_module_contents(module_name):
    """
    Find and return a string containing the contents of a module.
    """
    from os import listdir

    module_path = get_module_path()
    for path in module_path:
        if module_name in listdir(path):
            filepath = os.path.join(path, module_name)
            return open(filepath, "r").read()
    return None


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
    elif internal_obj.obj_type == ObjectType.NIL:
        print("nil")
    elif internal_obj.obj_type == ObjectType.ARRAY:
        output_str = "["
        for elem in internal_obj.elements:
            output_str += elem.__str__() + " "
        output_str += "]"
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
    return obj.obj_type in [
        ObjectType.BOOL,
        ObjectType.NUM,
        ObjectType.STR,
        ObjectType.NIL,
    ]
