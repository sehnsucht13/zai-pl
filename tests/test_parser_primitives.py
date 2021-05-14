from zai.tokens import TokType, Token
from zai.parse import Parser
import zai.ast_nodes as nodes
import pytest


def test_array():
    # Empty Array
    tok_stream = [Token(TokType.LSQUARE), Token(TokType.RSQUARE), Token(TokType.SEMIC), Token(TokType.EOF)]
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    assert isinstance(parse_tree, nodes.ProgramNode) is True
    assert isinstance(parse_tree.stmnts[0], nodes.ArrayNode) is True

    # Array with one element
    tok_stream = [
        Token(TokType.LSQUARE),
        Token(TokType.NUM, 1),
        Token(TokType.RSQUARE),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    array_node = parse_tree.stmnts[0]
    assert isinstance(parse_tree, nodes.ProgramNode) is True
    assert isinstance(array_node, nodes.ArrayNode) is True
    assert isinstance(array_node.elements[0], nodes.NumNode) is True and array_node.elements[0].val == 1

    # Array with several elements
    tok_stream = [
        Token(TokType.LSQUARE),
        Token(TokType.NUM, 1),
        Token(TokType.COMMA),
        Token(TokType.NUM, 2),
        Token(TokType.RSQUARE),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    array_node = parse_tree.stmnts[0]
    assert isinstance(parse_tree, nodes.ProgramNode) is True
    assert isinstance(array_node, nodes.ArrayNode) is True
    assert isinstance(array_node.elements[0], nodes.NumNode) is True and array_node.elements[0].val == 1
    assert isinstance(array_node.elements[1], nodes.NumNode) is True and array_node.elements[1].val == 2


def create_tok_stream(values):
    """Helper function used to generate a token stream from a list of token types and values."""
    tok_stream = []

    for token_type, token_value, _ in values:
        if token_type == TokType.STRING:
            tok_stream.append(Token(TokType.DQUOTE))
        tok_stream.append(Token(token_type, token_value))
        if token_type == TokType.STRING:
            tok_stream.append(Token(TokType.DQUOTE))
        tok_stream.append(Token(TokType.SEMIC))
    tok_stream.append(Token(TokType.EOF))

    return tok_stream


def compare_parsed_output(original_values, parse_tree):
    """Helper function used to compare a simple flat list of AST nodes to a pre-determined list of tokens."""
    assert isinstance(parse_tree, nodes.ProgramNode) == True
    for output in zip(parse_tree.stmnts, original_values):
        assert isinstance(output[0], output[1][2]) is True
        assert output[0].val == output[1][1]


def test_string_parsing():
    values = [(TokType.STRING, "one", nodes.StringNode)]
    tok_stream = create_tok_stream(values)
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    compare_parsed_output(values, parse_tree)

    values = [
        (TokType.STRING, "one", nodes.StringNode),
        (TokType.STRING, "two", nodes.StringNode),
        (TokType.STRING, "three", nodes.StringNode),
    ]
    tok_stream = create_tok_stream(values)
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    compare_parsed_output(values, parse_tree)


def test_nil():
    values = [(TokType.NIL, None, nodes.NilNode)]
    tok_stream = create_tok_stream(values)
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    compare_parsed_output(values, parse_tree)

    values = [
        (TokType.NIL, None, nodes.NilNode),
        (TokType.NIL, None, nodes.NilNode),
        (TokType.NIL, None, nodes.NilNode),
    ]
    tok_stream = create_tok_stream(values)
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    compare_parsed_output(values, parse_tree)


def test_boolean_parsing():
    values = [(TokType.TRUE, TokType.TRUE, nodes.BoolNode)]
    tok_stream = create_tok_stream(values)
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    compare_parsed_output(values, parse_tree)

    values = [(TokType.FALSE, TokType.FALSE, nodes.BoolNode)]
    tok_stream = create_tok_stream(values)
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    compare_parsed_output(values, parse_tree)

    values = [
        (TokType.FALSE, TokType.FALSE, nodes.BoolNode),
        (TokType.TRUE, TokType.TRUE, nodes.BoolNode),
        (TokType.FALSE, TokType.FALSE, nodes.BoolNode),
    ]
    tok_stream = create_tok_stream(values)
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    compare_parsed_output(values, parse_tree)


def test_integer_parsing():
    values = [(TokType.NUM, 1, nodes.NumNode)]
    tok_stream = create_tok_stream(values)
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    compare_parsed_output(values, parse_tree)

    values = [
        (TokType.NUM, 1, nodes.NumNode),
        (TokType.NUM, 0, nodes.NumNode),
        (TokType.NUM, -1, nodes.NumNode),
    ]
    tok_stream = create_tok_stream(values)
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    compare_parsed_output(values, parse_tree)


# Mixed tests for primitives
def test_mixed_primitive_values():
    tok_stream = [
        Token(TokType.NUM, 4),
        Token(TokType.SEMIC),
        Token(TokType.DQUOTE),
        Token(TokType.STRING, "Hello world"),
        Token(TokType.DQUOTE),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    assert isinstance(parse_tree, nodes.ProgramNode) is True
    num_node = parse_tree.stmnts[0]
    string_node = parse_tree.stmnts[1]
    assert isinstance(num_node, nodes.NumNode) and num_node.val == 4
    assert isinstance(string_node, nodes.StringNode) and string_node.val == "Hello world"

    tok_stream = [
        Token(TokType.LSQUARE),
        Token(TokType.NUM, 1),
        Token(TokType.COMMA),
        Token(TokType.NUM, 2),
        Token(TokType.RSQUARE),
        Token(TokType.SEMIC),
        Token(TokType.DQUOTE),
        Token(TokType.STRING, "Hello world"),
        Token(TokType.DQUOTE),
        Token(TokType.SEMIC),
        Token(TokType.TRUE),
        Token(TokType.SEMIC),
        Token(TokType.FALSE),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    assert isinstance(parse_tree, nodes.ProgramNode) is True
    array_node = parse_tree.stmnts[0]
    string_node = parse_tree.stmnts[1]
    true_bool_node = parse_tree.stmnts[2]
    false_bool_node = parse_tree.stmnts[3]
    assert isinstance(array_node, nodes.ArrayNode) is True
    assert isinstance(array_node.elements[0], nodes.NumNode) and isinstance(array_node.elements[1], nodes.NumNode)
    assert array_node.elements[0].val == 1 and array_node.elements[1].val == 2
    assert isinstance(string_node, nodes.StringNode) and string_node.val == "Hello world"
    assert isinstance(true_bool_node, nodes.BoolNode) and true_bool_node.val == TokType.TRUE
    assert isinstance(false_bool_node, nodes.BoolNode) and false_bool_node.val == TokType.FALSE
