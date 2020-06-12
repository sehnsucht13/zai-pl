""" Class used to convert an input string into a sequence of valid language tokens."""
from yapl.tokens import Tok_Type, Token, keywords


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

        self.curr_lin_num = 0
        self.curr_col_num = 0

        # Characters which break up identification tokens
        self.ident_sep = "\n\t#(),[]*/+-<=>!{}\"' "

    def advance(self):
        """ Advance the current character by one and return it. If there is no next character,
            return None."""
        if self.curr_char is None and self.curr_idx == 0:
            self.curr_char = self.text[self.curr_idx]
            return self.curr_char
        elif self.curr_idx + 1 < self.input_len:
            self.curr_idx += 1
            self.curr_char = self.text[self.curr_idx]
            self.curr_col_num += 1
            return self.curr_char
        elif self.curr_char is None:
            return None
        else:
            self.curr_char = None
            return None

    def reverse(self):
        if self.curr_idx > 0 and self.curr_char is not None:
            self.curr_idx -= 1
            self.curr_char = self.text[self.curr_idx]
            return self.curr_char
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
        while self.peek() is not None and self.peek() not in self.ident_sep:
            self.advance()
            ident_str += self.curr_char
        return ident_str

    def __tokenize_num(self):
        """ Tokenize a single integer number and return it."""
        num_str = str()
        num_str += self.curr_char
        while self.peek() is not None and self.peek() in "1234567890":
            self.advance()
            num_str += self.curr_char
        return int(num_str)

    def collect_str(self):
        str_content = str()
        while True:
            if self.curr_char is None:
                self.token_stream.append(Token(Tok_Type.STRING, str_content))
                return
            elif self.curr_char != "\\" and self.peek() == '"':
                str_content += self.curr_char
                self.token_stream.append(Token(Tok_Type.STRING, str_content))
                self.advance()
                self.token_stream.append(Token(Tok_Type.DQUOTE))
                return
            else:
                str_content += self.curr_char
                self.advance()

        # while self.peek() != None or (self.peek() != '"' and self.curr_char != "\\"):
        #     str_content.appen

    def __tokenize(self):
        """ Tokenize the current text sequence and return the tokens generated. """
        while self.advance() is not None:
            if self.curr_char == "\n":
                # Increment line numbers
                self.curr_lin_num += 1
                # Reset current column number
                self.curr_col_num = 0
            elif self.curr_char == "(":
                self.token_stream.append(Token(Tok_Type.LROUND))
            elif self.curr_char == ")":
                self.token_stream.append(Token(Tok_Type.RROUND))
            elif self.curr_char == ",":
                self.token_stream.append(Token(Tok_Type.COMMA))
            elif self.curr_char == ";":
                self.token_stream.append(Token(Tok_Type.SEMIC))
            elif self.curr_char == "{":
                self.token_stream.append(Token(Tok_Type.LCURLY))
            elif self.curr_char == "}":
                self.token_stream.append(Token(Tok_Type.RCURLY))
            elif self.curr_char == "[":
                self.token_stream.append(Token(Tok_Type.LSQUARE))
            elif self.curr_char == "]":
                self.token_stream.append(Token(Tok_Type.RSQUARE))
            elif self.curr_char == "-":
                self.token_stream.append(Token(Tok_Type.MINUS))
            elif self.curr_char == "+":
                self.token_stream.append(Token(Tok_Type.PLUS))
            elif self.curr_char == "/":
                self.token_stream.append(Token(Tok_Type.DIV))
            elif self.curr_char == "*":
                self.token_stream.append(Token(Tok_Type.MUL))
            elif self.curr_char == '"':
                self.token_stream.append(Token(Tok_Type.DQUOTE))
                # Skip over the current character which is a double quote
                self.advance()
                self.collect_str()
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
            elif self.curr_char in ["$", "@", "?"] or self.curr_char.isalpha():
                ident = self.__tokenize_ident()
                token = keywords.get(ident, Token(Tok_Type.ID, ident))
                self.token_stream.append(token)
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
        if self.text is not None:
            self.text = input_str
            self.input_len = len(input_str)

            # Reset all other variables
            self.token_stream = list()
            self.curr_char = None
            self.curr_idx = 0
            self.input_len = 0
            self.curr_lin_num = 0
            self.curr_col_num = 0

        # set input text string and its length
        self.text = input_str
        self.input_len = len(input_str)

        if self.input_len > 0:
            self.__tokenize()
            return self.token_stream
        else:
            return [Token(Tok_Type.EOF)]
