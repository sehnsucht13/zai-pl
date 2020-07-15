from yapl.tokens import Tok_Type
from yapl.internal_error import InternalRuntimeErr
from yapl.objects import *
from yapl.env import Environment, Scope
from yapl.lexer import Lexer
from yapl.parse import Parser
from yapl.utils import is_atom, is_truthy, pprint_internal_object, read_module_contents

import os


class Visitor:
    def __init__(self, environment):
        "Class implementing the visitor pattern which is used to evaluate language structures."
        self.env = environment
        self.repl_mode = False

    def set_repl_mode(self):
        self.repl_mode = True

    def visit(self, ast_root):
        """
        Main entry point for all AST roots.
        """
        return ast_root.accept(self)

    def visit_program(self, node):
        for stmnt in node.stmnts:
            ret_val = stmnt.accept(self)

            if ret_val is not None:
                if ret_val.obj_type == ObjectType.RETURN:
                    msg = '"return" statement not used outside of a function or class method!'
                    raise InternalRuntimeErr(msg)
                if ret_val.obj_type == ObjectType.BREAK:
                    msg = '"break" statement not used within a loop or a switch block!'
                    raise InternalRuntimeErr(msg)
                elif ret_val.obj_type == ObjectType.CONTINUE:
                    msg = '"continue" statement not used within a loop!'
                    raise InternalRuntimeErr(msg)
            if is_atom(ret_val) and self.repl_mode:
                pprint_internal_object(ret_val)

    def visit_num(self, node):
        return Num_Object(node.val)

    def visit_symbol(self, node):
        # Retrieve symbol from env
        curr_scope = self.env.peek()
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
            return left + right
        elif node.op == Tok_Type.MINUS:
            return left - right
        elif node.op == Tok_Type.MUL:
            return left * right
        elif node.op == Tok_Type.DIV:
            return left / right

    def visit_logic(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        # >
        if node.op == Tok_Type.AND:
            return left & right
        # >=
        elif node.op == Tok_Type.OR:
            return left | right

    def visit_relop(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        # >
        if node.op == Tok_Type.GT:
            return left > right
        # >=
        elif node.op == Tok_Type.GTE:
            return left >= right
        # <
        elif node.op == Tok_Type.LT:
            return left < right
        # <=
        elif node.op == Tok_Type.LTE:
            return left <= right

    def visit_eq(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        if node.op == Tok_Type.EQ:
            return left == right
        elif node.op == Tok_Type.NEQ:
            return left != right

    def visit_unary(self, node):
        result = node.value.accept(self)
        if node.op == Tok_Type.MINUS:
            return -node
        elif node.op == Tok_Type.BANG:
            return ~node

    def visit_if(self, node):
        # Evaluate each condition and execute block if it is true
        for cond in node.conditions:
            cond_value = cond[0].accept(self)
            if is_truthy(cond_value):
                return cond[1].accept(self)

            if node.else_block is not None:
                return node.else_block.accept(self)

    def visit_while(self, node):
        cond_value = node.condition.accept(self)
        while is_truthy(cond_value):
            # Detect any usage of return
            ret_val = node.body.accept(self)
            if ret_val is not None:
                # Exit loop early using return
                if ret_val.obj_type == ObjectType.BREAK:
                    return
                # There is no need to do anything here. We need to reevaluate the test
                # condition for the loop.
                elif ret_val.obj_type == ObjectType.CONTINUE:
                    continue
                # "return" value is floated up
                else:
                    return ret_val
            cond_value = node.condition.accept(self)

    def visit_print(self, node):
        print_value = node.expr.accept(self)
        pprint_internal_object(print_value)

    def visit_replace_assign(self, node):
        symbol = node.symbol
        # Evaluate the right hand side containing the value to be assigned
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
        # Evaluate the right hand side containing the value which will be assigned
        value = node.value.accept(self)

        assert symbol is not None
        assert value is not None

        scope = self.env.peek()
        scope.add_symbol(symbol, value, True)

    def visit_scope_block(self, node):
        # Create a new scope to evaluate the current block in
        parent_env = self.env.peek()
        self.env.enter_scope(parent_env)
        for stmnt in node.stmnts:
            # Detect any usage of return
            ret_val = stmnt.accept(self)
            if ret_val is not None and ret_val.obj_type in [
                ObjectType.RETURN,
                ObjectType.BREAK,
                ObjectType.CONTINUE,
            ]:
                self.env.exit_scope()
                return ret_val

        self.env.exit_scope()

    def visit_switch(self, node):
        # Create a new scope to evaluate the current block in
        test_cond = node.switch_cond.accept(self)
        # Index of the first switch case which has a true test condition
        start_case_idx = None
        for idx, switch_case in enumerate(node.switch_cases):
            case_cond = switch_case[0].accept(self)
            if case_cond == test_cond:
                start_case_idx = idx
                break

        for _, case_body in node.switch_cases[start_case_idx:]:
            ret_val = case_body.accept(self)
            # TODO: Handle "return" statements here
            if ret_val is not None:
                if ret_val.obj_type == ObjectType.BREAK:
                    return
                else:
                    return ret_val

        if node.default_case is not None:
            return node.default_case.accept(self)

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
                msg = 'function "{}"" accepts {} arguments but only {} were given!'.format(
                    call_object.name, len(arg_values), call_object.arity
                )
                raise InternalRuntimeErr(msg)

            # Add arguments to the current environment
            for arg_pair in zip(call_object.args, arg_values):
                self.env.peek().add_symbol(arg_pair[0].lexeme, arg_pair[1], True)

            for stmnt in call_object.body:
                ret_val = stmnt.accept(self)
                if ret_val is not None:
                    if ret_val.obj_type == ObjectType.RETURN:
                        return ret_val.value
                    elif ret_val.obj_type == ObjectType.BREAK:
                        msg = '"break" statement not used within a loop or a switch block!'
                        raise InternalRuntimeErr(msg)
                    elif ret_val.obj_type == ObjectType.CONTINUE:
                        msg = '"continue" statement not used within a loop!'
                        raise InternalRuntimeErr(msg)

            self.env.exit_scope()
            return Nil_Object()

        elif call_object.obj_type == ObjectType.CLASS_DEF:
            return Class_Instance_Object(
                call_object.class_name, call_object.class_methods
            )
        elif call_object.obj_type == ObjectType.CLASS_METHOD:
            # Create a new scope
            # self.env.enter_scope()
            self.env.enter_scope(call_object.class_env)
            print(self.env.peek().parent.scope)

            # Evaluate the arguments
            arg_values = list()
            for arg in node.call_args:
                val = arg.accept(self)
                arg_values.append(val)

            if len(arg_values) != call_object.arity:
                msg = 'function "{}" accepts {} arguments but only {} were given!'.format(
                    call_object.name, len(arg_values), call_object.arity
                )
                raise InternalRuntimeErr(msg)

            # Add arguments to the current environment
            for arg_pair in zip(call_object.args, arg_values):
                self.env.peek().add_symbol(arg_pair[0].lexeme, arg_pair[1], True)

            for stmnt in call_object.body:
                ret_val = stmnt.accept(self)
                if ret_val is not None:
                    if ret_val.obj_type == ObjectType.RETURN:
                        return ret_val.value
                    elif ret_val.obj_type == ObjectType.BREAK:
                        msg = '"break" statement not used within a loop or a switch block!'
                        raise InternalRuntimeErr(msg)
                    elif ret_val.obj_type == ObjectType.CONTINUE:
                        msg = '"continue" statement not used within a loop!'
                        raise InternalRuntimeErr(msg)

            self.env.exit_scope()
            return Nil_Object()

    def visit_dot_node(self, node):
        l = node.left.accept(self)
        if isinstance(l, Scope):
            val = l.lookup_symbol(node.right.lexeme)
            if val is not None:
                return val
            else:
                err_msg = "Current class environment does not contain the variable {}".format(
                    node.right.lexeme
                )
                raise InternalRuntimeErr(err_msg)
        elif l.obj_type == ObjectType.CLASS_INSTANCE:
            val = l.get_field(node.right.lexeme)
            if val is not None:
                return val
            else:
                err_msg = 'Class instance "{}" of class "{}" does not contain a field with name "{}"'.format(
                    node.left.val, l.class_name, node.right.lexeme
                )
                raise InternalRuntimeErr(err_msg)
        elif l.obj_type == ObjectType.MODULE:
            val = l.namespace.lookup_symbol(node.right.lexeme)
            if val is not None:
                return val
            else:
                err_msg = "Module {} does not contain the variable {}".format(
                    l.name, node.right.lexeme
                )
                raise InternalRuntimeErr(err_msg)
        else:
            err_msg = "variable {} is not an instance of a class!".format(node.left.val)
            raise InternalRuntimeErr(err_msg)

    def visit_this(self, node):
        curr_scope = self.env.peek()
        while curr_scope.parent != None:
            curr_scope = curr_scope.parent
        return curr_scope

    def visit_return(self, node):
        return_val = node.expr.accept(self)
        return Return_Object(return_val)

    def visit_continue(self, node):
        return Continue_Object()

    def visit_break(self, node):
        return Break_Object()

    def visit_do_while(self, node):
        # First execution of the body which always happens
        ret_val = node.body.accept(self)
        if ret_val is not None:
            # Exit loop early using return
            if ret_val.obj_type == ObjectType.BREAK:
                return
            # There is no need to do anything here. We need to reevaluate the test
            # condition for the loop.
            elif ret_val.obj_type == ObjectType.CONTINUE:
                pass
            # "return" value is floated up
            else:
                return ret_val

        # Subsequent executions which depend on the ocndition
        cond_value = node.cond.accept(self)
        while is_truthy(cond_value):
            # Detect any usage of return
            ret_val = node.body.accept(self)
            if ret_val is not None:
                # Exit loop early using return
                if ret_val.obj_type == ObjectType.BREAK:
                    return
                # There is no need to do anything here. We need to reevaluate the test
                # condition for the loop.
                elif ret_val.obj_type == ObjectType.CONTINUE:
                    continue
                # "return" value is floated up
                else:
                    return ret_val
            cond_value = node.cond.accept(self)

    def visit_array(self, node):
        eval_elem = list()
        for elem in node.elements:
            elem_val = elem.accept(self)
            eval_elem.append(elem_val)

        return Array_Object(eval_elem)

    def visit_array_access(self, node):
        array_obj = node.array_name.accept(self)
        array_idx = node.array_pos.accept(self)
        if array_idx.value < array_obj.size:
            return array_obj.elements[array_idx.value]
        else:
            msg = "Array has a size of {} but you want to access position {}".format(
                array_obj.size, array_idx.value
            )
            raise InternalRuntimeErr(msg)

    def visit_incr(self, node):
        node_val = node.value.accept(self)
        node_val.value += 1
        return node_val

    def visit_decr(self, node):
        node_val = node.value.accept(self)
        node_val.value -= 1
        return node_val

    def visit_nil(self, node):
        return Nil_Object()

    def visit_import(self, node):
        module_name = node.filename + ".yapl"
        file_text = read_module_contents(module_name)
        if file_text is None:
            err_msg = "Module {} could not be found within the interpreter path.".format(
                node.filename
            )
            raise InternalRuntimeErr(err_msg)

        lexer = Lexer()
        tok_stream = lexer.tokenize_string(file_text)
        parser = Parser(tok_stream)
        root = parser.parse()

        import_env = Environment()
        import_visitor = Visitor(import_env)
        import_visitor.visit(root)
        import_scope = import_visitor.env.peek()

        self.env.peek().add_symbol(
            node.filename, Module_Object(node.filename, import_scope), True
        )
        print(self.env.peek().scope)
