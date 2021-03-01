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

"""Module contains a visitor class implementation used to execute the AST
produced by the parser."""
from zai.ast_nodes import Array_Access_Node
from zai.tokens import Tok_Type
from zai.internal_error import InternalRuntimeErr
from zai.env import Environment, Scope
from zai.lexer import Lexer
from zai.parse import Parser
from zai.utils import is_truthy, read_module_contents
from zai.objects import (
    ObjectType,
    Bool_Object,
    Nil_Object,
    Num_Object,
    Func_Object,
    String_Object,
    Return_Object,
    Class_Def_Object,
    Class_Instance_Object,
    Continue_Object,
    Break_Object,
    Array_Object,
    Module_Object,
)


class Visitor:
    def __init__(self, environment):
        """
        Class implementing the visitor pattern which is used to evaluate
        language structures.
        """
        self.env = environment

    def visit(self, ast_root):
        """
        Main entry point for all AST roots.
        """
        return ast_root.accept(self)

    def visit_program(self, node):
        for stmnt in node.stmnts:
            ret_val = stmnt.accept(self)

            if ret_val is not None and ret_val.obj_type in [
                ObjectType.RETURN,
                ObjectType.BREAK,
                ObjectType.CONTINUE,
            ]:
                if ret_val.obj_type == ObjectType.RETURN:
                    msg = (
                        '"return" statement not used outside of a function or class'
                        "method!"
                    )
                    raise InternalRuntimeErr(msg)
                elif ret_val.obj_type == ObjectType.BREAK:
                    msg = '"break" statement not used within a loop or a switch block!'
                    raise InternalRuntimeErr(msg)
                elif ret_val.obj_type == ObjectType.CONTINUE:
                    msg = '"continue" statement not used within a loop!'
                    raise InternalRuntimeErr(msg)
            # else:
            #     return ret_val

    def visit_num(self, node):
        return Num_Object(node.val)

    def visit_symbol(self, node):
        # Retrieve symbol from env
        curr_scope = self.env.peek()
        symbol_val = curr_scope.lookup_symbol(node.val)

        if symbol_val is None:
            err_msg = 'Variable "{}" is not defined!.'.format(node.val)
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
            return -result
        elif node.op == Tok_Type.BANG:
            return ~result

    def visit_if(self, node):
        # Evaluate each condition and execute block if it is true
        for cond_block in node.cond_blocks:
            cond_value = cond_block["cond"].accept(self)
            if is_truthy(cond_value):
                return cond_block["block"].accept(self)

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
        print(str(print_value))

    def visit_replace_assign(self, node):
        symbol_namespace = None
        symbol_name = None
        new_value = node.value.accept(self)
        if node.symbol_path is not None:
            symbol_namespace = node.symbol_path.accept(self)
        else:
            symbol_namespace = self.env.peek()

        if isinstance(node.symbol_name, Array_Access_Node):
            symbol_name = node.symbol_name.array_name.val
            array_index = node.symbol_name.array_pos.accept(self)
            if array_index.obj_type != ObjectType.NUM:
                err_msg = 'Array cannot be "{}" !'.format(array_index.obj_type)
                raise InternalRuntimeErr(err_msg)

            array_instance = symbol_namespace.lookup_symbol(symbol_name)
            if array_instance is None:
                err_msg = (
                    'The array "{}" does not exist within the current' "environment!"
                ).format(symbol_name)
                raise InternalRuntimeErr(err_msg)
            else:
                if array_index.value < array_instance.size:
                    array_instance.elements[array_index.value] = new_value
                else:
                    err_msg = '"{}" exceeds the length of the array "{}"!'.format(
                        array_index.value, symbol_name
                    )
                    raise InternalRuntimeErr(err_msg)
        else:
            symbol_name = node.symbol_name.val
            if isinstance(symbol_namespace, Scope):
                status = symbol_namespace.replace_variable(symbol_name, new_value)
                if status is False:
                    err_msg = (
                        'Variable "{}" cannot be reasigned because it has not'
                        "been initialized!"
                    ).format(symbol_name)
                    raise InternalRuntimeErr(err_msg)
            elif symbol_namespace.obj_type in [
                ObjectType.MODULE,
                ObjectType.CLASS_INSTANCE,
            ]:
                status = symbol_namespace.namespace.replace_variable(
                    symbol_name, new_value
                )
                if status is False:
                    err_msg = (
                        'Variable "{}" cannot be reasigned because it has not'
                        "been initialized!"
                    ).format(symbol_name)
                    raise InternalRuntimeErr(err_msg)

    def visit_new_assign(self, node):
        # Symbol name will always be an id node
        symbol_name = node.symbol_name.val
        # Evaluate the right hand side containing the value which will be assigned
        value = node.value.accept(self)

        assert symbol_name is not None, (
            "Attempting to assign a new variable without a symbol name in"
            "visit_new_assign."
        )
        assert (
            value is not None
        ), "Attempting to assign a non existant value in visit_new_assign."

        # Find if a path to the variable exists
        symbol_path = None
        if node.symbol_path is None:
            # We must be trying to access a variable within the current scope.
            scope = self.env.peek()
            scope.new_variable(symbol_name, value)
        else:
            symbol_path = node.symbol_path.accept(self)
            if isinstance(symbol_path, Scope):
                symbol_path.new_variable(symbol_name, value)
            elif symbol_path.obj_type in [ObjectType.MODULE, ObjectType.CLASS_INSTANCE]:
                symbol_path.namespace.new_variable(symbol_name, value)

    def visit_scope_block(self, node):
        # Create a new scope to evaluate the current block in
        parent_env = self.env.peek()
        self.env.enter_scope(parent_env)
        for stmnt in node.stmnts:
            ret_val = stmnt.accept(self)
            # Bubble up any flow statements
            if ret_val is not None and ret_val.obj_type in [
                ObjectType.RETURN,
                ObjectType.BREAK,
                ObjectType.CONTINUE,
            ]:
                self.env.exit_scope()
                return ret_val

        self.env.exit_scope()

    def visit_switch(self, node):
        # Evaluate the condition used for testing all cases
        test_cond = node.switch_cond.accept(self)

        # Find the index of the first switch case which is true.
        start_case_idx = None
        for idx, switch_case in enumerate(node.switch_cases):
            case_cond = switch_case[0].accept(self)
            if is_truthy(case_cond == test_cond):
                start_case_idx = idx
                break

        # Execute all switch cases after that until we encounter a "break" keyword
        # or a "return"/"continue" keywords.
        for _, case_body in node.switch_cases[start_case_idx:]:
            ret_val = case_body.accept(self)
            if ret_val is not None:
                if ret_val.obj_type == ObjectType.BREAK:
                    return
                else:
                    return ret_val

        # Execute the default case if it is provided.
        if node.default_case is not None:
            return node.default_case.accept(self)

    def visit_func_def(self, node):
        curr_scope = self.env.peek()
        # Register the function in the current frame
        curr_scope.new_variable(
            node.name, Func_Object(node.name, node.args, node.body, curr_scope)
        )

    def visit_class_def(self, node):
        """
        Keyword Arguments:
        node -- Class definition node
        """
        curr_scope = self.env.peek()
        # Register the class in the scope
        curr_scope.new_variable(
            node.class_name, Class_Def_Object(node.class_name, node.class_methods)
        )

    def __run_native_function(self, func_object, call_args):
        if func_object.arity != len(call_args):
            raise InternalRuntimeErr(
                "Function '{}' accepts only {} arguments but {} were given".format(
                    func_object.name, func_object.arity, len(call_args)
                )
            )

        evaluated_args = list()
        for arg in call_args:
            val = arg.accept(self)
            evaluated_args.append(val)

        # Using the "*" operator will destructure the list of evaluated internal object
        # arguments into the arguments which the function accepts.
        return func_object.body(*evaluated_args)

    def __run_internal_function(self, func_object, call_args):
        """
        Runs the function represented by func_object. The arguments passed are supplied
        by the call_args in the form of a list.
        """
        # Evaluate the arguments
        arg_values = list()
        for arg in call_args:
            val = arg.accept(self)
            arg_values.append(val)

        if len(arg_values) != func_object.arity:
            msg = 'function "{}" accepts only {} arguments but {} were given!'.format(
                func_object.name,
                func_object.arity,
                len(arg_values),
            )
            raise InternalRuntimeErr(msg)

        if func_object.obj_type == ObjectType.FUNC:
            # Create a new scope
            self.env.enter_scope(func_object.env)
        elif func_object.obj_type == ObjectType.CLASS_METHOD:
            self.env.enter_scope(func_object.class_env)
            self.env.peek().new_variable("this", func_object.class_env)

        # Add arguments to the current environment
        for arg_pair in zip(func_object.args, arg_values):
            # print("Adding pair to environment", arg_pair)
            self.env.peek().new_variable(arg_pair[0].lexeme, arg_pair[1])

        for stmnt in func_object.body:
            ret_val = stmnt.accept(self)
            if ret_val is not None and ret_val.obj_type in [
                ObjectType.RETURN,
                ObjectType.BREAK,
                ObjectType.CONTINUE,
            ]:
                if ret_val.obj_type == ObjectType.RETURN:
                    return ret_val
                elif ret_val.obj_type == ObjectType.BREAK:
                    msg = '"break" statement not used within a loop or a switch block!'
                    raise InternalRuntimeErr(msg)
                elif ret_val.obj_type == ObjectType.CONTINUE:
                    msg = '"continue" statement not used within a loop!'
                    raise InternalRuntimeErr(msg)
        return None

    def visit_call(self, node):
        call_object = node.object_name.accept(self)

        # Case of function object
        if call_object.obj_type in [ObjectType.FUNC, ObjectType.CLASS_METHOD]:
            ret_val = self.__run_internal_function(call_object, node.call_args)
            self.env.exit_scope()
            if ret_val is None or ret_val.value is None:
                return Nil_Object()
            else:
                return ret_val.value

        elif call_object.obj_type == ObjectType.NATIVE_FUNC:
            return self.__run_native_function(call_object, node.call_args)

        elif call_object.obj_type == ObjectType.CLASS_DEF:
            instance_ptr = Class_Instance_Object(
                call_object.class_name, call_object.class_methods
            )
            # Enter new scope to register "this" namespace
            self.env.enter_scope(instance_ptr.namespace)
            self.env.peek().new_variable("this", instance_ptr.namespace)

            class_constructor = instance_ptr.get_field("constructor")
            if class_constructor is None and len(node.call_args) != 0:
                raise InternalRuntimeErr(
                    (
                        "Class '{}' does not have a constructor method but "
                        "initialization detected {} arguments passed."
                    ).format(call_object.class_name, len(node.call_args))
                )
            elif class_constructor is not None:
                self.__run_internal_function(class_constructor, node.call_args)

            self.env.exit_scope()
            return instance_ptr
        else:
            raise InternalRuntimeErr("Object is not callable!")

    def visit_dot_node(self, node):
        left_side = node.left.accept(self)
        if isinstance(left_side, Scope):
            val = left_side.lookup_symbol(node.right.val)
            if val is not None:
                return val
            else:
                err_msg = "Current environment does not contain the variable {}".format(
                    node.right.val
                )
                raise InternalRuntimeErr(err_msg)
        elif left_side.obj_type == ObjectType.MODULE:
            val = left_side.namespace.lookup_symbol(node.right.val)
            if val is not None:
                return val
            else:
                err_msg = "Module environment does not contain the variable {}".format(
                    node.right.lexeme
                )
                raise InternalRuntimeErr(err_msg)
        elif left_side.obj_type == ObjectType.CLASS_INSTANCE:
            val = left_side.get_field(node.right.val)
            if val is not None:
                return val
            else:
                err_msg = (
                    'Class instance "{}" of class "{}" does not contain a field '
                    'with name "{}"'
                ).format(node.left.val, left_side.class_name, node.right.val)
                raise InternalRuntimeErr(err_msg)
        else:
            err_msg = "variable {} is not accessible!".format(node.left.val)
            raise InternalRuntimeErr(err_msg)

    def visit_this(self, node):
        curr_scope = self.env.peek()
        while curr_scope.parent is not None:
            curr_scope = curr_scope.parent
        return curr_scope

    def visit_return(self, node):
        if node.expr is None:
            return Return_Object(Nil_Object())

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
        if array_obj.obj_type != ObjectType.ARRAY:
            err_str = "Object is not an array and cannot be accessed using '[]'!"
            raise InternalRuntimeErr(err_str)
        if array_idx.obj_type != ObjectType.NUM:
            err_str = "Array index is not a number but a '{}'!".format(
                str(array_idx.obj_type)
            )
            raise InternalRuntimeErr(err_str)
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
        module_name = node.module_name + ".zai"
        module_path, module_text = read_module_contents(module_name)
        if module_text is None:
            err_msg = (
                "Module {} could not be found within the interpreter path.".format(
                    node.filename
                )
            )
            raise InternalRuntimeErr(err_msg)

        # Initialize lexer and environment used to execute module contents
        lexer = Lexer()
        import_env = Environment()

        # Lex and parse module contents
        tok_stream = lexer.tokenize_string(module_text)
        parser = Parser(tok_stream, module_text)
        root = parser.parse()

        import_visitor = Visitor(import_env)
        import_visitor.visit(root)
        # Take the module's global environment to be added to the namespace.
        import_scope = import_visitor.env.peek()

        # Determine the name with which the module will be accessed.
        module_env_name = node.module_name
        if node.import_name is not None:
            module_env_name = node.import_name

        self.env.peek().new_variable(
            module_env_name,
            Module_Object(node.module_name, module_path, import_scope, module_env_name),
        )

    def visit_add_assign(self, node):
        # Symbol name will always be an id node
        symbol_name = node.symbol_name.val
        # Evaluate the right hand side containing the value which will be assigned
        new_value = node.increment.accept(self)

        # Find if a path to the variable exists
        symbol_path = None
        if node.symbol_path is None:
            current_scope = self.env.peek()
            old_val = current_scope.lookup_symbol(symbol_name)
            status = current_scope.replace_variable(symbol_name, old_val + new_value)
            if status is False:
                err_msg = (
                    'Variable "{}" cannot be reasigned because it does not exist'
                    " within the environment."
                ).format(symbol_name)
                raise InternalRuntimeErr(err_msg)
        else:
            symbol_path = node.symbol_path.accept(self)
            if isinstance(symbol_path, Scope):
                old_val = symbol_path.lookup_symbol(symbol_name)
                status = symbol_path.replace_variable(symbol_name, old_val + new_value)
                if status is False:
                    err_msg = (
                        'Variable "{}" cannot be reasigned because it does not'
                        "exist within the current class environment."
                    ).format(symbol_name)
                    raise InternalRuntimeErr(err_msg)
            elif symbol_path.obj_type in [ObjectType.MODULE, ObjectType.CLASS_INSTANCE]:
                old_val = symbol_path.namespace.lookup_symbol(symbol_name)
                status = symbol_path.namespace.replace_variable(
                    symbol_name, old_val + new_value
                )
                if status is False:
                    err_msg = (
                        'Variable "{}" cannot be reasigned because it does not '
                        "exist."
                    ).format(symbol_name)
                    raise InternalRuntimeErr(err_msg)

    def visit_sub_assign(self, node):
        # Symbol name will always be an id node
        symbol_name = node.symbol_name.val
        # Evaluate the right hand side containing the value which will be assigned
        new_value = node.decrement.accept(self)

        # Find if a path to the variable exists
        symbol_path = None
        if node.symbol_path is None:
            current_scope = self.env.peek()
            old_val = current_scope.lookup_symbol(symbol_name)
            status = current_scope.replace_variable(symbol_name, old_val - new_value)
            if status is False:
                err_msg = (
                    'Variable "{}" cannot be reasigned because it does not exist'
                    " within the  environment."
                ).format(symbol_name)
                raise InternalRuntimeErr(err_msg)
        else:
            symbol_path = node.symbol_path.accept(self)
            if isinstance(symbol_path, Scope):
                old_val = symbol_path.lookup_symbol(symbol_name)
                status = symbol_path.replace_variable(symbol_name, old_val - new_value)
                if status is False:
                    err_msg = (
                        'Variable "{}" cannot be reasigned because it does not '
                        "exist within the current class environment."
                    ).format(symbol_name)
                    raise InternalRuntimeErr(err_msg)
            elif symbol_path.obj_type in [ObjectType.MODULE, ObjectType.CLASS_INSTANCE]:
                old_val = symbol_path.namespace.lookup_symbol(symbol_name)
                status = symbol_path.namespace.replace_variable(
                    symbol_name, old_val - new_value
                )
                if status is False:
                    err_msg = (
                        'Variable "{}" cannot be reasigned because it does not '
                        "exist."
                    ).format(symbol_name)
                    raise InternalRuntimeErr(err_msg)
