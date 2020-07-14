from yapl.objects import pprint_type


class InternalErr(Exception):
    def __init__(self,):
        raise NotImplementedError()


class InternalTypeError(InternalErr):
    def __init__(self, operation, left_type, right_type=None):
        """Class representing an internal error encountered during and basic operations
        between one or more types.
        """
        self.operation = operation
        self.left = left_type
        self.right = right_type
        self.err_msg = str()

        if self.right != None:
            self.err_msg = "The operation {} is not allowed on a {}!".format(
                self.operation, pprint_type(self.left)
            )
        else:
            self.err_msg = "The operation {} is not allowed between a {} and a {}!".format(
                self.operation, pprint_type(self.left), pprint_type(self.right)
            )

    def __str__(self):
        return "Typecheck Error: {}".format(self.err_msg)

    def __repr__(self):
        "Internal Runtime Error: Operation {}, Left Side: {}, Right Side: {}".format(
            self.operation, self.left, self.right
        )


class InternalRuntimeErr(InternalErr):
    def __init__(self, message):
        "Class representing internal errors encountered during runtime."
        self.message = message

    def __str__(self):
        return "Runtime Error: {}".format(self.message)

    def __repr__(self):
        "Internal Runtime Error: {}".format(self.message)


class InternalParseErr(InternalErr):
    def __init__(self, message):
        "Class representing internal errors encountered during parsing/lexing stage."
        self.message = message

    def __str__(self):
        return "Parse Error: {}".format(self.message)

    def __repr__(self):
        "Internal Parse Error: {}".format(self.message)
