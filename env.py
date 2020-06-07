class Frame:
    def __init__(self, parent_frame=None):
        # Pointer to the environment of the parent frame
        self.parent_frame = parent_frame
        # List of the scopes in the current frame
        self.scopes = list()
        # Add the base scope of the current frame
        self.scopes.append(dict())
        self.scope_depth = 0

    def enter_scope(self):
        self.scope_depth += 1
        self.scopes.append(dict())

    def exit_scope(self):
        if self.scope_depth > -1:
            self.scopes.pop()
            self.scope_depth -= 1

    def add_symbol(self, symbol, value):
        self.scopes[self.scope_depth][symbol] = value

    def lookup_symbol(self, symbol):
        # Iterate through all scopes starting at the most current one.
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
        # Check for value in current frame
        value = self.lookup_symbol(symbol)
        #
        if value == None and self.parent_frame != None:
            return self.parent_frame.resolve_sym(symbol)
        else:
            return value


class RunTime_Stack:
    def __init__(self):
        """ A runtime stack used to manage stack frames produced during execution of function calls."""
        self.runtime_stack = list()
        # append the first frame which will contain the global environment and eventually will contain builtins
        self.runtime_stack.append(Frame())
        self.stack_height = 0

    def peek(self):
        if self.stack_height > -1:
            return self.runtime_stack[self.stack_height]

    def pop(self):
        if self.stack_height > -1:
            self.runtime_stack.pop()
            self.stack_height -= 1

    def push(self, new_frame):
        self.runtime_stack.append(new_frame)
        self.stack_height += 1
