class InternalErr(Exception):
    def __init__(self,):
        raise NotImplementedError()


class InternalRuntimeErr(InternalErr):
    def __init__(self, message):
        "Class representing internal errors encountered during runtime."
        self.message = message

    def __str__(self):
        return "Runtime Error: {}".format(self.message)

    def __repr__(self):
        "Internal Runtime Error: {}".format(self.message)
