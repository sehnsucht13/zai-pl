from yapl.tokens import Tok_Type, Token
from yapl.parse import Parser
from yapl.ast_nodes import (
    String_Node,
    Program_Node,
    ID_Node,
    Num_Node,
    Bool_Node,
    Nil_Node,
)
from yapl.internal_error import InternalParseErr
import pytest


def test_nil():
    tok_list = [
        Token(Tok_Type.NIL),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(Nil_Node())
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    tok_list = [
        Token(Tok_Type.NIL),
        Token(Tok_Type.NIL),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    p = Parser(tok_list, "")
    with pytest.raises(InternalParseErr):
        parsed_program = p.parse()


def test_bool():
    tok_list = [
        Token(Tok_Type.TRUE),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(Bool_Node(Tok_Type.TRUE))
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    tok_list = [
        Token(Tok_Type.FALSE),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(Bool_Node(Tok_Type.FALSE))
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program


def test_id():
    tok_list = [
        Token(Tok_Type.ID, "Hello world"),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(ID_Node("Hello world"))
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    tok_list = [
        Token(Tok_Type.ID, ""),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(ID_Node(""))
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program


def test_num():
    tok_list = [
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(Num_Node(4))
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    tok_list = [
        Token(Tok_Type.NUM, 0),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(Num_Node(0))
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    tok_list = [
        Token(Tok_Type.NUM, -4),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(Num_Node(-4))
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program


def test_string():
    tok_list = [
        Token(Tok_Type.DQUOTE),
        Token(Tok_Type.STRING, "Hello world"),
        Token(Tok_Type.DQUOTE),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(String_Node("Hello world"))
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    tok_list = [
        Token(Tok_Type.DQUOTE),
        Token(Tok_Type.STRING, "Hello world"),
        Token(Tok_Type.DQUOTE),
        Token(Tok_Type.DQUOTE),
        Token(Tok_Type.STRING, "Hello world"),
        Token(Tok_Type.DQUOTE),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    p = Parser(tok_list, "")
    with pytest.raises(InternalParseErr):
        parsed_program = p.parse()
