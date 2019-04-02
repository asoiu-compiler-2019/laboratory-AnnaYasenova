from errors import CustomError
from lexer import *

class Statement:
    pass


class BlockStatement(Statement):
    def __init__(self, statements):
        self.statements = statements

    def get_statements_list(self):
        return self.statements


class FunctionParameter:
    def __init__(self, p_type, p_identifier):
        self.p_type = p_type
        self.p_identifier = p_identifier

    def get_type(self):
        return self.p_type

    def get_identifier(self):
        return self.p_identifier


class Func:
    def __init__(self, id, params, body, ret, native):
        self.id = id
        self.params = params
        self.body = body
        self.returnType = ret
        self.native = native

    def get_id(self):
        return self.id

    def return_params(self):
        return self.params

    def get_body(self):
        return self.body

    def get_return_type(self):
        return self.returnType

    def get_native_func(self):
        return self.native


class IfStatement(Statement):
    def __init__(self, cond_exp, true_stm, false_stm):
        self.cond_exp = cond_exp
        self.true_stm = true_stm
        self.false_stm = false_stm

    def get_cond_exp(self):
        return self.cond_exp

    def get_true_stm(self):
        return self.true_stm

    def get_true_stm_arr(self):
        block = BlockStatement([self.true_stm])
        return block.get_statements_list()

    def get_false_stm(self):
        return self.false_stm

    def get_false_stm_arr(self):
        block = BlockStatement([self.false_stm])
        return block.get_statements_list()

    def has_false_stm(self):
        return self.false_stm is not None


class WhileStatement(Statement):
    def __init__(self, cond_exp, loop_stm):
        self.cond_exp = cond_exp
        self.loop_stm = loop_stm

    def get_cond_exp(self):
        return self.cond_exp

    def get_loop_stm(self):
        return self.loop_stm


class VarDeclaration:

    def __init__(self, var_type, var_id, value=None):
        self.var_type = var_type
        self.var_id = var_id
        self.value = value

    def get_type(self):
        return self.var_type

    def get_id(self):
        return self.var_id

    def get_value(self):
        return self.value

    def set_value(self, v):
        self.value = v


# In[3]:


class Expression:

    def get_value(self):
        pass

    def evaluateType(self, s):
        pass

    def getIdentifiers(self):
        return []

    def evaluateValue(self, s):
       return self.value


class IntegerLiteral(Expression):

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def evaluateType(self, s):
        return Tag.INTEGER

    def evaluateValue(self, s):
        return self.value

    def getIdentifiers(self):
        return []

class FloatLiteral(Expression):

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def evaluateType(self, s):
        return Tag.FLOAT


class BooleanLiteral(Expression):

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def evaluateType(self, s):
        return Tag.BOOLEAN

    def evaluateValue(self, s):
        return self.get_value()

    def getIdentifiers(self):
        return []


class CharacterLiteral(Expression):

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def evaluateType(self, s):
        return Tag.STRING


class StringLiteral(Expression):

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def evaluateType(self, s):
        return Tag.STRING

    def evaluateValue(self, s):
        return self.get_value()

    def getIdentifiers(self):
        return []


class IdentifierExpression(Expression):

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def getIdentifiers(self):
        return [self.value]

    def evaluateType(self, s):
       return s.analyzer.find_variable_declaration(self.value, s).get_type()

    def evaluateValue(self, s):
        return s.interpreter.getVar(self.value, s).get_value()


class NotExpression(Expression):

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def getIdentifiers(self):
        return self.getIdentifiers()

    def evaluateType(self, s):
        type = self.value.evaluateType(s)
        if type != Tag.BOOLEAN:
            print(CustomError('SH??: Non - boolean type in logic operator expression \'{}\''.format(type)))
        return Tag.BOOLEAN

    def evaluateValue(self, s):
        value = self.value.evaluateValue(s)
        return not value


class AndExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def getIdentifiers(self):
        lhsIdentifiers = self.lhs.get_dentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)

    def evaluateType(self, s):
       lhsType = self.lhs.evaluateType(s)
       rhsType = self.rhs.evaluateType(s)
       if lhsType != rhsType:
           print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
       if lhsType != Tag.BOOLEAN:
          print(CustomError('SH??: Non - boolean type in logic operator expression \'{}\''.format(lhsType)))
       return Tag.BOOLEAN

    def evaluateValue(self, s):
       lhsValue = self.lhs.evaluateValue(s)
       rhsValue = self.rhs.evaluateValue(s)
       return lhsValue and rhsValue


class OrExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def getIdentifiers(self):
        lhsIdentifiers = self.lhs.get_dentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)

    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)
        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
        if lhsType != Tag.BOOLEAN:
            print(CustomError('SH??: Non - boolean type in logic operator expression \'{}\''.format(lhsType)))
        return Tag.BOOLEAN

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue or rhsValue


class EqualExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def getIdentifiers(self):
        lhsIdentifiers = self.lhs.get_dentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)


    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)
        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
        return Tag.BOOLEAN

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue == rhsValue

class NotEqualExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)

        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))

        return Tag.BOOLEAN

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue != rhsValue

    def get_dentifiers(self):
        lhsIdentifiers = self.lhs.getIdentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)

class LessThanExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)

        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
        if lhsType != Tag.INTEGER:
            print(CustomError('SH??: Non - integer type in integer - only operator expression {}'.format(lhsType)))
        return Tag.BOOLEAN

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue < rhsValue

    def get_dentifiers(self):
        lhsIdentifiers = self.lhs.getIdentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)


class GreaterThanExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)

        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
        if lhsType != Tag.INTEGER:
            print(CustomError('SH??: Non - integer type in integer - only operator expression {}'.format(lhsType)))
        return Tag.BOOLEAN

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue > rhsValue

    def get_dentifiers(self):
        lhsIdentifiers = self.lhs.getIdentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)

class LessThanEqualExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)

        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
        if lhsType != Tag.INTEGER:
            print(CustomError('SH??: Non - integer type in integer - only operator expression {}'.format(lhsType)))
        return Tag.BOOLEAN

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue <= rhsValue

    def get_dentifiers(self):
        lhsIdentifiers = self.lhs.getIdentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)


class GreaterThanEqualExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)

        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
        if lhsType != Tag.INTEGER:
            print(CustomError('SH??: Non - integer type in integer - only operator expression {}'.format(lhsType)))
        return Tag.BOOLEAN

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue >= rhsValue
        
    def get_dentifiers(self):
        lhsIdentifiers = self.lhs.getIdentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)

class PlusExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def getIdentifiers(self):
        lhsIdentifiers = self.lhs.get_dentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)

    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)
        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
        if (lhsType != Tag.INTEGER) and (lhsType != Tag.STRING):
            print(CustomError('SH??: Non-integer type in integer-only operator expression \'{}\''.format(lhsType)))
        return Tag.INTEGER

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue + rhsValue

class MinusExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def getIdentifiers(self):
        lhsIdentifiers = self.lhs.get_dentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)

    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)
        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
        if lhsType != Tag.INTEGER:
            print(CustomError('SH??: Non-integer type in integer-only operator expression \'{}\''.format(lhsType)))
        return Tag.INTEGER

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue - rhsValue

class NegativeExpression(Expression):
    def __init__(self, value):
        self.value = value
    def get_value(self):
        return self.value

    def evaluateType(self, s):
        type = self.value.evaluateType(s);
        if type != Tag.INTEGER:
            print(CustomError('SH??: Non-integer type in integer-only operator expression \'{}\''.format(type)))

        return Tag.INTEGER

    def evaluateValue(self, s):
        value = self.value.evaluateValue(s)
        return -value

    def getIdentifiers(self):
        return self.value.getIdentifiers()


class TimesExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def getIdentifiers(self):
        lhsIdentifiers = self.lhs.get_dentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)

    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)
        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
        if lhsType != Tag.INTEGER:
            print(CustomError('SH??: Non-integer type in integer-only operator expression \'{}\''.format(lhsType)))
        return Tag.lhsType

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue * rhsValue


class DivExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs

    def getIdentifiers(self):
        lhsIdentifiers = self.lhs.get_dentifiers()
        rhsIdentifiers = self.rhs.getIdentifiers()
        return lhsIdentifiers.append(rhsIdentifiers)

    def evaluateType(self, s):
        lhsType = self.lhs.evaluateType(s)
        rhsType = self.rhs.evaluateType(s)
        if lhsType != rhsType:
            print(CustomError('SH??: Non - matching expression types \'{}\' and \'{}\''.format(lhsType, rhsType)))
        if lhsType != Tag.INTEGER_LITERAL:
            print(CustomError('SH??: Non-integer type in integer-only operator expression \'{}\''.format(lhsType)))
        return Tag.lhsType

    def evaluateValue(self, s):
        lhsValue = self.lhs.evaluateValue(s)
        rhsValue = self.rhs.evaluateValue(s)
        return lhsValue / rhsValue


class ModExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getLHS(self):
        return self.lhs

    def getRHS(self):
        return self.rhs


class Identifier(Expression):
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def evaluateValue(self, s):
        print(CustomError('Method not implemented.'))

    def evaluateType(self, s):
        print(CustomError('Method not implemented.'))

    def getIdentifiers(self):
        print(CustomError('Method not implemented.'))


class FieldAssignment:
    def __init__(self, field, assignment):
        self.field = field
        self.assignment = assignment


class ComplexAssignStatement(Statement):
    def __init__(self, ass_id, values):
        self.id = ass_id
        self.values = values

    def get_id(self):
        return self.id

    def get_values(self):
        return self.values


class AssignStatement(Statement):
    def __init__(self, ass_id, value):
        self.id = ass_id
        self.value = value

    def get_id(self):
        return self.id

    def get_value(self):
        return self.value


class FieldAccessExpression(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs

    def getIdentifiers(self):
        return [self.lhs.get_value(), self.rhs.get_value()]

    def evaluateType(self, s):
        complexType = self.lhs.get_value()
        fieldType = self.rhs.get_value()
        return s.analyzer.find_complex_field_declaration(complexType, fieldType, s).get_type()

    def evaluateValue(self, s):
        complexId = self.lhs.get_value()
        fieldId = self.rhs.get_value()
        complexObject = s.interpreter.getVar(complexId, s).get_value()
        return complexObject[fieldId]

class FuncCallExpression(Expression):
    def __init__(self, id, params):
        self.id = id
        self.params = params

    def get_id(self):
        return self.lhs

    def get_params(self):
        return self.params

    def getIdentifiers(self):
        return [self.id]

    def evaluateType(self, s):
        funcDec = s.analyzer.find_function_declaration(self.id, s)
        funcParams = funcDec.get_params()
        callParams = self.get_params()

        if funcDec is not None:
            print(CustomError('SH19: Trying to call func {} but it\'s not declared'.format(self.id)))

        if len(funcParams) != len(callParams):
            print(CustomError('SH20: Func {} has {} params, called with {}'.format(self.id, len(funcParams), len(callParams))))

        for i in range(len(funcParams)):
            expectedType = funcParams[i].get_type()
            actualType = callParams[i].evaluateType(s)
            if expectedType != actualType:
                print(CustomError('SH21: Param at index {} expected to have type {} got {}'.format(i+1, expectedType, actualType)))
        return s.analyzer.find_function_declaration(self.id, s).get_return_type()

    def evaluateValue(self, s):
        funcDec = s.interpreter.getFunc(self.id, s)
        funcParams = funcDec.get_params()
        callParams = self.get_params()

        if funcDec.get_native_func() is not None:
            nativeFunc = funcDec.get_native_func()
            evaluatedParams = [p.evaluateValue(s) for p in callParams]
            result = nativeFunc(*evaluatedParams)
            return result

        paramDeclarations = [
            VarDeclaration(funcParams[callParams.index(p)].get_type(),
                           funcParams[callParams.index(p)].get_id(), p.evaluateValue(s)) for p in callParams]

        return s.interpreter.interpretFunc(funcDec, paramDeclarations, s)

class AccessFieldAssignment:
    def __init__(self, complexVar, field, assignment):
        self.complexVar = complexVar
        self.field = field
        self.assignment = assignment


class AccessAssignStatement(Statement):

    def __init__(self, complexVar, field, assignment):
        self.complexVar = complexVar
        self.field = field
        self.assignment = assignment

    def get_complex_id(self):
        return self.complexVar

    def get_field_id(self):
        return self.field

    def get_value(self):
        return self.assignment


class FuncCallStatement(Statement):
    def __init__(self, funcId, params):
        self.funcId = funcId
        self.params = params

    def get_funcId(self):
        return self.funcId

    def get_params(self):
        return self.params


class ReturnStatement(Statement):
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def evaluateType(self, s):
        if self.value is not None:
            return None
        return self.value.evaluateType(s)

    def evaluateValue(self, s):
        if self.value is not None:
            return 'net'
        return self.value.evaluateValue(s)


class ComplexField:
    def __init__(self, t, id):
        self.type = t
        self.id = id

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id



class Parser:
    st_list = [Tag.SEMI, Tag.IF, Tag.WHILE, Tag.LPAREN,
               Tag.LBRACE, Tag.IDENTIFIER, Tag.LET]

    types = [Tag.BOOLEAN, Tag.INTEGER, Tag.FLOAT, Tag.STRING, Tag.DIRECTION,
             Tag.RATE, Tag.TREND, Tag.TRADER, Tag.NAME, Tag.PAIR]

    def __init__(self, filename):
        self.init_levels()
        self.declarations = []
        self.identifiers = []
        self.assigns = []
        self.conditions = []
        self.curr_token = 0
        self.functions = []
        self.lexer = Lexer(filename)
        self.tokens = self.lexer.return_all_tokens()
        self.errors = 0

        self.token = self.tokens[self.curr_token]  # lexer.next_token()
        self.messageFormat = "Expected \"{}\", found \"{}\" instead"

    def init_levels(self):
        self.binopLevels = {};
        self.binopLevels[Tag.AND] = 10
        self.binopLevels[Tag.OR] = 10
        self.binopLevels[Tag.LT] = 20
        self.binopLevels[Tag.RT] = 20
        self.binopLevels[Tag.LT_EQ] = 20
        self.binopLevels[Tag.RT_EQ] = 20
        self.binopLevels[Tag.EQ] = 20
        self.binopLevels[Tag.PLUS] = 30
        self.binopLevels[Tag.MINUS] = 30
        self.binopLevels[Tag.TIMES] = 40
        self.binopLevels[Tag.DIV] = 40
        self.binopLevels[Tag.DOT] = 45
        self.binopLevels[Tag.LBRACE] = 50

    def raise_syntax_error(self, message=None):
        if message is not None:
            print("[Syntax Error] at {}:{} {}\n".format(self.token.line, self.token.column, message))

    def next_token(self):
        self.curr_token += 1
        if self.curr_token == len(self.tokens):
            return
        self.token = self.tokens[self.curr_token]

    def skip_to(self, tags):
        while self.token.tag != Tag.END_OF_FILE:
            if self.token.tag in tags:
                return
            self.next_token()

    def eat(self, tag):
        curr_tag = self.token.tag
        if curr_tag == tag:
            self.next_token()
            return True
        else:
            self.raise_syntax_error(self.messageFormat.format(str(tag), str(curr_tag)))
            return False

    def parse(self):
        self.statements = self.parse_statement_list()
        self.eat(Tag.END_OF_FILE)
        return self.statements

    def parse_type(self):

        t = self.tokens[self.curr_token]
        token_tag = t.tag
        if token_tag in self.types:
            self.eat(token_tag)
            return token_tag
        else:
            self.raise_syntax_error("Unknown type " + str(t.lexeme))
            # return None

    def parse_identifier(self):
        t = self.tokens[self.curr_token]
        identifier = ''
        if t.tag == Tag.IDENTIFIER:
            identifier = t.lexeme
        self.eat(Tag.IDENTIFIER)
        return identifier

    def is_statement(self):
        if self.token.tag in self.st_list:
            return True
        else:
            return False

    def parse_statement_list(self):

        statement_list = []
        while self.is_statement():
            statement_list.append(self.parse_statement())
        return statement_list

    def parse_block(self):
        self.eat(Tag.LBRACE)
        st = []
        while self.token.tag not in [Tag.RBRACE, Tag.END_OF_FILE]:
            st.append(self.parse_statement())
        if not self.eat(Tag.RBRACE):
            self.skip_to([Tag.RBRACE])
            self.eat(Tag.RBRACE)

        return BlockStatement(st)

    def parse_func_parameter(self):
        f_p_id = self.parse_identifier()
        f_p_type = self.parse_type()
        return FunctionParameter(f_p_type, f_p_id)

    def parse_func_parameters(self):
        self.eat(Tag.LPAREN)
        if self.token.tag == Tag.VOID:
            self.eat(Tag.VOID)
            self.eat(Tag.RPAREN)
            return []
        param = self.parse_func_parameter()
        params = [param]
        while self.token.tag == Tag.COMMA:
            self.eat(Tag.COMMA)
            params.append(self.parse_func_parameter)
        self.eat(Tag.RPAREN)
        return params

    def parse_complex_field(self):
        f_type = self.parse_type()
        f_id = self.parse_identifier()
        self.eat(Tag.SEMI)
        return ComplexField(f_type, f_id)

    def parse_complex_fields(self):
        self.eat(Tag.LBRACE)
        fields = []
        while (self.token.tag != Tag.RBRACE) and (self.token.tag != Tag.END_OF_FILE):
            fields.append(self.parse_complex_field())
        self.eat(Tag.RBRACE)
        return fields

    def parse_field_assignment(self):
        identifier = self.parse_identifier()
        self.eat(Tag.ASSIGN)
        val = self.parse_expression()
        self.eat(Tag.SEMI)
        return {
            'field': identifier,
            'assignment': val
        }

    def parse_statement(self):
        # if statement
        if self.token.tag == Tag.IF:
            self.eat(Tag.IF)

            # parse condition
            if not self.eat(Tag.LPAREN):
                self.skip_to([Tag.RPAREN, Tag.LBRACE, Tag.RBRACE])

            cond_exp = self.parse_expression()

            if not self.eat(Tag.RPAREN):
                self.skip_to([Tag.SEMI, Tag.LBRACE, Tag.RBRACE])

            # T/F stm
            if self.token.tag == Tag.LBRACE:
                true_stm = self.parse_block()
            else:
                true_stm = self.parse_statement()

            if self.token.tag == Tag.ELSE:
                if not self.eat(Tag.ELSE):
                    self.skip_to([Tag.SEMI, Tag.LBRACE, Tag.RBRACE])

                if self.token.tag == Tag.LBRACE:
                    false_stm = self.parse_block()
                else:
                    false_stm = self.parse_statement()

                return IfStatement(cond_exp, true_stm, false_stm)
            return IfStatement(cond_exp, true_stm, None)

        if self.token.tag == Tag.WHILE:
            self.eat(Tag.WHILE)

            if not self.eat(Tag.LPAREN):
                self.skip_to([Tag.RPAREN, Tag.LBRACE, Tag.RBRACE])

            cond_exp = self.parse_expression()

            if not self.eat(Tag.RPAREN):
                self.skip_to([Tag.SEMI, Tag.LBRACE, Tag.RBRACE])

            self.eat(Tag.LBRACE)
            loop_stm = self.parse_statement_list()
            self.eat(Tag.RBRACE)

            return WhileStatement(cond_exp, loop_stm)

        if self.token.tag == Tag.LET:
            self.eat(Tag.LET)
            var_type = self.parse_type()
            var_id = self.parse_identifier()
            self.eat(Tag.SEMI)
            return VarDeclaration(var_type, var_id)

        if self.token.tag == Tag.IDENTIFIER:
            id_val = Identifier(self.token.lexeme)
            self.identifiers.append(id_val)
            self.eat(Tag.IDENTIFIER)

            if self.token.tag == Tag.ASSIGN:
                self.eat(Tag.ASSIGN)
                if self.token.tag == Tag.LBRACE:
                    self.eat(Tag.LBRACE)
                    values = []
                    while ((self.token.tag != Tag.RBRACE) and (self.token.tag != Tag.END_OF_FILE)):
                        values.append(self.parse_field_assignment())
                    self.eat(Tag.RBRACE)
                    return ComplexAssignStatement(id_val, values)
                value = self.parse_expression()
                self.eat(Tag.SEMI)
                assign = AssignStatement(id_val, value)
                return assign

            if self.token.tag == Tag.DOT:
                self.eat(Tag.DOT)
                field = self.parse_identifier()
                self.eat(Tag.ASSIGN)
                value = self.parse_expression()
                self.eat(Tag.SEMI)

                return AccessAssignStatement(id_val.get_value(), field, value)
            if self.token.tag == Tag.LPAREN:
                params = self.parse_func_call_params()
                self.eat(Tag.SEMI)
                return FuncCallStatement(id_val, params)

            if self.token.tag == Tag.FUNC:
                self.eat(Tag.FUNC)
                f_type = self.parse_type()
                f_name = self.parse_identifier()
                params = self.parse_func_parameters()
                f_body = self.parse_block()

                function = Func(f_name, params, f_body, f_type)
                self.functions.append(function)
                return function
            if self.token.tag == Tag.RETURN:
                self.eat(Tag.RETURN)
                if self.token.tag == Tag.SEMI:
                    self.eat(Tag.SEMI)
                    return ReturnStatement(None)
                value = self.parse_expression()
                self.eat(Tag.SEMI)
                return ReturnStatement(value)

            self.eat(Tag.UNKNOWN)
            self.next_token()
            return None

    def parse_func_call_params(self):
        self.eat(Tag.LPAREN)
        if self.token.tag == Tag.RPAREN:
            self.eat(Tag.RPAREN)
            return []
        param = self.parse_expression()
        params = [param]
        while self.token.tag == Tag.COMMA:
            self.eat(Tag.COMMA)
            params.append(self.parse_expression())
        self.eat(Tag.RPAREN)
        return params

    def parse_expression(self):
        lhs = self.parse_primary_expression()
        return self.parse_binop_rhs(0, lhs)

    def return_boolean_value(self, str_val):
        if str_val == 'ugu':
            return True
        else:
            return False

    def parse_primary_expression(self):
        t = self.token
        if t.tag == Tag.INTEGER_LITERAL:
            int_val = int(t.lexeme)
            self.eat(Tag.INTEGER_LITERAL)
            return IntegerLiteral(int_val)
        if t.tag == Tag.FLOAT_LITERAL:
            f_val = float(t.lexeme)
            self.eat(Tag.FLOAT_LITERAL)
            return FloatLiteral(f_val)
        elif ((t.tag == Tag.BOOLEAN_LITERAL_TRUE) or (t.tag == Tag.BOOLEAN_LITERAL_FALSE)):
            boolean_val = self.return_boolean_value(self.token.lexeme)
            self.eat(t.tag)
            return BooleanLiteral(boolean_val)
        elif t.tag == Tag.CHARACTER_LITERAL:
            character_value = self.token.lexeme
            self.eat(Tag.CHARACTER_LITERAL)
            return CharacterLiteral(character_value)
        elif t.tag == Tag.STRING_LITERAL:
            string_value = self.token.lexeme
            self.eat(Tag.STRING_LITERAL)
            return StringLiteral(string_value)
        elif t.tag == Tag.IDENTIFIER:
            id_val = self.parse_identifier()
            self.identifiers.append(id_val)
            if self.token.tag == Tag.LPAREN:
                params = self.parse_func_call_params()
                return FuncCallExpression(id_val, params)
            return IdentifierExpression(id_val)
        elif t.tag == Tag.NOT:
            self.eat(Tag.NOT)
            return NotExpression(self.parse_expression())
        elif t.tag == Tag.MINUS:
            self.eat(Tag.MINUS)
            return NegativeExpression(self.parse_expression())
        elif t.tag == Tag.LPAREN:
            self.eat(Tag.LPAREN)
            exp = self.parse_expression()
            self.eat(Tag.RPAREN)
            return exp
        else:
            self.eat(Tag.UNKNOWN)
            self.next_token()
            return None

    def parse_binop_rhs(self, level, lhs):

        while True:
            if self.token.tag in self.binopLevels:
                token_level = self.binopLevels[self.token.tag]
            else:
                token_level = -1

            if token_level < level:
                return lhs

            binop = self.token.tag
            self.eat(binop)

            rhs = self.parse_primary_expression()

            if self.token.tag in self.binopLevels:
                next_level = self.binopLevels[self.token.tag]
            else:
                next_level = -1

            if token_level < next_level:
                rhs = self.parse_binop_rhs(token_level + 1, rhs)

            if binop == Tag.AND:
                lhs = AndExpression(lhs, rhs)
                return lhs
            elif binop == Tag.OR:
                lhs = OrExpression(lhs, rhs)
                return lhs
            elif binop == Tag.EQ:
                lhs = EqualExpression(lhs, rhs)
                return lhs
            elif binop == Tag.LT:
                lhs = LessThanExpression(lhs, rhs)
                return lhs
            elif binop == Tag.RT:
                lhs = GreaterThanExpression(lhs, rhs)
                return lhs
            elif binop == Tag.LT_EQ:
                lhs = LessThanEqualExpression(lhs, rhs)
                return lhs
            elif binop == Tag.RT_EQ:
                lhs = GreaterThanEqualExpression(lhs, rhs)
                return lhs
            elif binop == Tag.DOT:
                lhs = FieldAccessExpression(lhs, rhs)
                return lhs
            elif binop == Tag.PLUS:
                lhs = PlusExpression(lhs, rhs)
                return lhs
            elif binop == Tag.MINUS:
                lhs = MinusExpression(lhs, rhs)
                return lhs
            elif binop == Tag.TIMES:
                lhs = TimesExpression(lhs, rhs)
                return lhs
            elif binop == Tag.DIV:
                lhs = DivExpression(lhs, rhs)
                return lhs
            elif binop == Tag.MOD:
                lhs = ModExpression(lhs, rhs)
                return lhs
            else:
                self.eat(Tag.UNKNOWN)
                self.next_token()
                return None


# In[58]:


# lexer = Lexer('parser_test.txt')
#parser = Parser('parser_test.txt')

#for t in parser.tokens:
#    print(t)

# In[61]:


#res = parser.parse()

# In[41]:


#print(res[0].cond_exp)

# In[42]:


#print(res[0].loop_stm)

# In[ ]:


#



