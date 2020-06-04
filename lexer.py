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

    def advance(self):
        """ Advance the current character by one and return it. If there is no next character,
            return None."""
        if self.curr_idx + 1 < self.input_len:
            self.curr_idx += 1
            self.curr_char = self.text[self.curr_idx]
            return self.curr_char
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

    def lex_ident(self):
        ident_str = str()
        while self.curr_char not in [" "]:
            ident_str += self.curr_char
            self.advance()
        return ident_str

    def lex_num(self):
        pass

    def __tokenize(self):
        """ Tokenize the current text sequence and return the tokens generated. """
        while self.curr_char is not None:
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
                if self.peek() == "="
                    self.token_stream.append(Token(Tok_Type.NEQ))
                else:
                    self.token_stream.append(Token(Tok_Type.BANG))
            elif self.curr_char == "=":
                if self.peek() == "="
                    self.token_stream.append(Token(Tok_Type.EQ))
                else:
                    self.token_stream.append(Token(Tok_Type.ASSIGN))
            elif self.curr_char == "<":
                if self.peek() == "="
                    self.token_stream.append(Token(Tok_Type.LTE))
                else:
                    self.token_stream.append(Token(Tok_Type.LT))
            elif self.curr_char == ">":
                if self.peek() == "="
                    self.token_stream.append(Token(Tok_Type.GTE))
                else:
                    self.token_stream.append(Token(Tok_Type.GT))
            elif self.curr_char in ['$', '@', '?'] or self.curr_char.isalpha():
                self.lex_ident()
            elif self.curr_char.isdigit():
                self.lex_num()
            
        

    def tokenize_file(self, filename):
        pass

    def tokenize_string(self, input_str):
        pass
