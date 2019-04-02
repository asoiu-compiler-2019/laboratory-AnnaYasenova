from tag import Tag
from tokenType import Token


class SymbolTable:

    def __init__(self):
        self.table = dict()
        self.table["&&"] = Token(Tag.AND, "&&")
        self.table["||"] = Token(Tag.OR, "||")
        self.table["=="] = Token(Tag.EQ, "==")
        self.table["<"] = Token(Tag.LT, "<")
        self.table[">"] = Token(Tag.RT, ">")
        self.table["<="] = Token(Tag.LT_EQ, "<=")
        self.table[">="] = Token(Tag.RT_EQ, ">=")
        self.table["+"] = Token(Tag.PLUS, "+")
        self.table["-"] = Token(Tag.MINUS, "-")
        self.table["*"] = Token(Tag.TIMES, "*")
        self.table["/"] = Token(Tag.DIV, "/")
        self.table["%"] = Token(Tag.MOD, "%")
        self.table["("] = Token(Tag.LPAREN, "(")
        self.table[")"] = Token(Tag.RPAREN, ")")
        self.table["["] = Token(Tag.LBRACKET, "[")
        self.table["]"] = Token(Tag.RBRACKET, "]")
        self.table["{"] = Token(Tag.LBRACE, "{")
        self.table["}"] = Token(Tag.RBRACE, "}")
        self.table[";"] = Token(Tag.SEMI, ";")
        self.table[","] = Token(Tag.COMMA, ",")
        self.table["="] = Token(Tag.ASSIGN, "=")
        self.table["not"] = Token(Tag.NOT, "not")
        self.table["ugu"] = Token(Tag.BOOLEAN_LITERAL_TRUE, "ugu")
        self.table["net"] = Token(Tag.BOOLEAN_LITERAL_FALSE, "net")
        

        self.table["->"] = Token(Tag.DIRECTION_UP, "->")
        self.table["<-"] = Token(Tag.DIRECTION_DOWN, "<-")   
        self.table["main"] = Token(Tag.MAIN, "main")
        self.table["boolean"] = Token(Tag.BOOLEAN, "boolean")
        self.table["integer"] = Token(Tag.INTEGER, "integer")
        self.table["float"] = Token(Tag.FLOAT, "float")
        self.table["string"] = Token(Tag.STRING, "string")
        self.table["direction"] = Token(Tag.DIRECTION, "direction")
        self.table["rate"] = Token(Tag.RATE, "rate")
        self.table["trend"] = Token(Tag.TREND, "trend")
        self.table["trader"] = Token(Tag.TRADER, "trader")
        self.table["name"] = Token(Tag.NAME, "name")
        self.table["pair"] = Token(Tag.PAIR, "pair")
        self.table["let"] = Token(Tag.LET, "let")
        self.table["if"] = Token(Tag.IF, "if")
        self.table["else"] = Token(Tag.ELSE, "else")
        self.table["elif"] = Token(Tag.ELIF, "elif")
        self.table["for"] = Token(Tag.FOR, "for")
        self.table["return"] = Token(Tag.RETURN, "return")

    def include(self, lexeme, tag):
        token = self.table.get(lexeme, None)

        if not token:
            token = Token(tag, lexeme)
            self.table[lexeme] = token

        return token

    def __len__(self):
        return len(self.table)

    def __getitem__(self, item):
        for token in self.table.values():
            if token.lexeme.lower() == item.lower():
                return token

        return None

    def __str__(self):
        print(self.table)
