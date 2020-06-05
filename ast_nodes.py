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
        self.right = right
        self.op = op

class Bracket_Node(AST_Node):
    def __init__(self, expr):
        self.type = node_type
        self.exrp = expr

class ID_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

class Bool_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

class String_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

class Num_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val
