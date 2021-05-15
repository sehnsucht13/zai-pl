from zai.tokens import TokType, Token
from zai.parse import Parser
import zai.ast_nodes as nodes
from zai.internal_error import InternalParseError
import pytest

def test_function_call_with_args():
    # Call with one arg
    tok_stream = [
        Token(TokType.ID, "hello"),
        Token(TokType.LROUND),
        Token(TokType.NUM, 4),
        Token(TokType.RROUND),
        Token(TokType.EOF)
    ]
    p = Parser(tok_stream, "")
    call_node = p.call_or_access()
    assert isinstance(call_node, nodes.CallNode) and len(call_node.call_args) == 1
    assert isinstance(call_node.call_args[0], nodes.NumNode) and call_node.call_args[0].val == 4

    # Call with one arg
    tok_stream = [
        Token(TokType.ID, "hello"),
        Token(TokType.LROUND),
        Token(TokType.NUM, 4),
        Token(TokType.COMMA),
        Token(TokType.NUM, 5),
        Token(TokType.RROUND),
        Token(TokType.EOF)
    ]
    p = Parser(tok_stream, "")
    call_node = p.call_or_access()
    assert isinstance(call_node, nodes.CallNode) and len(call_node.call_args) == 2
    assert isinstance(call_node.call_args[0], nodes.NumNode) and call_node.call_args[0].val == 4
    assert isinstance(call_node.call_args[1], nodes.NumNode) and call_node.call_args[1].val == 5

def test_call_without_comma():
    tok_stream = [
        Token(TokType.ID, "hello"),
        Token(TokType.LROUND),
        Token(TokType.NUM, 4),
        Token(TokType.NUM, 5),
        Token(TokType.RROUND),
        Token(TokType.EOF)
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        call_node = p.call_or_access()

def test_function_call_without_args():
    # Call with one arg
    tok_stream = [
        Token(TokType.ID, "hello"),
        Token(TokType.LROUND),
        Token(TokType.RROUND),
        Token(TokType.EOF)
    ]
    p = Parser(tok_stream, "")
    call_node = p.call_or_access()
    assert isinstance(call_node, nodes.CallNode) and len(call_node.call_args) == 0

def test_call_missing_begin_bracket():
    tok_stream = [
        Token(TokType.ID, "hello"),
        Token(TokType.LROUND),
        Token(TokType.EOF)
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        call_node = p.call_or_access()


def test_call_missing_end_bracket():
    tok_stream = [
        Token(TokType.ID, "hello"),
        Token(TokType.RROUND),
        Token(TokType.EOF)
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        call_node = p.call_or_access()

