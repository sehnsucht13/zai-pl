from zai.tokens import TokType, Token
from zai.parse import Parser
import zai.ast_nodes as nodes
from zai.internal_error import InternalParseError
import pytest


def test_add_assign():
    # let id = 4;
    tok_stream = [
        Token(TokType.ID, "id"),
        Token(TokType.SUBASSIGN),
        Token(TokType.INT, 4),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]

    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    assign_node = parse_tree.stmnts[0]

    assert isinstance(parse_tree, nodes.ProgramNode) is True
    assert isinstance(assign_node, nodes.SubassignNode) is True
    assert assign_node.symbol_path is None
    assert isinstance(assign_node.symbol_name, nodes.SymbolNode) and assign_node.symbol_name.val == "id"
    assert isinstance(assign_node.decrement, nodes.IntNode) and assign_node.decrement.val == 4

    # Omit the value to be assigned like "let id = ;"
    tok_stream = [Token(TokType.ID, "id"), Token(TokType.SUBASSIGN), Token(TokType.SEMIC), Token(TokType.EOF)]

    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        parse_tree = p.parse()

    # Omit the variable name like "let  = 4 ;"
    tok_stream = [Token(TokType.SUBASSIGN), Token(TokType.INT, 4), Token(TokType.SEMIC), Token(TokType.EOF)]

    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        parse_tree = p.parse()


def test_add_assign():
    # let id = 4;
    tok_stream = [
        Token(TokType.ID, "id"),
        Token(TokType.ADDASSIGN),
        Token(TokType.INT, 4),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]

    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    assign_node = parse_tree.stmnts[0]

    assert isinstance(parse_tree, nodes.ProgramNode) is True
    assert isinstance(assign_node, nodes.AddassignNode) is True
    assert assign_node.symbol_path is None
    assert isinstance(assign_node.symbol_name, nodes.SymbolNode) and assign_node.symbol_name.val == "id"
    assert isinstance(assign_node.increment, nodes.IntNode) and assign_node.increment.val == 4

    # Omit the value to be assigned like "let id = ;"
    tok_stream = [Token(TokType.ID, "id"), Token(TokType.ADDASSIGN), Token(TokType.SEMIC), Token(TokType.EOF)]

    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        parse_tree = p.parse()

    # Omit the variable name like "let  = 4 ;"
    tok_stream = [Token(TokType.ADDASSIGN), Token(TokType.INT, 4), Token(TokType.SEMIC), Token(TokType.EOF)]

    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        parse_tree = p.parse()


def test_reassign():
    # let id = 4;
    tok_stream = [
        Token(TokType.ID, "id"),
        Token(TokType.ASSIGN),
        Token(TokType.INT, 4),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]

    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    assign_node = parse_tree.stmnts[0]

    assert isinstance(parse_tree, nodes.ProgramNode) is True
    assert isinstance(assign_node, nodes.ReassignBinNode) is True
    assert assign_node.symbol_path is None
    assert isinstance(assign_node.symbol_name, nodes.SymbolNode) and assign_node.symbol_name.val == "id"
    assert isinstance(assign_node.value, nodes.IntNode) and assign_node.value.val == 4

    # Omit the value to be assigned like "let id = ;"
    tok_stream = [Token(TokType.ID, "id"), Token(TokType.ASSIGN), Token(TokType.SEMIC), Token(TokType.EOF)]

    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        parse_tree = p.parse()

    # Omit the variable name like "let  = 4 ;"
    tok_stream = [Token(TokType.ASSIGN), Token(TokType.INT, 4), Token(TokType.SEMIC), Token(TokType.EOF)]

    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        parse_tree = p.parse()


def test_new_assignment():
    # let id = 4;
    tok_stream = [
        Token(TokType.LET),
        Token(TokType.ID, "id"),
        Token(TokType.ASSIGN),
        Token(TokType.INT, 4),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]

    p = Parser(tok_stream, "")
    parse_tree = p.parse()
    assign_node = parse_tree.stmnts[0]

    assert isinstance(parse_tree, nodes.ProgramNode) is True
    assert isinstance(assign_node, nodes.NewAssignBinNode) is True
    assert assign_node.symbol_path is None
    assert isinstance(assign_node.symbol_name, nodes.SymbolNode) and assign_node.symbol_name.val == "id"
    assert isinstance(assign_node.value, nodes.IntNode) and assign_node.value.val == 4

    # Omit the value to be assigned like "let id = ;"
    tok_stream = [
        Token(TokType.LET),
        Token(TokType.ID, "id"),
        Token(TokType.ASSIGN),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]

    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        parse_tree = p.parse()

    # Omit the variable name like "let  = 4 ;"
    tok_stream = [
        Token(TokType.LET),
        Token(TokType.ASSIGN),
        Token(TokType.INT, 4),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]

    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        parse_tree = p.parse()
