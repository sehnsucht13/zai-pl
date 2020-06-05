""" Class used to convert an input string into a sequence of valid language tokens."""
from tokens import Tok_Type, Token

class Lexer:
    def __init__(self):
        self.text = None
        self.token_stream = list()
        # Current char observed
        self.curr_char = None
        # Current index within the input stream
        self.curr_idx = 0
        # Total length of input stream
        self.input_len = 0

        # Characters which break up identification tokens
        self.ident_sep = "#(),[]*/+-<=>!{}\"' "

    def advance(self):
        """ Advance the current character by one and return it. If there is no next character,
            return None."""
        if self.curr_char is None and self.curr_idx == 0:
            self.curr_char = self.text[self.curr_idx]
            return self.curr_char
        elif self.curr_idx + 1 < self.input_len:
            self.curr_idx += 1
            self.curr_char = self.text[self.curr_idx]
            return self.curr_char
        elif self.curr_char is None:
            return None
        else:
            self.curr_char = None
            return None
        

    def peek(self):
        """ Return the next character in the input text sequence. If there is no next
            character, return None."""
        if self.curr_idx + 1 < self.input_len:
            return self.text[self.curr_idx + 1]
        else:
            return None

    def __tokenize_ident(self):
        """ Tokenize a single identifier and return it."""
        ident_str = str()
        ident_str += self.curr_char
        while self.advance() is not None and self.curr_char not in self.ident_sep:
            ident_str += self.curr_char
            #self.advance()
        return ident_str

    def __tokenize_num(self):
        """ Tokenize a single integer number and return it."""
        num_str = str()
        num_str += self.curr_char
        while self.advance() is not None and self.curr_char in "1234567890":
            num_str += self.curr_char
            #self.advance()
        return int(num_str)

    def __tokenize(self):
        """ Tokenize the current text sequence and return the tokens generated. """
        while self.advance() != None:
            if self.curr_char == "(":
                self.token_stream.append(Token(Tok_Type.LRBRACE))
            elif self.curr_char == ")":
                self.token_stream.append(Token(Tok_Type.RRBRACE))
            elif self.curr_char == ",":
                self.token_stream.append(Token(Tok_Type.COMMA))
            elif self.curr_char == ",":
                self.token_stream.append(Token(Tok_Type.COMMA))
            elif self.curr_char == "-":
                self.token_stream.append(Token(Tok_Type.MINUS))
            elif self.curr_char == "+":
                self.token_stream.append(Token(Tok_Type.PLUS))
            elif self.curr_char == "/":
                self.token_stream.append(Token(Tok_Type.DIV))
            elif self.curr_char == "/":
                self.token_stream.append(Token(Tok_Type.MUL))
            elif self.curr_char == "\"":
                self.token_stream.append(Token(Tok_Type.DQUOTE))
            elif self.curr_char == "'":
                self.token_stream.append(Token(Tok_Type.QUOTE))
            elif self.curr_char == "!":
                if self.peek() == "=":
                    self.token_stream.append(Token(Tok_Type.NEQ))
                    self.advance()
                else:
                    self.token_stream.append(Token(Tok_Type.BANG))
            elif self.curr_char == "=":
                if self.peek() == "=":
                    self.token_stream.append(Token(Tok_Type.EQ))
                    self.advance()
                else:
                    self.token_stream.append(Token(Tok_Type.ASSIGN))
            elif self.curr_char == "<":
                if self.peek() == "=":
                    self.token_stream.append(Token(Tok_Type.LTE))
                    self.advance()
                else:
                    self.token_stream.append(Token(Tok_Type.LT))
            elif self.curr_char == ">":
                if self.peek() == "=":
                    self.token_stream.append(Token(Tok_Type.GTE))
                    self.advance()
                else:
                    self.token_stream.append(Token(Tok_Type.GT))
            elif self.curr_char in ['$', '@', '?'] or self.curr_char.isalpha():
                ident = self.__tokenize_ident()
                self.token_stream.append(Token(Tok_Type.ID, ident))
            elif self.curr_char.isdigit():
                num = self.__tokenize_num()
                self.token_stream.append(Token(Tok_Type.NUM, num))

        # Add final EOF token to indicate end of token stream
        self.token_stream.append(Token(Tok_Type.EOF))

    def tokenize_file(self, filename):
        """ Tokenize an input file. If the fule does not exist, return a runtime error. 
            Otheriwse returns the token stream produced."""
        pass

    def tokenize_string(self, input_str):
        """ Tokenize a single input string. Returns the token stream produced."""
        self.text = input_str
        self.input_len = len(input_str)
        if self.input_len > 0:
            self.__tokenize()
            return self.token_stream
        else: 
            return [Token(Tok_Type.EOF)]

"""
if __name__ == "__main__":
    l = Lexer()
    stream = l.tokenize_string("a$141_bc")
    print(stream)
"""
