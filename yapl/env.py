class Scope:
    def __init__(self, parent):
        self.scope = dict()
        self.parent = parent

    def add_symbol(self, symbol, value):
        assert symbol != None
        assert value != None
        self.scope[symbol] = value

    def lookup_symbol(self, symbol):
        value = self.scope.get(symbol, None)
        if value == None and self.parent != None:
            return self.parent.lookup_symbol(symbol)
        return value


class Environment:
    def __init__(self):
        self.scopes = list()
        # Add the global scope
        self.scopes.append(Scope(None))
        self.stack_height = 0

    def peek(self):
        if self.stack_height > -1:
            return self.scopes[self.stack_height]

    def exit_scope(self):
        if self.stack_height > -1:
            self.scopes.pop()
            self.stack_height -= 1

    def enter_scope(self, parent_scope=None):
        self.scopes.append(Scope(parent_scope))
        self.stack_height += 1
