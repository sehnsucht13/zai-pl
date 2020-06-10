""" Module defining nodes used in the abstract syntax tree created by the parser. """


class AST_Node:
    """  """

    def __init__(self):
        raise NotImplementedError()


class Program_Node(AST_Node):
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
        stmnt_string = str()
        for stmnt in self.stmnts:
            stmnt_string += "\n" + stmnt.__str__()


class Print_Node(AST_Node):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_print(self)

    def __str__(self):
        return "{}".format(self.expr)


class Bin_Node(AST_Node):
    def __init__(self, left, op, right):
        raise NotImplementedError()


class Assign_Bin_Node(AST_Node):
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def __str__(self):
        return "ASSIGN_NODE {} {}".format(self.symbol, self.value)

    def accept(self, visitor):
        return visitor.visit_assign(self)


class Eq_Bin_Node(Bin_Node):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_eq(self)

    def __str__(self):
        return "EQ_NODE: {} {} {}".format(self.left, self.op, self.right)


class Arith_Bin_Node(Bin_Node):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_arith(self)

    def __str__(self):
        return "ARITH_NODE: {} {} {}".format(self.left, self.op, self.right)


class Logic_Bin_Node(Bin_Node):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_logic(self)

    def __str__(self):
        return "LOGIC_NODE: {} {} {}".format(self.left, self.op, self.right)


class Relop_Bin_Node(Bin_Node):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_relop(self)

    def __str__(self):
        return "RELOP_NODE: {} {} {}".format(self.left, self.op, self.right)


class Unary_Node(AST_Node):
    def __init__(self, op, right):
        self.value = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_unary(self)

    def __str__(self):
        return "UNARY_NODE: {} {}".format(self.op, self.right)


class Bracket_Node(AST_Node):
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


class If_Node(AST_Node):
    def __init__(self, condition, true_stmnt, else_stmnt):
        self.condition = condition
        self.true_stmnt = true_stmnt
        self.else_stmnt = else_stmnt

    def __str__(self):
        return "IF_NODE: cond: {} true: {} false:{}".format(
            self.condition, self.true_stmnt, self.else_stmnt
        )

    def accept(self, visitor):
        return visitor.visit_if(self)


class ID_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

    def __str__(self):
        return "{}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_symbol(self)


class Bool_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

    def __str__(self):
        return "BOOL_NODE: {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_bool(self)


class String_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

    def __str__(self):
        return "STR_NODE: {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_string(self)


class Num_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

    def __str__(self):
        return "NUM_NODE: {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_num(self)


class Func_Node(AST_Node):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def __str__(self):
        return "FUNC_NODE {} {} {}".format(self.val)

    def accept(self, visitor):
        return visitor.visit_func_def(self)


class Block_Node(AST_Node):
    def __init__(self, block_stmnts):
        self.stmnts = block_stmnts

    def __str__(self):
        output = str()
        for stmtn in self.stmnts:
            output += "\n" + stmtn.__str__()
        return "BLOCK_NODE \n{}".format(output)

    def accept(self, visitor):
        return visitor.visit_block(self)
