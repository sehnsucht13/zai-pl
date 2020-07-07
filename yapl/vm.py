from yapl.lexer import Lexer
from yapl.env import Environment, Scope
from yapl.objects import *
from yapl.parse import Parser
from yapl.tokens import Tok_Type
from yapl.internal_error import InternalRuntimeErr


class YAPL_VM:
    """
    Class representing a single instance of the YAPL virtual machine. Each command
    is evaluate within the same context.
    """

    def __init__(self):
        self.env = Environment()
        self.repl_mode_flag = False

    def execute(self, ast_root):
        """
        Main entry point for all AST roots.
        """
        return ast_root.accept(self)

    def run_repl(self):
        """
        Start a REPL which evaluates every command provided within one VM context.
        """
        self.repl_mode_flag = True
        while True:
            lexer = Lexer()
            str_input = input(">> ")
            tok_stream = lexer.tokenize_string(str_input)
            parser = Parser(tok_stream)
            root = parser.parse()
            val = self.execute(root)

    def run_string(self, input_str):
        """
        Run a single string within the current VM context.
        """
        lexer = Lexer()
        try:
            tok_stream = lexer.tokenize_string(input_str)
            # print(tok_stream)
            parser = Parser(tok_stream)
            root = parser.parse()
            val = self.execute(root)
        except InternalRuntimeErr as e:
            print(e)

    def visit_program(self, node):
        for stmnt in node.stmnts:
            val = stmnt.accept(self)
            if is_atom(val) and self.repl_mode_flag:
                pprint_internal_object(val)

    def visit_num(self, node):
        return Num_Object(node.val)

    def visit_symbol(self, node):
        # Retrieve symbol from env
        curr_scope = self.env.peek()
        # TODO: Catch case of symbol not existing. Need to return an error
        symbol_val = curr_scope.lookup_symbol(node.val)

        if symbol_val is None:
            err_msg = 'Variable "{}" does not exist.'.format(node.val)
            raise InternalRuntimeErr(err_msg)
        else:
            return symbol_val

    def visit_string(self, node):
        return String_Object(node.val)

    def visit_bracket(self, node):
        return node.expr.accept(self)

    def visit_bool(self, node):
        if node.val == Tok_Type.TRUE:
            return Bool_Object(True)
        else:
            return Bool_Object(False)

    def visit_arith(self, node):
        # Evaluate left and right sides
        left = node.left.accept(self)
        right = node.right.accept(self)

        # Perform actions depeding on type
        if node.op == Tok_Type.PLUS:
            return Num_Object(left.value + right.value)
        elif node.op == Tok_Type.MINUS:
            return Num_Object(left.value - right.value)
        elif node.op == Tok_Type.MUL:
            return Num_Object(left.value * right.value)
        elif node.op == Tok_Type.DIV:
            return Num_Object(left.value / right.value)

    def visit_logic(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        # Stores the result of the operation
        result = None

        # >
        if node.op == Tok_Type.AND:
            relop_result = left.value and right.value
        # >=
        elif node.op == Tok_Type.OR:
            relop_result = left.value or right.value

        return Bool_Object(relop_result)

    def visit_relop(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        # Stores the result of the operation
        relop_result = None

        # >
        if node.op == Tok_Type.GT:
            relop_result = left.value > right.value
        # >=
        elif node.op == Tok_Type.GTE:
            relop_result = left.value >= right.value
        # <
        elif node.op == Tok_Type.LT:
            relop_result = left.value < right.value
        # <=
        elif node.op == Tok_Type.LTE:
            relop_result = left.value <= right.value

        return Bool_Object(relop_result)

    def visit_eq(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        # Store the result of the comparison
        eq_result = None
        if node.op == Tok_Type.EQ:
            eq_result = left.value == right.value
        elif node.op == Tok_Type.NEQ:
            eq_result = left.value != right.value

        return Bool_Object(eq_result)

    def visit_unary(self, node):
        result = node.value.accept(self)
        if node.op == Tok_Type.MINUS:
            return Num_Object(-(result.value))
        elif node.op == Tok_Type.BANG:
            return Bool_Object(not (result.value))

    def visit_if(self, node):
        # Evaluate each condition and execute block if it is true
        for cond in node.conditions:
            cond_value = cond[0].accept(self)
            if is_truthy(cond_value):
                return cond[1].accept(self)

        return node.else_block.accept(self)

    def visit_while(self, node):
        cond_value = node.condition.accept(self)
        while is_truthy(cond_value):
            node.body.accept(self)
            cond_value = node.condition.accept(self)

    def visit_print(self, node):
        print_value = node.expr.accept(self)
        pprint_internal_object(print_value)

    def visit_replace_assign(self, node):
        symbol = node.symbol
        # Evaluate the right hand side
        value = node.value.accept(self)
        assert symbol is not None
        assert value is not None

        scope = self.env.peek()

        status = scope.add_symbol(symbol, value, False)
        if status is False:
            err_msg = 'Variable "{}" cannot be reasigned because it does not exist.'.format(
                symbol
            )
            raise InternalRuntimeErr(err_msg)

    def visit_new_assign(self, node):
        symbol = node.symbol
        # Evaluate the right hand side
        value = node.value.accept(self)

        assert symbol is not None
        assert value is not None

        scope = self.env.peek()
        scope.add_symbol(symbol, value, True)

    def visit_block(self, node):
        # Create a new scope to evaluate the current block in
        parent_env = self.env.peek()
        self.env.enter_scope(parent_env)
        for stmnt in node.stmnts:
            stmnt.accept(self)
        self.env.exit_scope()

    def visit_func_def(self, node):
        scope = self.env.peek()
        # Register the function in the current frame
        scope.add_symbol(
            node.name, Func_Object(node.name, node.args, node.body, scope), True
        )

    def visit_class_def(self, node):
        """
        Keyword Arguments:
        node -- Class definition node
        """
        scope = self.env.peek()
        # Register the class in the scope
        scope.add_symbol(
            node.class_name, Class_Def_Object(node.class_name, node.class_methods), True
        )

    def visit_call(self, node):
        call_object = node.object_name.accept(self)

        # Case of function object
        if call_object.obj_type == ObjectType.FUNC:
            # Create a new scope
            self.env.enter_scope(call_object.env)

            # Evaluate the arguments
            arg_values = list()
            for arg in node.call_args:
                val = arg.accept(self)
                arg_values.append(val)

            if len(arg_values) != call_object.arity:
                # TODO: Add error handling for mismatched arity
                print("Not enough values!")

            # Add arguments to the current environment
            for arg_pair in zip(call_object.args, arg_values):
                self.env.peek().add_symbol(arg_pair[0].lexeme, arg_pair[1], True)

            for stmnt in call_object.body:
                stmnt.accept(self)

            self.env.exit_scope()

        elif call_object.obj_type == ObjectType.CLASS_DEF:
            return Class_Instance_Object(
                call_object.class_name, call_object.class_methods
            )

    def visit_dot_node(self, node):
        l = node.left.accept(self)
        if l.obj_type == ObjectType.CLASS_INSTANCE:
            val = l.get_field(node.right.lexeme)
            if val is not None:
                return val
            else:
                # TODO: Throw error for field not existing.
                print("Value does not exist")
        # TODO: Throw error here for object not being callable.
        else:
            print("Not class instance")
