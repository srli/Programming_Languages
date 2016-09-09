############################################################
# HOMEWORK 1
#
# Team members: Sophie and Lindsey
#
# Emails: lindsey.vanderlyn@students.olin.edu and sophie.li@students.olin.edu
#
# Remarks:
#




#
# Expressions
#

class Exp (object):
    pass


class EInteger (Exp):
    # Integer literal

    def __init__ (self,i):
        self._integer = i

    def __str__ (self):
        return "EInteger({})".format(self._integer)

    def eval (self):
        return VInteger(self._integer)


class EBoolean (Exp):
    # Boolean literal

    def __init__ (self,b):
        self._boolean = b

    def __str__ (self):
        return "EBoolean({})".format(self._boolean)

    def eval (self):
        return VBoolean(self._boolean)


class EPlus (Exp):
    # Addition operation

    def __init__ (self,e1,e2):
        self._exp1 = e1
        self._exp2 = e2

    def __str__ (self):
        return "EPlus({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()
        if v1.type == "integer" and v2.type == "integer":
            return VInteger(v1.value + v2.value)
        raise Exception ("Runtime error: trying to add non-numbers")


class EMinus (Exp):
    # Subtraction operation

    def __init__ (self,e1,e2):
        self._exp1 = e1
        self._exp2 = e2

    def __str__ (self):
        return "EMinus({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()
        if v1.type == "integer" and v2.type == "integer":
            return VInteger(v1.value - v2.value)
        raise Exception ("Runtime error: trying to subtract non-numbers")


class ETimes (Exp):
    # Multiplication operation

    def __init__ (self,e1,e2):
        self._exp1 = e1
        self._exp2 = e2

    def __str__ (self):
        return "ETimes({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()
        if v1.type == "integer" and v2.type == "integer":
            return VInteger(v1.value * v2.value)
        raise Exception ("Runtime error: trying to multiply non-numbers")


class EIf (Exp):
    # Conditional expression

    def __init__ (self,e1,e2,e3):
        self._cond = e1
        self._then = e2
        self._else = e3

    def __str__ (self):
        return "EIf({},{},{})".format(self._cond,self._then,self._else)

    def eval (self):
        v = self._cond.eval()
        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval()
        else:
            return self._else.eval()

#
# Values
#

class Value (object):
    pass


class VInteger (Value):
    # Value representation of integers
    def __init__ (self,i):
        self.value = i
        self.type = "integer"

class VBoolean (Value):
    # Value representation of Booleans
    def __init__ (self,b):
        self.value = b
        self.type = "boolean"


#HOMEWORK ANSWERS START HERE
# ------------- #

#Question 1
class EIsZero (Exp):
    # Checks if input is 0

    def __init__(self, e1):
        self._exp = e1

    def __str__(self):
        return "EIsZero({})".format(self._exp)

    def eval(self):
        v1 = self._exp.eval()
        if v1.value == 0:
            return VBoolean(True)
        else:
            return VBoolean(False)

class EAnd (Exp):
    # Does and operation on two inputs

    def __init__(self, e1, e2):
        self._exp1 = e1
        self._exp2 = e2

    def __str__(self):
        return "EAnd({}, {})".format(self._exp1, self._exp2)

    def eval(self):
        _v1 = self._exp1.eval()
        _v2 = self._exp2.eval()
        if _v1.type != "boolean":
            raise Exception ("Runtime error: expression 1 not a Boolean")
        elif not _v1.value:
            return VBoolean(False)

        if _v2.type != "boolean":
            raise Exception ("Runtime error: expression w not a Boolean")
        elif not _v2.value:
            return VBoolean(False)
        else:
            return VBoolean(True)

class EOr(Exp):
    def __init__(self, e1, e2):
        self._e1 = e1
        self._e2 = e2

    def __str__(self):
        return "EOr({},{})".format(self._e1, self._e2)

    def eval(self):
        _v1 = self._e1.eval()
        _v2 = self._e2.eval()
        if _v1.type != "boolean":
            raise Exception ("Runtime error: expression 1 not a Boolean")
        elif _v1.value:
            return VBoolean(True)

        if _v2.type != "boolean":
            raise Exception ("Runtime error: expression w not a Boolean")
        elif _v2.value:
            return VBoolean(True)
        else:
            return VBoolean(False)

class ENot(Exp):
    # Does not operation on one input

    def __init__(self, e1):
        self._exp = e1

    def __str__(self):
        return "ENot({})".format(self._exp)

    def eval(self):
        v1 = self._exp.eval()
        if v1.type == "boolean":
            return VBoolean(not v1.value)
        else:
            raise Exception ("Runtime error: condition not a Boolean")

#Question 2
class VVector (Value):
    # Value representation of vector

    def __init__ (self,i):
        self._rawData = i
        self.length = len(i)
        self.type = "vector"

    def get(self, n):
        if n > self.length:
            raise Exception ("Runtime error: N is greater than length of vector")
        else:
            return self._rawData[n]

class EVector (Exp):
    #Takes a list of expressions and evaluates to a vector of the resulting evaluations

    def __init__(self, vexp):
        self._vexp = vexp

    def __str__(self):
        return "EVector({})".format(self._vexp)

    def eval(self):
        expLen = len(self._vexp)
        valList = []
        i = 0
        while i < expLen:
            valList.append(self._vexp[i].eval())
            i += 1
        return VVector(valList)
