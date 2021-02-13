from yapl.tokens import Tok_Type, Token
from yapl.parse import Parser
from yapl.ast_nodes import (
    Arith_Bin_Node,
    Bool_Node,
    Logic_Bin_Node,
    Relop_Bin_Node,
    New_Assign_Bin_Node,
    Replace_Assign_Bin_Node,
    Dot_Bin_Node,
    Num_Node,
    Program_Node,
)
from yapl.internal_error import InternalParseErr
import pytest


def test_arith():
    tok_list = [
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.MINUS, None),
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(
        Arith_Bin_Node(Num_Node(4), Token(Tok_Type.MINUS), Num_Node(4))
    )
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    # Test nesting operators of the same type
    tok_list = [
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.MINUS, None),
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.MINUS, None),
        Token(Tok_Type.NUM, 5),
        Token(Tok_Type.MINUS, None),
        Token(Tok_Type.NUM, 6),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(
        Arith_Bin_Node(
            Arith_Bin_Node(
                Arith_Bin_Node(Num_Node(4), Token(Tok_Type.MINUS), Num_Node(4)),
                Token(Tok_Type.MINUS),
                Num_Node(5),
            ),
            Token(Tok_Type.MINUS),
            Num_Node(6),
        )
    )
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    tok_list = [
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.MUL, None),
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(
        Arith_Bin_Node(Num_Node(4), Token(Tok_Type.MUL), Num_Node(4))
    )
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    tok_list = [
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.DIV, None),
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(
        Arith_Bin_Node(Num_Node(4), Token(Tok_Type.DIV), Num_Node(4))
    )
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    tok_list = [
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.PLUS, None),
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(
        Arith_Bin_Node(Num_Node(4), Token(Tok_Type.PLUS), Num_Node(4))
    )
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    # Test nesting operators
    tok_list = [
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.MINUS, None),
        Token(Tok_Type.NUM, 4),
        Token(Tok_Type.PLUS, None),
        Token(Tok_Type.NUM, 5),
        Token(Tok_Type.DIV, None),
        Token(Tok_Type.NUM, 6),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(
        Arith_Bin_Node(
            Arith_Bin_Node(Num_Node(4), Token(Tok_Type.MINUS), Num_Node(4)),
            Token(Tok_Type.PLUS),
            Arith_Bin_Node(
                Num_Node(5),
                Token(Tok_Type.DIV),
                Num_Node(6),
            ),
        ),
    )
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program


def test_logic():
    tok_list = [
        Token(Tok_Type.TRUE, None),
        Token(Tok_Type.AND, None),
        Token(Tok_Type.FALSE, None),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(
        Logic_Bin_Node(
            Bool_Node(Tok_Type.TRUE), Tok_Type.AND, Bool_Node(Tok_Type.FALSE)
        )
    )
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    tok_list = [
        Token(Tok_Type.TRUE, None),
        Token(Tok_Type.OR, None),
        Token(Tok_Type.FALSE, None),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.EOF),
    ]
    test_program = Program_Node()
    test_program.add_stmnt(
        Logic_Bin_Node(Bool_Node(Tok_Type.TRUE), Tok_Type.OR, Bool_Node(Tok_Type.FALSE))
    )
    p = Parser(tok_list, "")
    parsed_program = p.parse()
    assert parsed_program == test_program

    # Test nesting operators of the same type
    # tok_list = [
    #     Token(Tok_Type.NUM, 4),
    #     Token(Tok_Type.AND, None),
    #     Token(Tok_Type.NUM, 4),
    #     Token(Tok_Type.OR, None),
    #     Token(Tok_Type.NUM, 5),
    #     Token(Tok_Type.AND, None),
    #     Token(Tok_Type.NUM, 6),
    #     Token(Tok_Type.SEMIC),
    #     Token(Tok_Type.EOF),
    # ]
    # test_program = Program_Node()
    # test_program.add_stmnt(
    #     Logic_Bin_Node(
    #         Logic_Bin_Node(
    #             Logic_Bin_Node(Num_Node(4), Tok_Type.AND, Num_Node(4)),
    #             Tok_Type.OR,
    #             Num_Node(5),
    #         ),
    #         Tok_Type.AND,
    #         Num_Node(6),
    #     )
    # )
    # p = Parser(tok_list, "")
    # parsed_program = p.parse()
    # print("PArsd", parsed_program.stmnts[0])
    # assert parsed_program == test_program