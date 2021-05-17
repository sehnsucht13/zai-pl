from zai.tokens import TokType, Token
from zai.parse import Parser
import zai.ast_nodes as nodes
from zai.internal_error import InternalParseError
import pytest


def test_basic_import():
    tok_stream = [
        Token(TokType.IMPORT),
        Token(TokType.ID, "Hello"),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    import_node = p.import_statement()
    assert isinstance(import_node, nodes.ImportNode) and import_node.module_name == "Hello"


def test_renamed_import():
    tok_stream = [
        Token(TokType.IMPORT),
        Token(TokType.ID, "Hello"),
        Token(TokType.AS),
        Token(TokType.ID, "World"),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    import_node = p.import_statement()
    assert (
        isinstance(import_node, nodes.ImportNode)
        and import_node.module_name == "Hello"
        and import_node.import_name == "World"
    )


def test_import_missing_module():
    # Test importing with missing id "import ;"
    tok_stream = [
        Token(TokType.IMPORT),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        import_node = p.import_statement()

    tok_stream = [
        Token(TokType.IMPORT),
        Token(TokType.AS),
        Token(TokType.ID, "World"),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        import_node = p.import_statement()


def test_import_missing_local_name():
    # Test "import "Hello" as ;"
    tok_stream = [
        Token(TokType.IMPORT),
        Token(TokType.ID, "Hello"),
        Token(TokType.AS),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        import_node = p.import_statement()
