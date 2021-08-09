from zai.tokens import TokType, Token
from zai.parse import Parser
import zai.ast_nodes as nodes
import pytest


def binary_nodes_repeat_operator_helper(operations, node_type):
    """Test arbitrary binary nodes up to depth of 2. The main purpose of this is to see if the order or
    operations is respected."""
    for curr_op in operations:
        tok_stream = (
            [Token(TokType.INT, 1)]
            + [Token(curr_op)]
            + [Token(TokType.INT, 2), Token(TokType.SEMIC), Token(TokType.EOF)]
        )
        p = Parser(tok_stream, "")
        parse_tree = p.parse()
        bin_node = parse_tree.stmnts[0]

        assert isinstance(parse_tree, nodes.ProgramNode) is True
        assert isinstance(bin_node, node_type) is True
        assert isinstance(bin_node.left, nodes.IntNode) is True and bin_node.left.val == 1
        assert isinstance(bin_node.right, nodes.IntNode) is True and bin_node.right.val == 2
        assert bin_node.op == curr_op

        # Depth of two
        tok_stream2 = (
            [Token(TokType.INT, 1)]
            + [Token(curr_op)]
            + [Token(TokType.INT, 2)]
            + [Token(curr_op)]
            + [Token(TokType.INT, 3)]
            + [Token(TokType.SEMIC), Token(TokType.EOF)]
        )
        p = Parser(tok_stream2, "")
        parse_tree2 = p.parse()
        nested_bin_node = parse_tree2.stmnts[0]

        assert isinstance(parse_tree2, nodes.ProgramNode) is True
        assert isinstance(nested_bin_node, node_type) is True

        assert isinstance(nested_bin_node.left, node_type) is True

        assert isinstance(nested_bin_node.left.left, nodes.IntNode) is True and nested_bin_node.left.left.val == 1
        assert nested_bin_node.left.op == curr_op
        assert isinstance(nested_bin_node.left.right, nodes.IntNode) is True and nested_bin_node.left.right.val == 2

        assert isinstance(nested_bin_node.right, nodes.IntNode) is True and nested_bin_node.right.val == 3
        assert nested_bin_node.op == curr_op


def test_logic_binary_nodes():
    operations = [TokType.AND, TokType.OR]
    node_type = nodes.LogicBinNode
    binary_nodes_repeat_operator_helper(operations, node_type)


def test_comparison_binary_nodes():
    operations = [TokType.LTE, TokType.LT, TokType.GTE, TokType.GT]
    node_type = nodes.RelopBinNode
    binary_nodes_repeat_operator_helper(operations, node_type)


def test_eq_binary_nodes():
    operations = [TokType.EQ, TokType.NEQ]
    node_type = nodes.EqBinNode
    binary_nodes_repeat_operator_helper(operations, node_type)


def test_arith_binary_nodes():
    operations = [TokType.PLUS, TokType.DIV, TokType.MUL, TokType.MINUS]
    node_type = nodes.ArithBinNode
    binary_nodes_repeat_operator_helper(operations, node_type)

    # 4 * 2 - 3 == (4 * 2) - 3
    tok_stream2 = (
        [Token(TokType.INT, 4)]
        + [Token(TokType.MUL)]
        + [Token(TokType.INT, 2)]
        + [Token(TokType.MINUS)]
        + [Token(TokType.INT, 3)]
        + [Token(TokType.SEMIC), Token(TokType.EOF)]
    )
    parser = Parser(tok_stream2, "")
    parse_tree = parser.parse()
    nested_bin_node = parse_tree.stmnts[0]
    assert isinstance(parse_tree, nodes.ProgramNode) is True
    assert isinstance(nested_bin_node, nodes.ArithBinNode) is True
    assert isinstance(nested_bin_node.left, nodes.ArithBinNode) is True

    assert isinstance(nested_bin_node.left.left, nodes.IntNode) is True and nested_bin_node.left.left.val == 4
    assert nested_bin_node.left.op == TokType.MUL
    assert isinstance(nested_bin_node.left.right, nodes.IntNode) is True and nested_bin_node.left.right.val == 2

    assert isinstance(nested_bin_node.right, nodes.IntNode) is True and nested_bin_node.right.val == 3
    assert nested_bin_node.op == TokType.MINUS

    # 3 - 4 * 2 == 3 - (4 * 2)
    tok_stream2 = (
        [Token(TokType.INT, 3)]
        + [Token(TokType.MINUS)]
        + [Token(TokType.INT, 4)]
        + [Token(TokType.MUL)]
        + [Token(TokType.INT, 2)]
        + [Token(TokType.SEMIC), Token(TokType.EOF)]
    )
    parser = Parser(tok_stream2, "")
    parse_tree = parser.parse()
    nested_bin_node = parse_tree.stmnts[0]
    assert isinstance(parse_tree, nodes.ProgramNode) is True
    assert isinstance(nested_bin_node, nodes.ArithBinNode) is True

    assert isinstance(nested_bin_node.left, nodes.IntNode) is True and nested_bin_node.left.val == 3
    assert nested_bin_node.op == TokType.MINUS

    assert isinstance(nested_bin_node.right, nodes.ArithBinNode) is True
    assert isinstance(nested_bin_node.right.left, nodes.IntNode) is True and nested_bin_node.right.left.val == 4
    assert isinstance(nested_bin_node.right.right, nodes.IntNode) is True and nested_bin_node.right.right.val == 2
    assert nested_bin_node.right.op == TokType.MUL
