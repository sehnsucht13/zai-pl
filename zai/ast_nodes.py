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

""" Module defining nodes used in the abstract syntax tree created by the parser. """
from abc import ABC, abstractmethod


class ASTNode(ABC):
    """
    Base class from which all AST nodes are derived.
    """

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def accept(self, visitor):
        pass


class ProgramNode(ASTNode):
    def __init__(self):
        self.stmnts = list()

    def add_stmnt(self, stmnt):
        self.stmnts.append(stmnt)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_program(self)

    def __str__(self):
        for stmnt in self.stmnts:
            print(stmnt)
        return "Program_node"


class PrintNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_print(self)

    def __str__(self):
        return "{}".format(self.expr)


class PropertyAccessNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "(DOT_NODE L:{} R:{})".format(self.left, self.right)

    def accept(self, visitor):
        return visitor.visit_dot_node(self)


class ReassignBinNode(ASTNode):
    def __init__(self, symbol_path, symbol_name, value):
        self.path = symbol_path  # Path leading to the symbol
        self.name = symbol_name  # The actual symbol name within the environment
        self.value = value

    def __str__(self):
        return "REPLACE_ASSIGN_NODE {} {} {}".format(self.name, self.path, self.value)

    def accept(self, visitor):
        return visitor.visit_replace_assign(self)


class NewAssignBinNode(ASTNode):
    def __init__(self, symbol_path, symbol_name, value):
        self.path = symbol_path
        self.name = symbol_name
        self.value = value

    def __str__(self):
        return "NEW_ASSIGN_NODE {} {} {}".format(self.name, self.path, self.value)

    def accept(self, visitor):
        return visitor.visit_new_assign(self)


class BinOpNode(ASTNode):
    """Base class for all binary nodes with an associated operation."""

    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op


class EqBinNode(BinOpNode):
    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_eq(self)

    def __str__(self):
        return "EQ_NODE: {} {} {}".format(self.left, self.op, self.right)


class ArithBinNode(BinOpNode):
    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_arith(self)

    def __str__(self):
        return "(ARITH_NODE: {} {} {})".format(self.left, self.op, self.right)


class LogicBinNode(BinOpNode):
    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_logic(self)

    def __str__(self):
        return "LOGIC_NODE: {} {} {}".format(self.left, self.op, self.right)


class RelopBinNode(BinOpNode):
    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_relop(self)

    def __str__(self):
        return "RELOP_NODE: {} {} {}".format(self.left, self.op, self.right)


class UnaryNode(ASTNode):
    def __init__(self, op, right):
        self.value = right
        self.op = op

    def __str__(self):
        return "UNARY_NODE: {} {}".format(self.op, self.value)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_unary(self)


class BracketNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "BRACKET_NODE: {}".format(self.expr)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_bracket(self)


class IfNode(ASTNode):
    def __init__(self, conditions, else_block):
        self.condition_blocks = conditions
        self.else_block = else_block

    def __str__(self):
        return "IF_NODE: conditions: {} else:{}".format(self.condition_blocks, self.else_block)

    def accept(self, visitor):
        return visitor.visit_if(self)


class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return "WHILE_NODE: condition: {} body:{}".format(self.condition, self.body)

    def accept(self, visitor):
        return visitor.visit_while(self)


class SwitchNode(ASTNode):
    def __init__(self, switch_cond, switch_cases, default_case):
        self.switch_cond = switch_cond
        self.switch_cases = switch_cases
        self.default_case = default_case

    def __str__(self):
        return "SWITCH_NODE: condition: {} cases:{} default:{}".format(
            self.switch_cond, self.switch_cases, self.default_case
        )

    def accept(self, visitor):
        return visitor.visit_switch(self)


class PrimitiveValueNode(ASTNode):
    """Base class for all primitive values."""

    def __init__(self, val=None):
        self.val = val


class SymbolNode(PrimitiveValueNode):
    def __str__(self):
        return "ID_NODE: {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_symbol(self)


class BoolNode(PrimitiveValueNode):
    def __str__(self):
        return "BOOL_NODE: {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_bool(self)


class StringNode(PrimitiveValueNode):
    def __str__(self):
        return "STR_NODE: {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_string(self)


class FloatNode(PrimitiveValueNode):
    def __str__(self):
        return "FLOAT_NODE {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_float(self)


class IntNode(PrimitiveValueNode):
    def __str__(self):
        return "INT_NODE: {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_int(self)


class NilNode(PrimitiveValueNode):
    def __str__(self):
        return "NIL_NODE"

    def accept(self, visitor):
        return visitor.visit_nil(self)


class FuncNode(ASTNode):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def __str__(self):
        return "FUNC_NODE {}".format(self.name)

    def accept(self, visitor):
        return visitor.visit_func_def(self)


class BlockNode(ASTNode):
    def __init__(self, block_stmnts):
        self.stmnts = block_stmnts

    def __str__(self):
        output = str()
        for stmtn in self.stmnts:
            output += "\n" + stmtn.__str__()
        return "BLOCK_NODE \n{}".format(output)

    def accept(self, visitor):
        return visitor.visit_scope_block(self)


class CallNode(ASTNode):
    def __init__(self, object_name, call_args):
        self.object_name = object_name
        self.call_args = call_args

    def __str__(self):
        return "CALL_NODE: {} {}".format(self.object_name, self.call_args)

    def accept(self, visitor):
        return visitor.visit_call(self)


class ClassMethodNode(ASTNode):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def __str__(self):
        return "CLASS_METHOD_NODE {}".format(self.name)

    def accept(self, visitor):
        return visitor.visit_class_method(self)


class ClassDefNode(ASTNode):
    def __init__(self, class_name, class_methods):
        self.class_name = class_name
        self.class_methods = class_methods

    def __str__(self):
        return "CLASS_NODE {} {}".format(self.class_name, self.class_methods)

    def accept(self, visitor):
        return visitor.visit_class_def(self)


class ThisNode(ASTNode):
    def __init__(self):
        pass

    def __str__(self):
        return "THIS_NODE"

    def accept(self, visitor):
        return visitor.visit_this(self)


class BreakNode(ASTNode):
    def __init__(self):
        pass

    def __str__(self):
        return "BREAK_NODE"

    def accept(self, visitor):
        return visitor.visit_break(self)


class ContinueNode(ASTNode):
    def __init__(self):
        pass

    def __str__(self):
        return "CONTINUE_NODE"

    def accept(self, visitor):
        return visitor.visit_continue(self)


class ReturnNode(ASTNode):
    def __init__(self, return_expr):
        self.expr = return_expr

    def __str__(self):
        return "RETURN_NODE {}".format(self.expr)

    def accept(self, visitor):
        return visitor.visit_return(self)


class DoWhileNode(ASTNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def __str__(self):
        return "DO_WHILE_NODE {}, {}".format(self.cond, self.body)

    def accept(self, visitor):
        return visitor.visit_do_while(self)


class ArrayNode(ASTNode):
    def __init__(self, elements):
        # elements is a list of "or_expr"
        self.elements = elements

    def __str__(self):
        return "ARRAY_NODE elements: {}".format(self.elements)

    def accept(self, visitor):
        return visitor.visit_array(self)


class ArrayAccessNode(ASTNode):
    def __init__(self, array_id, array_position):
        self.array_name = array_id
        self.array_pos = array_position

    def __str__(self):
        return "ARRAY_ACCESS_NODE name: {}, position: {}".format(self.array_name, self.array_pos)

    def accept(self, visitor):
        return visitor.visit_array_access(self)


class IncrNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "INCR_NODE {}".format(self.value)

    def accept(self, visitor):
        return visitor.visit_incr(self)


class DecrNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "DECR_NODE {}".format(self.value)

    def accept(self, visitor):
        return visitor.visit_decr(self)


class ImportNode(ASTNode):
    def __init__(self, module_name, import_name=None):
        self.module_name = module_name
        self.import_name = import_name

    def __str__(self):
        return "IMPORT_NODE {} with import name: {}".format(self.module_name, self.import_name)

    def accept(self, visitor):
        return visitor.visit_import(self)


class AddassignNode(ASTNode):
    def __init__(self, symbol_path, symbol_name, increment):
        self.symbol_path = symbol_path
        self.symbol_name = symbol_name
        self.increment = increment

    def __str__(self):
        return "ADD_ASSIGN_NODE {} {} {}".format(self.symbol_name, self.symbol_path, self.increment)

    def accept(self, visitor):
        return visitor.visit_add_assign(self)


class SubassignNode(ASTNode):
    def __init__(self, symbol_path, symbol_name, decrement):
        self.symbol_path = symbol_path
        self.symbol_name = symbol_name
        self.decrement = decrement

    def __str__(self):
        return "SUB_ASSIGN_NODE {} {} {}".format(self.symbol_name, self.symbol_path, self.decrement)

    def accept(self, visitor):
        return visitor.visit_sub_assign(self)
