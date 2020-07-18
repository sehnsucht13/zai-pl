import yapl.objects


def object_type(internal_object):
    """
    Return the type of an internal object as a string. If the type is 
    unknown, return 'nil'.
    """
    if internal_object.obj_type == yapl.objects.ObjectType.ARRAY:
        return yapl.objects.String_Object("array")
    elif internal_object.obj_type == yapl.objects.ObjectType.NUM:
        return yapl.objects.String_Object("number")
    elif internal_object.obj_type == yapl.objects.ObjectType.STR:
        return yapl.objects.String_Object("string")
    elif internal_object.obj_type == yapl.objects.ObjectType.NIL:
        return yapl.objects.String_Object("nil")
    elif internal_object.obj_type == yapl.objects.ObjectType.MODULE:
        return yapl.objects.String_Object("module")
    elif internal_object.obj_type == yapl.objects.ObjectType.BOOL:
        return yapl.objects.String_Object("boolean")
    elif internal_object.obj_type == yapl.objects.ObjectType.FUNC:
        return yapl.objects.String_Object("function")
    elif internal_object.obj_type == yapl.objects.ObjectType.CLASS_DEF:
        return yapl.objects.String_Object("class_def")
    elif internal_object.obj_type == yapl.objects.ObjectType.CLASS_INSTANCE:
        return yapl.objects.String_Object("class_instance")
    elif internal_object.obj_type == yapl.objects.ObjectType.CLASS_METHOD:
        return yapl.objects.String_Object("class_method")
    else:
        return yapl.objects.Nil_Object()


def str_len(internal_object):
    """
    Determine the length of a string. If the object passed to this function is
    not a string object, return nil.
    """
    if internal_object.obj_type == yapl.objects.ObjectType.STR:
        return yapl.objects.Num_Object(internal_object.str_len)
    else:
        return yapl.objects.Nil_Object()


def register_functions():
    """
    Transform all native function defined within this module into internal objects
    which can be called by the interpreter.
    """
    registered_functions = list()
    registered_functions.append(yapl.objects.Native_Func_Object(str_len))
    registered_functions.append(yapl.objects.Native_Func_Object(object_type))

    return registered_functions
