############################################################
# Simple imperative language
# C-like surface syntac
# with S-expression syntax for expressions
# (no recursive closures)
#

import sys
#
# Expressions
#

class Exp (object):
    pass


class EValue (Exp):
    # Value literal (could presumably replace EInteger and EBoolean)
    def __init__ (self,v):
        self._value = v

    def __str__ (self):
        return "EValue({})".format(self._value)

    def eval (self,env):
        return self._value


class EPrimCall (Exp):
    # Call an underlying Python primitive, passing in Values
    #
    # simplifying the prim call
    # it takes an explicit function as first argument

    def __init__ (self,prim,es):
        self._prim = prim
        self._exps = es

    def __str__ (self):
        return "EPrimCall(<prim>,[{}])".format(",".join([ str(e) for e in self._exps]))

    def eval (self,env):
        vs = [ e.eval(env) for e in self._exps ]
        return apply(self._prim,vs)


class EIf (Exp):
    # Conditional expression

    def __init__ (self,e1,e2,e3):
        self._cond = e1
        self._then = e2
        self._else = e3

    def __str__ (self):
        return "EIf({},{},{})".format(self._cond,self._then,self._else)

    def eval (self,env):
        v = self._cond.eval(env)
        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval(env)
        else:
            return self._else.eval(env)


class ELet (Exp):
    # local binding
    # allow multiple bindings
    # eager (call-by-avlue)

    def __init__ (self,bindings,e2):
        self._bindings = bindings
        self._e2 = e2

    def __str__ (self):
        return "ELet([{}],{})".format(",".join([ "({},{})".format(id,str(exp)) for (id,exp) in self._bindings ]),self._e2)

    def eval (self,env):
        new_env = [ (id,e.eval(env)) for (id,e) in self._bindings] + env
        return self._e2.eval(new_env)

class EId (Exp):
    # identifier

    def __init__ (self,id):
        self._id = id

    def __str__ (self):
        return "EId({})".format(self._id)

    def eval (self,env):
        for (id,v) in env:
            if self._id == id:
                return v
        raise Exception("Runtime error: unknown identifier {}".format(self._id))


class ECall (Exp):
    # Call a defined function in the function dictionary

    def __init__ (self,fun,exps):
        self._fun = fun
        self._args = exps

    def __str__ (self):
        return "ECall({},[{}])".format(str(self._fun),",".join(str(e) for e in self._args))

    def eval (self,env):
        f = self._fun.eval(env)
        if f.type != "function":
            print "GOT: ", f
            raise Exception("Runtime error: trying to call a non-function")

        args = [ e.eval(env) for e in self._args]
        if len(args) != len(f.params):
            raise Exception("Runtime error: argument # mismatch in call")
        new_env = zip(f.params,args) + f.get_env(self._fun)
        return f.body.eval(new_env)


class EFunction (Exp):
    # Creates an anonymous function

    def __init__ (self,params,body):
        self._params = params
        self._body = body

    def __str__ (self):
        return "EFunction([{}],{})".format(",".join(self._params),str(self._body))

    def eval (self,env):
        return VClosure(self._params,self._body,env)


class ERefCell (Exp):
    # this could (should) be turned into a primitive
    # operation.  (WHY?)

    def __init__ (self,initialExp):
        self._initial = initialExp

    def __str__ (self):
        return "ERefCell({})".format(str(self._initial))

    def eval (self,env):
        v = self._initial.eval(env)
        return VRefCell(v)

class EDo (Exp):

    def __init__ (self,exps):
        self._exps = exps

    def __str__ (self):
        return "EDo([{}])".format(",".join(str(e) for e in self._exps))

    def eval (self,env):
        # default return value for do when no arguments
        v = VNone()
        for e in self._exps:
            v = e.eval(env)
        return v

class EWhile (Exp):

    def __init__ (self,cond,exp):
        self._cond = cond
        self._exp = exp

    def __str__ (self):
        return "EWhile({},{})".format(str(self._cond),str(self._exp))

    def eval (self,env):
        c = self._cond.eval(env)
        if c.type != "boolean":
            raise Exception ("Runtime error: while condition not a Boolean")
        while c.value:
            self._exp.eval(env)
            c = self._cond.eval(env)
            if c.type != "boolean":
                raise Exception ("Runtime error: while condition not a Boolean")
        return VNone()

class EArray (Exp):

    def __init__ (self, exps):
        self._exps = exps

    def __str__(self):
        return "EArray({})".format(str(self._e1))

    def eval (self, env):
        vals = [e.eval(env) for e in self._exps]
        return VArray(vals)

class EDictionary (Exp):

    def __init__(self, keys, values):
        self._keys= keys
        self._values = values

    def __str__(self):
        return "EDictionary({}, {})".format(str(self._keys), str(self._values))

    def eval (self, env):
        # keys_evaled = [k.eval(env) for k in self._keys]
        keys_evaled = self._keys
        values_evaled = [v.eval(env) for v in self._values]
        return VDictionary(keys_evaled, values_evaled)

class EWith (Exp):

    def __init__ (self, obj1, e1):
        self._obj1 = obj1
        self._e1 = e1

    def __str__(self):
        return "EWith({},{})".format((str(self._obj1), str(self._e1)))

    def eval(self, env):
        obj = self._obj1.eval(env)
        methods = obj.content.methods

        for m in methods:
            env.insert(0, m)

        v1 = self._e1.eval(env)
        return v1

#
# Values
#

class Value (object):
    pass


class VString (Value):
    def __init__(self, s):
        self.value = s
        self.type = "string"

    def __str__(self):
        return self.value

class VInteger (Value):
    # Value representation of integers

    def __init__ (self,i):
        self.value = i
        self.type = "integer"

    def __str__ (self):
        return str(self.value)


class VBoolean (Value):
    # Value representation of Booleans

    def __init__ (self,b):
        self.value = b
        self.type = "boolean"

    def __str__ (self):
        return "true" if self.value else "false"

class VArray (Value):
    #Array of stuff

    def __init__(self, in_vals):
        self.values = in_vals
        self.length = len(self.values)
        self.type = "array"
        self.methods = [
                ("index",
                VRefCell(VClosure(["x"],
                       EPrimCall(self.oper_index,[EId("x")]),
                       [self]))),
                ("length",
                VRefCell(VClosure([],
                      EPrimCall(self.oper_length,[]),
                      [self]))),
                ("map",
                VRefCell(VClosure(["x"],
                     EPrimCall(self.oper_map,[EId("x")]),
                     [self])))]

    def __str__(self):
        return "[" + ", ".join([str(j) for j in self.values]) + "]"

    def oper_index(self, v1):
        if v1.type == "integer":
            return self.values[v1.value]
        raise Exception ("Runtime error: incompatible types in index")

    def oper_length(self):
        return VInteger(self.length)

    def oper_map(self, f1):
        for i, v in enumerate(self.values):
            new_env = zip(f1.params,[v]) + f1.env
            self.values[i] = f1.body.eval(new_env)
        return self

class VDictionary (Value):
    #Array of stuff

    def __init__(self, keys, values):
        self.values = dict(zip(keys, values))
        self.type = "dictionary"

    def __str__(self):
        return "{" + ", ".join([str(k) for k in self.values]) + "}"


class VClosure (Value):

    def __init__ (self,params,body,env):
        self.params = params
        self.body = body
        self.env = env
        self.type = "function"

    def __str__ (self):
        return "<function [{}] {}>".format(",".join(self.params),str(self.body))

    def get_env(self, name):
        if type(name) is EId:
            if True not in [name._id == x for (x, y) in self.env]:
                cur_closure = VClosure(self.params, self.body, self.env)
                self.env.append((name._id, cur_closure))

        return self.env


class VRefCell (Value):

    def __init__ (self,initial):
        self.content = initial
        self.type = "ref"

    def __str__ (self):
        return "<ref {}>".format(str(self.content))


class VNone (Value):

    def __init__ (self):
        self.type = "none"

    def __str__ (self):
        return "none"


# Primitive operations




def oper_plus (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value + v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")

def oper_minus (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value - v2.value)
    raise Exception ("Runtime error: trying to subtract non-numbers")

def oper_times (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value * v2.value)
    raise Exception ("Runtime error: trying to multiply non-numbers")

def oper_greater_than (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VBoolean(v1.value > v2.value)
    raise Exception ("Runtime error: trying to greater than non-numbers")

def oper_greater_eq_than (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VBoolean(v1.value >= v2.value)
    raise Exception ("Runtime error: trying to greater equal than non-numbers")

def oper_less_than (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VBoolean(v1.value < v2.value)
    raise Exception ("Runtime error: trying to less than non-numbers")

def oper_less_eq_than (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VBoolean(v1.value <= v2.value)
    raise Exception ("Runtime error: trying to less equal than non-numbers")

def oper_equals (v1,v2):
    accepted_types = ["integer", "boolean", "string", "array"]
    if v1.type in accepted_types and v2.type in accepted_types:
        if v1.type == "array":
            for (i, e) in enumerate(v1.value):
                if e.value != v2.value[i].value:
                    return VBoolean(False)
            return VBoolean(True)
        else:
            return VBoolean(v1.value == v2.value)
    raise Exception ("Runtime error: trying to compute equality of non-values")

def oper_not_equals (v1,v2):
    eq = oper_equals(v1, v2)
    return VBoolean(not(eq.value))

def oper_zero (v1):
    if v1.type == "integer":
        return VBoolean(v1.value==0)
    raise Exception ("Runtime error: type error in zero?")

def oper_not (v1):
    if v1.type == "boolean":
        return VBoolean(not v1.value)
    raise Exception ("Runtime error: type error in zero?")

def oper_length (s1):
    if s1.type == "string":
        return VInteger(len(s1.value))
    raise Exception ("Runtime error: type error in oper_length")

def oper_substring(s1, v1, v2):
    if s1.type == "string" and v1.type == "integer" and v2.type == "integer":
        return VString(s1.value[v1.value:v2.value])
    raise Exception ("Runtime error: type error in oper_substring")

def oper_concat (s1, s2):
    if s1.type == "string" and s2.type == "string":
        return VString(s1.value + s2.value)
    raise Exception ("Runtime error: type error in oper_concat")

def oper_startswith (s1, s2):
    if s1.type == "string" and s2.type == "string":
        return VBoolean(s1.value.startswith(s2.value))
    raise Exception ("Runtime error: type error in oper_startswith")

def oper_endswith (s1, s2):
    if s1.type == "string" and s2.type == "string":
        return VBoolean(s1.value.endswith(s2.value))
    raise Exception ("Runtime error: type error in oper_endswith")

def oper_lower (s1):
    if s1.type == "string":
        return VString(s1.value.lower())
    raise Exception ("Runtime error: type error in oper_lower")

def oper_upper (s1):
    if s1.type == "string":
        return VString(s1.value.upper())
    raise Exception ("Runtime error: type error in oper_upper")

def oper_deref (v1):
    if v1.type == "ref":
        return v1.content
    raise Exception ("Runtime error: dereferencing a non-reference value")

def oper_update (v1,v2):
    if v1.type == "ref":
        v1.content = v2
        return VNone()
    raise Exception ("Runtime error: updating a non-reference value")

def oper_update_arr (v1,v2,v3):
    if v1.type == "ref":
        v1.content.values[v2.value] = v3
        return VNone()
    raise Exception ("Runtime error: updating a non-reference value")

def oper_swap_arr (v1, v2, v3):
    if v1.type == "array":
        tempContent1 = v1.values[v2.value]
        tempContent2 = v1.values[v3.value]
        v1.values[v2.value] = tempContent2
        v1.values[v3.value] = tempContent1
        return v1
    raise Exception ("Runtime error: updating a non-array value")

def oper_print (v1):
    print v1
    return VNone()

def oper_nothing (v1):
    return VNone()



############################################################
# IMPERATIVE SURFACE SYNTAX
#



##
## PARSER
##
# cf http://pyparsing.wikispaces.com/

from pyparsing import Word, Literal, ZeroOrMore, OneOrMore, Keyword, Forward, alphas, alphanums, NoMatch, Combine, Optional


def initial_env_imp ():
    # A sneaky way to allow functions to refer to functions that are not
    # yet defined at top level, or recursive functions
    env = []
    env.insert(0,
               ("+",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_plus,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("-",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_minus,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("*",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_times,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("zero?",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_zero,[EId("x")]),
                                  env))))
    env.insert(0,
               (">",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_greater_than,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               (">=",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_greater_eq_than,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("<",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_less_than,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("<=",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_less_eq_than,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("==",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_equals,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("<>",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_not_equals,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("not",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_not,[EId("x")]),
                                  env))))
    env.insert(0,
               ("length",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_length,[EId("x")]),
                                  env))))
    env.insert(0,
               ("substring",
                VRefCell(VClosure(["x","y","z"],
                                  EPrimCall(oper_substring,[EId("x"),EId("y"),EId("z")]),
                                  env))))
    env.insert(0,
               ("concat",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_concat,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("startswith?",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_startswith,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("endswith?",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_endswith,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("lower",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_lower,[EId("x")]),
                                  env))))
    env.insert(0,
               ("upper",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_upper,[EId("x")]),
                                  env))))
    env.insert(0,
               ("swap",
                VRefCell(VClosure(["x","y","z"],
                                  EPrimCall(oper_swap_arr,[EId("x"),EId("y"),EId("z")]),
                                  env))))

    return env


def createFor(result):
    res = ELet([(result[1][0], ERefCell(result[1][1]))], EDo([EWhile(EPrimCall(oper_not,[result[2]]), EDo([result[6], EPrimCall(oper_update, (EId(result[1][0]), result[4]))]))]))
    return res

def createProcedure(result):
    procedure_name = result[1]

    params = []
    i = 3
    while result[i] != ")":
        if result[i] != ",":
            params.append(result[i])
        i += 1
    stmt = result[i+1]
    bindings = [ (p,ERefCell(EId(p))) for p in params ]

    return (procedure_name, EFunction(params, ELet(bindings,stmt)))

def callProcedure(result):
    procedure_name = result[0]

    params = []
    i = 2
    while result[i] != ")":
        if result[i] != ",":
            params.append(result[i])
        i += 1

    return ECall(EPrimCall(oper_deref,[EId(procedure_name)]), params)

def parsePLet (input):
    print "INPUT: ", input
    bindings = input[3]
    names = []
    expressions = []
    for binding in bindings:
        names.append(binding[0])
        expressions.append(binding[1])
    function = input[5]
    print "OUT: ", ECall(EFunction(names, function), [expressions])
    return ECall(EFunction(names, function), [expressions])

def parse_imp (input):
    # parse a string into an element of the abstract representation

    # Grammar:
    #
    # <expr> ::= <integer>
    #            true
    #            false
    #            <identifier>
    #            ( if <expr> <expr> <expr> )
    #            ( function ( <name ... ) <expr> )
    #            ( <expr> <expr> ... )
    #
    # <decl> ::= var name = expr ;
    #
    # <stmt> ::= if <expr> <stmt> else <stmt>
    #            while <expr> <stmt>
    #            name <- <expr> ;
    #            print <expr> ;
    #            <block>
    #
    # <block> ::= { <decl> ... <stmt> ... }
    #
    # <toplevel> ::= <decl>
    #                <stmt>
    #


    idChars = alphas+"_+*-?!=<>"
    oper_chars = "+*-=<>"

    pIDENTIFIER = Word(idChars, idChars+"0123456789")
    #### NOTE THE DIFFERENCE
    pIDENTIFIER.setParseAction(lambda result: EPrimCall(oper_deref,[EId(result[0])]))

    # A name is like an identifier but it does not return an EId...
    pNAME = Word(idChars,idChars+"0123456789")
    pOPER = Word(oper_chars)

    pNAMES = ZeroOrMore(pNAME)
    pNAMES.setParseAction(lambda result: [result])

    pINTEGER = Optional("-") + Word("0123456789")
    pINTEGER.setParseAction(lambda result: EValue(VInteger(int("".join(result)))))

    pBOOLEAN = Keyword("true") | Keyword("false")
    pBOOLEAN.setParseAction(lambda result: EValue(VBoolean(result[0]=="true")))

    ESC_QUOTE = Literal("#\"")
    pSTRING = "\"" + ZeroOrMore(Combine(Word(idChars+"0123456789'") | ESC_QUOTE)) + "\""
    pSTRING.setParseAction(lambda result: EValue(VString(" ".join(result[1:-1]).replace("#\"", "\""))))

    pEXPR = Forward()
    pSTMT = Forward()
    pBODY = Forward()

    pEXPRS = ZeroOrMore(pEXPR)
    pEXPRS.setParseAction(lambda result: [result])

    pIF = "(" + Keyword("if") + pEXPR + pEXPR + pEXPR + ")"
    pIF.setParseAction(lambda result: EIf(result[2],result[3],result[4]))

    pARRAY = "[" + Optional(pEXPR + OneOrMore("," + pEXPR)) + "]"
    pARRAY.setParseAction(lambda result: EArray(result[1:-1][::2]))

    pDICT_ELEM = pNAME + ":" + pEXPR
    pDICT = "{" + Optional(pDICT_ELEM + OneOrMore("," + pDICT_ELEM)) + "}"
    pDICT.setParseAction(lambda result: EDictionary(result[1:-1][::4], result[3:-1][::4]))

    def mkFunBody (params,body):
        bindings = [ (p,ERefCell(EId(p))) for p in params ]
        return ELet(bindings,body)

    def printRes(result):
        print "GOT: ", [r.__str__() for r in result]
        return EFunction(result[3],mkFunBody(result[3],result[5]))

    pFUN = Keyword("fun") + "(" + pNAMES + ")" + pSTMT + ";"
    pFUN.setParseAction(lambda result: printRes(result))

    pWITH = "(" + Keyword("with") + pNAME + pEXPR + ")"
    pWITH.setParseAction(lambda result: EWith(EId(result[2]), result[3]))

    pCALL = "(" + pEXPR + pEXPRS + ")"
    pCALL.setParseAction(lambda result: ECall(result[1],result[2]))

    pEXPR_FIRST = (pINTEGER | pBOOLEAN | pSTRING | pFUN | pIDENTIFIER | pARRAY | pDICT | pIF | pWITH | pCALL)
    pEXPR_REST = pOPER + pEXPR

    pALGEBRA = pEXPR_FIRST + pEXPR_REST
    pALGEBRA.setParseAction(lambda result: ECall(EPrimCall(oper_deref,[EId(result[1])]), [result[0], result[2]]))

    pEXPR << (pALGEBRA | pEXPR_FIRST )

    pSTMT_IF_1 = "if" + pEXPR + pSTMT + "else" + pSTMT + ";"
    pSTMT_IF_1.setParseAction(lambda result: EIf(result[1],result[2],result[4]))

    pSTMT_IF_2 = "if" + pEXPR + pSTMT + ";"
    pSTMT_IF_2.setParseAction(lambda result: EIf(result[1],result[2],EValue(VBoolean(True))))

    pSTMT_WHILE = "while" + pEXPR + pSTMT + ";"
    pSTMT_WHILE.setParseAction(lambda result: EWhile(result[1],result[2]))

    pFOR_VAR = "var" + pNAME + "=" + pEXPR + ";"
    pFOR_VAR.setParseAction(lambda result: (result[1],result[3]))

    pSTMT_FOR = "for" + pFOR_VAR + pCALL + ";" + pCALL + ";" + pSTMT
    pSTMT_FOR.setParseAction(lambda result: createFor(result))

    pSTMT_PRINT = "print" + pEXPR + ";"
    pSTMT_PRINT.setParseAction(lambda result: EPrimCall(oper_print,[result[1]]));

    pSTMT_UPDATE = pNAME + "<-" + pEXPR + ";"
    pSTMT_UPDATE.setParseAction(lambda result: EPrimCall(oper_update,[EId(result[0]),result[2]]))

    pSTMT_ARR_UPDATE = pNAME + "[" + pEXPR + "]" + "<-" + pEXPR + ";"
    pSTMT_ARR_UPDATE.setParseAction(lambda result: EPrimCall(oper_update_arr, [EId(result[0]), result[2], result[5]]))

    pSTMT_PROCEDURE = pNAME + "(" + pEXPR + ZeroOrMore("," + pEXPR) + ")" + ";"
    pSTMT_PROCEDURE.setParseAction(lambda result: callProcedure(result))

    pSTMTS = ZeroOrMore(pSTMT)
    pSTMTS.setParseAction(lambda result: [result])

    pDECL_VAR = "var" + pNAME + "=" + pEXPR + ";"
    pDECL_VAR.setParseAction(lambda result: (result[1],result[3]))

    pDECL_PROCEDURE = "procedure" + pNAME + "(" + pNAME + ZeroOrMore("," + pNAME) + ")" + pSTMT + ";"
    pDECL_PROCEDURE.setParseAction(lambda result: createProcedure(result))

    # hack to get pDECL to match only PDECL_VAR (but still leave room
    # to add to pDECL later)
    pDECL = ( pDECL_VAR | pDECL_PROCEDURE | NoMatch() )

    pDECLS = ZeroOrMore(pDECL)
    pDECLS.setParseAction(lambda result: [result])

    def mkBlock (decls,stmts):
        bindings = [ (n,ERefCell(expr)) for (n,expr) in decls ]
        return ELet(bindings,EDo(stmts))

    pSTMT_BLOCK = "{" + pDECLS + pSTMTS + "}"
    pSTMT_BLOCK.setParseAction(lambda result: mkBlock(result[1],result[2]))

    pBODY << pSTMT_BLOCK

    pSTMT << ( pSTMT_IF_1 | pSTMT_IF_2 | pSTMT_WHILE | pSTMT_FOR | pSTMT_PRINT | pSTMT_UPDATE | pSTMT_ARR_UPDATE | pSTMT_PROCEDURE | pSTMT_BLOCK )

    # can't attach a parse action to pSTMT because of recursion, so let's duplicate the parser
    pTOP_STMT = pSTMT.copy()
    pTOP_STMT.setParseAction(lambda result: {"result":"statement",
                                             "stmt":result[0]})

    pTOP_DECL = pDECL.copy()
    pTOP_DECL.setParseAction(lambda result: {"result":"declaration",
                                             "decl":result[0]})

    pABSTRACT = "#abs" + pSTMT
    pABSTRACT.setParseAction(lambda result: {"result":"abstract",
                                             "stmt":result[1]})

    pQUIT = Keyword("#quit")
    pQUIT.setParseAction(lambda result: {"result":"quit"})

    pTOP = (pQUIT | pABSTRACT | pTOP_DECL | pTOP_STMT )

    result = pTOP.parseString(input)[0]
    return result    # the first element of the result is the expression


def shell_imp ():
    # A simple shell
    # Repeatedly read a line of input, parse it, and evaluate the result

    print "Homework 6 - Imp Language"
    print "#quit to quit, #abs to see abstract representation"
    env = initial_env_imp()


    while True:
        inp = raw_input("imp> ")

        try:
            result = parse_imp(inp)

            if result["result"] == "statement":
                stmt = result["stmt"]
                # print "Abstract representation:", exp
                v = stmt.eval(env)

            elif result["result"] == "abstract":
                print result["stmt"]

            elif result["result"] == "quit":
                return

            elif result["result"] == "declaration":
                (name,expr) = result["decl"]
                v = expr.eval(env)
                env.insert(0,(name,VRefCell(v)))
                print "{} defined".format(name)


        except Exception as e:
            print "Exception: {}".format(e)

shell_imp()
