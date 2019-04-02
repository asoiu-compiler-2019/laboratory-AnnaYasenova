from errors import SemanticError
from parser import *

reserved = [
    Tag.NOT,
    Tag.BOOLEAN_LITERAL_TRUE,
    Tag.BOOLEAN_LITERAL_FALSE,
    Tag.MAIN,
    Tag.VOID,
    Tag.FUNCTION,
    Tag.BOOLEAN,
    Tag.INTEGER,
    Tag.FLOAT,
    Tag.STRING,
    Tag.DIRECTION,
    Tag.RATE,
    Tag.TREND,
    Tag.TRADER,
    Tag.NAME,
    Tag.PAIR,
    Tag.LET,
    Tag.IF,
    Tag.ELSE,
    Tag.WHILE,
    Tag.RETURN
]

def isIdentifierReserved(character):
    return character in reserved


class Scope:
    def __init__(self, declarations=None, parentContext=None, retType=None, analyzer=None):
        self.declarations = declarations
        self.parentContext = parentContext
        self.retType = retType
        self.analyzer = analyzer


class SemanticAnalyzer:
    def __init__(self, filename):
        self.statements = []
        self.complexTypeDeclarations = []
        self.functionDeclarations = []
        self.declarations = []
        self.parser = Parser(filename)

    def raise_error(self, message):
        print(SemanticError(message))

    def analyze(self, s, scope):

        if isinstance(s, Func):
            self.check_Function(s, scope)
        if isinstance(s, ReturnStatement):
            self.check_return(s, scope)
        if isinstance(s, VarDeclaration):
            self.check_variable_declaration(s, scope)
        if isinstance(s, IfStatement):
            self.check_if(s, scope)
        if isinstance(s, WhileStatement):
            self.check_while(s, scope)
        if isinstance(s, AssignStatement):
            self.check_assign(s, scope)
        if isinstance(s, ComplexAssignStatement):
            self.check_complex_assign(s, scope)
        if isinstance(s, AccessAssignStatement):
            self.check_acess_assign(s, scope)
        if isinstance(s, FuncCallStatement):
            self.check_func_call(s, scope)
        if isinstance(s, ComplexAssignStatement):
            self.check_complex_assign(s, scope)

    def get_ast(self):
        return self.statements

    def analyze_file(self):
        self.statements = self.parser.parse()
        #self.complexTypeDeclarations = exportComplexTypeDeclarations()
        #self.functionDeclarations = exportFuncDeclarations()
        self.declarations = []
        for s in self.statements:
            self.analyze(s, None)


    def find_function_declaration(self, id, s):
        func = None
        for f in self.functionDeclarations:
            if f.get_id() == id:
                func = f

        if func is None:
            self.raise_error('SH??: Function with id {} not declared'.format(id))
        return func

    def find_variable_declaration(self, id, s):
        curr_scope = s
        var_dec = None
        while curr_scope is not None:
            for v in curr_scope.declarations:
                if v.var_id == id:
                    var_dec = v
            if var_dec is not None:
                return var_dec
            curr_scope = curr_scope.parentContext
        for v in self.declarations:
            if v.var_id == id:
                var_dec = v
        return var_dec

    def find_complex_field_declaration(self, complexTypeId, fieldId, s):

        complex = self.find_variable_declaration(complexTypeId, s)
        if not complex:
            self.raise_error('SH??: Complex type variable with id {} not found'.format(complexTypeId))

        complexType = None
        for t in self.complex_type_declarations:
            if t.get_id() == complex.get_type():
                complexType = t
        if complexType is None:
            self.raise_error('SH??: Complex type variable with id {} not declared'.format(complex.getType()))

        field = None
        for f in complexType.get_fields():
            if f.get_id() == fieldId:
                field = f
        if field is None:
            self.raise_error('SH??: Complex type {} has no field {}'.format(complexTypeId, fieldId))

        return field

    def check_complex_type_fields(self, complexID, fields):
        identifiers = []
        for s in fields:
            fieldType = s.get_type()
            id = s.get_id()
            isReserved = not isIdentifierReserved(fieldType)

            found = False
            for ct in self.complexTypeDeclarations:
                if ct.get_id() == fieldType:
                    found = True
            if isReserved and (not found):
                self.raise_error('SH05: Field with id {} already declared for {}'.format(id, complexID))

            identifiers.append(id)

    def check_complex_type(self, c, scope):

        id = c.get_id()
        fields = c.get_fields()

        found = False
        for ct in self.complexTypeDeclarations:
            if ct.get_id() == id:
                found = True

        if found:
            self.raise_error('SH01: Complex type {} already declared'.format(id))

        if isIdentifierReserved(id):
            self.raise_error('SH02: Reserved indentifier {}'.format(id))

        if len(fields) == 0:
            self.raise_error('SH03: Empty complex type {} declaration'.format(id))

        self.check_complex_type_fields(id, fields)
        self.complexTypeDeclarations.append(c)

    def check_complex_assign(self, s, scope):
        if scope is None:
            scope = Scope(analyzer=self, declarations=self.declarations)

        id = s.get_id().get_value()
        fieldAssignments = s.get_values()
        for a in fieldAssignments:
            fieldDec = self.find_complex_field_declaration(id, a.field, scope)
            assignType = a.assignment.evaluateType(scope)
            fieldType = fieldDec.get_type()
            if fieldType != assignType:
                self.raise_error('SH18: Trying to assign {} to {} field {} of {} var'.format(assignType, fieldType, a.field, id))

    def check_return(self, r, scope, funcType):
        retType = r.evaluateType(scope)

        if retType != funcType:
            self.raise_error('SH08: Type {} doesn\'t match with {}'.format(retType, funcType))


    def check_variable_declaration(self, dec, scope):
        id = dec.get_id()
        v_type = dec.get_type()
        if self.find_variable_declaration(id, scope):
            self.raise_error('SH10: Variable with id {} already declared'.format(id))

        isReserved = not isIdentifierReserved(v_type)

        found = False
        for ct in self.complexTypeDeclarations:
            if ct.get_id() == id:
                found = True

        if isReserved and (not found):
            self.raise_error('SH04: Unknown type {}'.format(v_type))

        if scope:
            scope.declarations.append(dec)
        else:
            self.declarations.append(dec)


    def check_if(self, st, sc):
        if sc is None:
            sc = Scope(analyzer=self, declarations=self.declarations)
        condType = st.get_cond_exp().evaluateType(sc)
        trueBody = st.get_true_stm_arr()
        if condType != Tag.BOOLEAN:
            self.raise_error('SH11: If statement\'s condition type is {} but boolean expected'.format(condType))

        trueScope = Scope(declarations=[], retType=sc.retType, analyzer=self, parentContext=sc)

        for s in trueBody:
            self.analyze(s, trueScope)

        if st.has_false_stm():
            falseBody = st.get_false_stm_arr()
            falseScope = Scope(declarations=[], retType=sc.retType, analyzer=self, parentContext=sc)

            for s in falseBody:
                self.analyze(s, falseScope)

    def check_assign(self, st, sc):
        if sc is None:
            sc = Scope(analyzer=self, declarations=self.declarations)
        varId = st.get_id().get_value()
        varDec = self.find_variable_declaration(varId, sc)

        if sc is not None:
            assignType = st.get_value().evaluateType(sc)
        else:
            assignType = st.get_value().evaluateType(Scope(analyzer=self))

        if varDec is None:
            self.raise_error('SH15: Trying to assign {} but it\'s not declared'.format(varId))

        if varDec.get_type() != assignType:
            self.raise_error('SH16: Trying to assign {} to {} variable'.format(assignType, varDec.get_type()))

    def check_access_assign(self, st, sc):
        varId = st.get_complex_id()
        varDec = self.find_variable_declaration(varId, sc)
        assignType = st.get_value().evaluateType(sc)
        fieldId = st.get_field_id()

        if varDec is None:
            self.raise_error('SH17: Trying to assign complex var {} but it\'s not declared'.format(varId))
        fieldType = self.findComplexFieldDeclaration(varId, fieldId, sc).getType()

        if fieldType != assignType:
            self.raise_error('SH18: Trying to assign {} to {} field {} of {} var'.format(assignType, fieldType, fieldId, varId))

    def check_func_call(self, st, sc):
        funcId = st.get_func_id().get_value()
        funcDec = self.find_function_declaration(funcId, sc)
        funcParams = funcDec.get_params()
        callParams = st.get_params()

        if sc is None:
            sc = Scope(analyzer=self, declarations=self.declarations)

        if funcDec is None:
            self.raise_error('SH19: Trying to call func {} but it\'s not declared'.format(funcId))

        if len(funcParams) != len(callParams):
            self.raise_error('SH20: Func {} has {} params, called with {}'.format(funcId, len(funcParams), len(callParams)))

        for i in range(len(funcParams)):
            expectedType = funcParams[i].get_type()
            actualType = callParams[i].evaluateType(sc)
            if expectedType != actualType:
                self.raise_error('SH21: Param at index {} expected to have type {}, got {}'.format(i + 1, expectedType, actualType))

    def check_while(self, st, sc):
        if sc is None:
            sc = Scope(analyzer=self, declarations=self.declarations)
        condType = st.get_cond_exp().evaluateType(sc)
        body = st.get_loop_stm()
        if condType != Tag.BOOLEAN:
            self.raise_error('SH12: While statement\'s condition type is {} but boolean expected'.format(condType))

        expressionIdentifiers = st.get_cond_exp().get_identifiers()
        atLeastOneIdUsed = False
        for s in st.get_loop_stm():
            if isinstance(s, AssignStatement):
                for e in expressionIdentifiers:
                    if e == s.get_id().get_value():
                        atLeastOneIdUsed = True
        if not atLeastOneIdUsed:
            self.raise_error('SH13: Possible endless while loop')

        bodyScope = Scope(declarations=[], retType=sc.retType, analyzer=self, parentContext=sc)

        for s in body:
            self.analyze(s, bodyScope)


    def check_function_parameters(self, funcID, params):
        identifiers = []
        for s in params:
            paramType = s.get_type()
            id = s.get_id()
            isReserved = not isIdentifierReserved(paramType)
            flagType = False
            for ct in self.complexTypeDeclarations:
                if ct.get_id() == paramType:
                    flagType = True
            if isReserved and (not flagType):
                self.raise_error('SH04: Unknown type {}'.format(paramType))

            try:
                ind = identifiers.index(id)
            except ValueError:
                self.raise_error('SH09: Param with id {} already declared for {}'.format(id, funcID))
            identifiers.append(id)

    def check_function(self, f, sc):
        id = f.get_id()
        params = f.get_params()
        body = f.get_body().get_statements_list()
        retType = f.get_return_type()

        flagType = False
        for ct in self.functionDeclarations:
            if ct.get_id() == id:
                flagType = True

        if flagType:
            self.raise_error('SH06: Function {} already declared'.format(id))

        if isIdentifierReserved(id):
            self.raise_error('SH02: Reserved indentifier {}'.format(id))

        if retType is not None:
            isReserved = not isIdentifierReserved(retType)
            flagType = False
            for ct in self.complexTypeDeclarations:
                if ct.get_id() == retType:
                    flagType = True
            if isReserved and (not flagType):
                self.raise_error('SH04: Unknown type {}'.format(retType))

        self.check_function_parameters(id, params)
        bodyScope = Scope(declarations=params, retType=sc.retType, analyzer=self, parentContext=None)
        for s in body:
            self.analyze(s, bodyScope)

        self.functionDeclarations.append(f)