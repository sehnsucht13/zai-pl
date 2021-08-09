from zai.tokens import TokType, Token
from zai.parse import Parser
import zai.ast_nodes as nodes
from zai.internal_error import InternalParseError
import pytest


def test_well_formed_block():
    # Empty block
    tok_stream = [
        Token(TokType.LCURLY),
        Token(TokType.RCURLY),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    block_node = p.block()

    assert isinstance(block_node, nodes.BlockNode)

    # Block with contents
    tok_stream = [
        Token(TokType.LCURLY),
        Token(TokType.INT, 1),
        Token(TokType.PLUS),
        Token(TokType.INT, 2),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    block_node = p.block()

    assert isinstance(block_node, nodes.BlockNode)
    assert isinstance(block_node.stmnts[0], nodes.ArithBinNode) and block_node.stmnts[0].op == TokType.PLUS
    assert isinstance(block_node.stmnts[0].left, nodes.IntNode) and block_node.stmnts[0].left.val == 1
    assert isinstance(block_node.stmnts[0].right, nodes.IntNode) and block_node.stmnts[0].right.val == 2


def test_missing_opening_block():
    # Missing an opening "{" bracket
    tok_stream = [
        Token(TokType.RCURLY),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        block_node = p.block()


def test_missing_closing_block():
    pass
    tok_stream = [
        Token(TokType.LCURLY),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        block_node = p.block()
