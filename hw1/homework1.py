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
        elif v1.type == "vector" or v2.type == "vector":
            v1_vec = v1.type == "vector"
            v2_vec = v2.type == "vector"
            if v1_vec and v2_vec and v1.length != v2.length:
                raise Exception("Runtime error: vectors of unequal length")
            to_return = []
            length = v1.length if v1_vec else v2.length
            for i in range(length):
                first = v1.get(i) if v1_vec else v1
                second = v2.get(i) if v2_vec else v2
                if first.type == "integer" and second.type == "integer":
                    to_return.append(VInteger(first.value + second.value))
                else:
                    raise Exception ("Runtime error: vectors of incompatable types - not integers")

            return VVector(to_return)
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
        elif v1.type == "vector" or v2.type == "vector":
            v1_vec = v1.type == "vector"
            v2_vec = v2.type == "vector"
            if v1_vec and v2_vec and v1.length != v2.length:
                raise Exception("Runtime error: vectors of unequal length")
            to_return = []
            length = v1.length if v1_vec else v2.length
            for i in range(length):
                first = v1.get(i) if v1_vec else v1
                second = v2.get(i) if v2_vec else v2
                if first.type == "integer" and second.type == "integer":
                    to_return.append(VInteger(first.value - second.value))
                else:
                    raise Exception ("Runtime error: vectors of incompatable types - not integers")

            return VVector(to_return)
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
        elif v1.type == "vector" or v2.type == "vector":
            v1_vec = v1.type == "vector"
            v2_vec = v2.type == "vector"
            if v1_vec and v2_vec and v1.length != v2.length:
                raise Exception("Runtime error: vectors of unequal length")
            to_return = []
            length = v1.length if v1_vec else v2.length
            v_sum = 0
            for i in range(length):
                first = v1.get(i) if v1_vec else v1
                second = v2.get(i) if v2_vec else v2
                if first.type == "integer" and second.type == "integer":
                    product = first.value * second.value
                    to_return.append(VInteger(product))
                    v_sum += product
                else:
                    raise Exception ("Runtime error: vectors of incompatable types - not integers")

            return VVector(to_return) if v1_vec != v2_vec else VInteger(v_sum)
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

        if _v1.type == "vector" and _v2.type == "vector":
            if _v1.length != _v2.length:
                raise Exception ("Runtime error: lists not equal length")
            else:
                resList = []
                i = 0
                while i < _v1.length:
                    resList.append(EAnd(EBoolean(_v1.get(i).value), EBoolean(_v2.get(i).value)))
                    i += 1

                return EVector(resList).eval()

        else:
            if _v1.type == "boolean":
                if _v2.type == "boolean":
                    return VBoolean(_v1.value and _v2.value)
                elif _v2.type == "vector":
                    singleBool = _v1
                    vectorBools = _v2
                else:
                    return VBoolean(_v1.value)

            elif _v1.type == "vector" and _v2.type == "boolean":
                singleBool = _v2
                vectorBools = _v1

            else:
                raise Exception ("Runtime error: expressions are not a Booleans")

            resList = []
            i = 0
            while i < vectorBools.length:
                resList.append(EAnd(EBoolean(vectorBools.get(i).value), EBoolean(singleBool.value)))
                i += 1
            return EVector(resList).eval()


class EOr(Exp):
    #Does OR operation on two inputs

    def __init__(self, e1, e2):
        self._e1 = e1
        self._e2 = e2

    def __str__(self):
        return "EOr({},{})".format(self._e1, self._e2)

    def eval(self):
        _v1 = self._e1.eval()
        _v2 = self._e2.eval()


        if _v1.type == "vector" and _v2.type == "vector":
            if _v1.length != _v2.length:
                raise Exception ("Runtime error: lists not equal length")
            else:
                resList = []
                i = 0
                while i < _v1.length:
                    resList.append(EOr(EBoolean(_v1.get(i).value), EBoolean(_v2.get(i).value)))
                    i += 1

                return EVector(resList).eval()

        else:
            if _v1.type == "boolean":
                if _v2.type == "boolean":
                    return VBoolean(_v1.value or _v2.value)
                elif _v2.type == "vector":
                    singleBool = _v1
                    vectorBools = _v2
                else:
                    return VBoolean(_v1.value)

            elif _v1.type == "vector" and _v2.type == "boolean":
                singleBool = _v2
                vectorBools = _v1

            else:
                raise Exception ("Runtime error: expressions are not a Booleans")

            resList = []
            i = 0
            while i < vectorBools.length:
                resList.append(EOr(EBoolean(vectorBools.get(i).value), EBoolean(singleBool.value)))
                i += 1
            return EVector(resList).eval()


class ENot(Exp):
    # Does not operation on one input

    def __init__(self, e1):
        self._exp = e1

    def __str__(self):
        return "ENot({})".format(self._exp)

    def eval(self):
        _v1 = self._exp.eval()

        if _v1.type == "vector":
            resList = []
            valLength = _v1.length
            i = 0
            while i < valLength:
                _v2 = _v1.get(i)
                if _v2.type == "boolean":
                    resList.append(ENot(EBoolean(_v2.value)))
                else:
                    raise Exception("Runtime error: expression is not a Boolean")
                i += 1
            return EVector(resList).eval()

        if _v1.type == "boolean":
            return VBoolean(not _v1.value)
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

def pair(v):
    return (v.get(0).value, v.get(1).value)

def rat (v):
    return "{}/{}".format(v.numer,v.denom)
