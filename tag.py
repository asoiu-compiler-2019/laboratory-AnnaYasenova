from enum import Enum, unique

try:
    from enum import auto
except ImportError: 
    __my_enum_auto_id = 0
    def auto() -> int:
        global __my_enum_auto_id
        i = __my_enum_auto_id
        __my_enum_auto_id += 1
        return i

@unique
class Tag(Enum):
    # Language keyword
    MAIN = auto() #
    VOID = auto()
    BOOLEAN = auto() #
    INTEGER = auto() #
    FLOAT = auto() #
    STRING = auto() #
    DIRECTION = auto() #
    RATE = auto() #
    TREND = auto() #
    TRADER = auto() #
    NAME = auto() #
    PAIR = auto() #
    LET = auto() #
    IF = auto() #
    ELSE = auto() #
    #ELIF = auto() #
    WHILE = auto() #
    RETURN = auto() #
    FUNCTION = auto()
    LPAREN = auto() #
    RPAREN = auto() #
    LBRACKET = auto() #
    RBRACKET = auto() #
    LBRACE = auto() #
    RBRACE = auto() #
    SEMI = auto() #
    COMMA = auto() #
    ASSIGN = auto() #
    NOT = auto() #

    DOT = auto()
    
    AND = auto() #
    OR = auto() #
    EQ = auto() #
    LT = auto() #
    RT = auto() #
    LT_EQ = auto() #
    RT_EQ = auto() #
    PLUS = auto() #
    MINUS = auto() #
    TIMES = auto() #
    DIV = auto() #
    MOD = auto() #
    
    DIRECTION_UP = auto() #
    DIRECTION_DOWN = auto() #

    IDENTIFIER = auto() #
    BOOLEAN_LITERAL_TRUE = auto() #
    BOOLEAN_LITERAL_FALSE = auto() #
    INTEGER_LITERAL = auto() #
    FLOAT_LITERAL = auto() #
    CHARACTER_LITERAL = auto() #
    STRING_LITERAL = auto() #
    END_OF_FILE = auto() #
    
    BOOLEAN_TYPE = auto()
    INTEGER_TYPE = auto()
    FLOAT_TYPE = auto()
    STRING_TYPE = auto()

    UNKNOWN = auto()


"""


EURUSD.price = 1.36;
output("accessing complex type var field");
output(EURUSD.price);
output("it works omg i'm so hyped");

function_call();
print("this print should be after function call");



print("accessing user type accessToken");
print(Revan730.accessToken);


"""