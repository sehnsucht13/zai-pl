""" Class used to convert an input string into a sequence of valid language tokens."""
from yapl.tokens import Tok_Type, Token, keywords


class Lexer:
    def __init__(self):
        self.text = None
        self.token_stream = list()
        # Current char observed
        self.curr_char = None
        # Current index within the input stream
        self.curr_idx = -1
        # Total length of input stream
        self.input_len = 0

        self.curr_lin_num = 0
        self.curr_col_num = 0

        # Characters which break up identification tokens
        self.ident_sep = "\n\t#;(),[]*/+-<=>!{}\"' "

    def advance(self):
        """ Advance the current character by one and return it. If there is no next character,
            return None."""
        if self.curr_idx + 1 < self.input_len:
            self.curr_idx += 1
            self.curr_char = self.text[self.curr_idx]
            self.curr_col_num += 1
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

    def reverse(self):
        if self.curr_idx > 0 and self.curr_char is not None:
            self.curr_idx -= 1
            self.curr_char = self.text[self.curr_idx]
            return self.curr_char
        return None

    def _tokenize_ident(self):
        """ Tokenize a single identifier and return it."""
        ident_str = str(self.curr_char)
        # ident_str += self.curr_char
        while self.peek() is not None and self.peek() not in self.ident_sep:
            self.advance()
            ident_str += self.curr_char
        return ident_str

    def _tokenize_num(self):
        """ Tokenize a single integer number and return it."""
        num_str = str()
        num_str += self.curr_char
        while self.peek() is not None and self.peek() in "1234567890":
            self.advance()
            num_str += self.curr_char
        return int(num_str)

    def _tokenize_str(self):
        str_content = str()
        while True:
            if self.curr_char is None:
                self.token_stream.append(
                    Token(
                        Tok_Type.STRING,
                        str_content,
                        self.curr_lin_num,
                        self.curr_col_num,
                    )
                )
                return
            elif self.curr_char != "\\" and self.peek() == '"':
                str_content += self.curr_char
                self.token_stream.append(
                    Token(
                        Tok_Type.STRING,
                        str_content,
                        self.curr_lin_num,
                        self.curr_col_num,
                    )
                )
                self.advance()
                self.token_stream.append(
                    Token(Tok_Type.DQUOTE, self.curr_lin_num, self.curr_col_num)
                )
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
                self.token_stream.append(
                    Token(Tok_Type.LROUND, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == ")":
                self.token_stream.append(
                    Token(Tok_Type.RROUND, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == ",":
                self.token_stream.append(
                    Token(Tok_Type.COMMA, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == ";":
                self.token_stream.append(
                    Token(Tok_Type.SEMIC, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "{":
                self.token_stream.append(
                    Token(Tok_Type.LCURLY, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "}":
                self.token_stream.append(
                    Token(Tok_Type.RCURLY, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "[":
                self.token_stream.append(
                    Token(Tok_Type.LSQUARE, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "]":
                self.token_stream.append(
                    Token(Tok_Type.RSQUARE, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "-":
                self.token_stream.append(
                    Token(Tok_Type.MINUS, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "+":
                self.token_stream.append(
                    Token(Tok_Type.PLUS, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "/":
                self.token_stream.append(
                    Token(Tok_Type.DIV, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "*":
                self.token_stream.append(
                    Token(Tok_Type.MUL, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == '"':
                self.token_stream.append(
                    Token(Tok_Type.DQUOTE, self.curr_lin_num, self.curr_col_num)
                )
                # Skip over the current character which is a double quote
                self.advance()
                self._tokenize_str()
            elif self.curr_char == "'":
                self.token_stream.append(
                    Token(Tok_Type.QUOTE, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "!":
                if self.peek() == "=":
                    self.token_stream.append(
                        Token(Tok_Type.NEQ, self.curr_lin_num, self.curr_col_num)
                    )
                    self.advance()
                else:
                    self.token_stream.append(
                        Token(Tok_Type.BANG, self.curr_lin_num, self.curr_col_num)
                    )
            elif self.curr_char == "=":
                if self.peek() == "=":
                    self.token_stream.append(
                        Token(Tok_Type.EQ, self.curr_lin_num, self.curr_col_num)
                    )
                    self.advance()
                else:
                    self.token_stream.append(
                        Token(Tok_Type.ASSIGN, self.curr_lin_num, self.curr_col_num)
                    )
            elif self.curr_char == "<":
                if self.peek() == "=":
                    self.token_stream.append(
                        Token(Tok_Type.LTE, self.curr_lin_num, self.curr_col_num)
                    )
                    self.advance()
                else:
                    self.token_stream.append(
                        Token(Tok_Type.LT, self.curr_lin_num, self.curr_col_num)
                    )
            elif self.curr_char == ">":
                if self.peek() == "=":
                    self.token_stream.append(
                        Token(Tok_Type.GTE, self.curr_lin_num, self.curr_col_num)
                    )
                    self.advance()
                else:
                    self.token_stream.append(
                        Token(Tok_Type.GT, self.curr_lin_num, self.curr_col_num)
                    )
            elif self.curr_char in ["$", "@", "?"] or self.curr_char.isalpha():
                # Store the column at the start of the identifier
                ident_start_col = self.curr_col_num
                ident = self._tokenize_ident()
                token = keywords.get(
                    ident,
                    Token(Tok_Type.ID, ident, self.curr_lin_num, ident_start_col),
                )
                self.token_stream.append(token)
            elif self.curr_char.isdigit():
                # Store the column at the start of the number
                num_start_col = self.curr_col_num
                num = self._tokenize_num()
                self.token_stream.append(
                    Token(Tok_Type.NUM, num, self.curr_lin_num, num_start_col)
                )

        # Add final EOF token to indicate end of token stream
        self.token_stream.append(Token(Tok_Type.EOF))

    def _reset_internal_state(self):
        self.input_len = len(self.text)

        # Reset all other variables
        self.token_stream = list()
        self.curr_char = None
        self.curr_idx = 0
        self.input_len = 0
        self.curr_lin_num = 0
        self.curr_col_num = 0

    def tokenize_string(self, input_str):
        """ Tokenize a single input string. Returns the token stream produced."""
        if self.text is not None:
            self.text = input_str
            self._reset_internal_state()

        # set input text string and its length
        self.text = input_str
        self.input_len = len(input_str)

        if self.input_len > 0:
            self.__tokenize()
            return self.token_stream
        else:
            return [Token(Tok_Type.EOF)]
