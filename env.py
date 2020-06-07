
class RunTime_Stack:
    def __init__(self):
        """ A runtime stack used to manage stack frames produced during execution of function calls."""
        pass

    def peek(self):
        pass

    def pop(self):
        pass

    def push(self, new_frame):
        pass


class Frame:
    def __init__(self, parent_env=None):
        # Pointer to the environment of the parent frame
        self.parent_env = parent_env
        # List of the scopes in the current frame
        self.scopes = list()
        # Add the base scope of the current frame
        self.scopes.append(dict())
        self.scope_depth = -1

    def enter_scope(self):
        self.scope_depth += 1
        self.scopes.append(dict())

    def exit_scope(self):
        if self.scope_depth > -1:
            self.scopes.pop()

    def add_symbol(self, symbol, value):
        self.scopes[self.scope_depth][symbol] = value

    def lookup_symbol(self, symbol):
        for depth in range(self.scope_depth, -1, -1):
            curr_scope = self.scopes[depth]
            sym_value = curr_scope.get(symbol, None)
            if sym_value is not None:
                return sym_value

        return None

    # NOTE: To resolve a symbol, we need to look at all the current scopes of this frame first.
        # If the symbol is found here, it is returned. Otherwise, we look up the chain of parent frames.
        # If the symbol is not found in any frames, we return None.
    def resolve_sym(self, symbol):
        return self.lookup_symbol(symbol)
