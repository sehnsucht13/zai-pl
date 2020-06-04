class AST_Node:
    def __init__(self):
        raise NotImplementedError()

class Program_Node(AST_Node):
    def __init__(self):
        self.stmnts = list()
    def add_stmnt(self, stmnt):
        self.stmnts.append(stmnt)

class Bin_Node(AST_Node):
    def __init__(self, left, op, right):
        self.type = node_type
        self.left = left
        self.right = right
        self.op = op

class Unary_Node(AST_Node):
    def __init__(self, op, right):
        self.type = node_type
        self.right = right
        self.op = op

class Bracket_Node(AST_Node):
    def __init__(self, expr):
        self.type = node_type
        self.exrp = expr

class Bool_Node(AST_Node):
    def __init__(self, node_type, bool_val):
        self.type = node_type
        self.val = bool_val

class Num_Node(AST_Node):
    def __init__(self, int_val):
        self.val = int_val
