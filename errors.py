class LexicalError:

    def __init__(self, symbol, line, column):
        self.symbol = symbol
        self.line = line
        self.column = column

    def __str__(self):
        return "\n>>>>>>>>>>>>>>>>>>>>>>>>>> Lexical Error >>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\"" \
               + self.symbol + "\" at " + str(self.line) + ":" \
               + str(self.column) \
               + " is not a valid symbol.\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n"


class CustomLexicalError:

    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return "\n>>>>>>>>>>>>>>>>>>>>>>>>>> Lexical Error >>>>>>>>>>>>>>>>>>>>>>>>>>>>\n" \
               + self.message + " at " + str(self.line) + ":" \
               + str(self.column) \
               + "\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n"


class SemanticError:

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "\n>>>>>>>>>>>>>>>>>>>>>>>>>> Semantic Error >>>>>>>>>>>>>>>>>>>>>>>>>>>>\n" \
               + self.message\
               + "\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n"


class CustomError:

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "\n>>>>>>>>>>>>>>>>>>>>>>>>>> Error >>>>>>>>>>>>>>>>>>>>>>>>>>>>\n" \
               + self.message\
               + "\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n"
