"""Module containing utilities functions used by the interpreter."""
import os
from yapl.objects import ObjectType


def get_module_path():
    """
    Retrieve the interpreter's module path from the environment.
    """
    # retrieve the current working directory and the interpreter path specified
    # in the environment
    curr_path = [os.getcwd()]
    environ_path = os.environ.get("YAPL_PATH").split(":")

    # Remove any strings containing only whitespace and combine with current working
    # directory path.
    environ_path = list(filter(None, environ_path))
    return curr_path + environ_path


def read_module_contents(module_name):
    """
    Find and return a string containing the contents of a module.
    """
    from os import listdir

    module_path = get_module_path()
    full_module_path = None
    for path in module_path:
        if module_name in listdir(path):
            full_module_path = os.path.join(path, module_name)
            return (full_module_path, open(full_module_path, "r").read())
    return (None, None)


def is_truthy(internal_object):
    """ Check if an internal object is truthy. Returns True or False."""
    # Truthiness will be the same as the one in python
    if internal_object.obj_type in [
        ObjectType.BOOL,
        ObjectType.STR,
        ObjectType.NUM,
        ObjectType.NIL,
        ObjectType.ARRAY,
    ]:
        return bool(internal_object)
    else:
        # Functions, class instances and class definitions are not truthy.
        return False


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