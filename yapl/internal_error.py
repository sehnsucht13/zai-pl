class InternalSyntaxErr(Exception):
    "Exception used when a syntax error is encountered during parsing."

    def __init__(self, error_msg, line_num=0, col_num=0):
        self.error_msg = error_msg
        # Line and column number data
        self.line_num = line_num
        self.col_num = col_num
