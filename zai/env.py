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
Module containing classes related to managing the interpreter environment
and nested scopes.
"""


class Scope:
    def __init__(self, parent):
        self.scope = dict()
        self.parent = parent

    def new_variable(self, var_name, value):
        """
        Instantiate a new variable within the current scope of the environment.
        Return True to indicate success.
        """
        assert (
            var_name is not None
        ), "Variable name of new environment variable is None."
        assert value is not None, "Variable value of new environment variable is None."
        self.scope[var_name] = value
        return True

    def replace_variable(self, var_name, value):
        """
        Replace the value of an existing variable within the environment.
        Return True or False if the value exists/does not exist within
        the current environment.
        """
        assert var_name is not None, "Variable name to be replaced is None."
        assert value is not None, "Variable value to be replaced is None"
        if var_name in self.scope.keys():
            self.scope[var_name] = value
            return True
        elif self.parent is None:
            return False
        else:
            return self.parent.replace_variable(var_name, value)

    def lookup_symbol(self, symbol):
        """
        Lookupt the value of a symbol in the current scope and all parent scopes
        and return it. If the symbol does not exist, return None.
        """
        value = self.scope.get(symbol, None)
        if value is None and self.parent is not None:
            return self.parent.lookup_symbol(symbol)
        return value

    def merge_scopes(self, new_scope):
        """
        Merge two scope objects into one.
        """
        for k, v in new_scope.scope.items():
            self.scope[k] = v

    def __str__(self):
        return str(self.scope)


class Environment:
    """
    Class responsible for managing a stack of environment scopes.
    """

    def __init__(self):
        self.scopes = list()
        # Add the global scope
        self.scopes.append(Scope(None))
        self.stack_height = 0

    def peek(self):
        """
        Return the scope on the top of the scope stack.
        """
        if self.stack_height > -1:
            return self.scopes[self.stack_height]

    def exit_scope(self):
        """
        Remove the most current scope from the scope stack.
        """
        if self.stack_height > -1:
            self.scopes.pop()
            self.stack_height -= 1

    def enter_scope(self, parent_scope=None):
        """
        Put a new scope on top of the scope stack.
        """
        self.scopes.append(Scope(parent_scope))
        self.stack_height += 1

    def __str__(self):
        env_stack = str()
        for scope in self.scopes:
            env_stack += str(scope) + "\n"
        return env_stack
