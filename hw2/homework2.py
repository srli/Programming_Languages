############################################################
# HOMEWORK 2
#
# Team members: Limdsey and Sophie
#
# Emails: lindsey.vanderlyn@students.olin.edu and sohpia.li@students.olin.edu
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

    def eval (self,prim_dict):
        return VInteger(self._integer)

    def substitute (self,ids,new_es):
        return self


class EBoolean (Exp):
    # Boolean literal

    def __init__ (self,b):
        self._boolean = b

    def __str__ (self):
        return "EBoolean({})".format(self._boolean)

    def eval (self,prim_dict):
        return VBoolean(self._boolean)

    def substitute (self,ids,new_es):
        return self


class EPrimCall (Exp):

    def __init__ (self,name,es):
        self._name = name
        self._exps = es

    def __str__ (self):
        return "EPrimCall({},[{}])".format(self._name,",".join([ str(e) for e in self._exps]))

    def eval (self,prim_dict):
        vs = [ e.eval(prim_dict) for e in self._exps ]
        return apply(prim_dict[self._name],vs)

    def substitute (self,ids,new_es):
        new_es = [ e.substitute(ids,new_es) for e in self._exps]
        return EPrimCall(self._name,new_es)


class EIf (Exp):
    # Conditional expression

    def __init__ (self,e1,e2,e3):
        self._cond = e1
        self._then = e2
        self._else = e3

    def __str__ (self):
        return "EIf({},{},{})".format(self._cond,self._then,self._else)

    def eval (self,prim_dict):
        v = self._cond.eval(prim_dict)
        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval(prim_dict)
        else:
            return self._else.eval(prim_dict)

    def substitute (self,ids,new_es):
        return EIf(self._cond.substitute(ids,new_es),
                   self._then.substitute(ids,new_es),
                   self._else.substitute(ids,new_es))


class ELet (Exp):
    # local binding

    def __init__ (self,assignments,e2):
        self._ids = [a[0] for a in assignments]
        self._e1s = [a[1] for a in assignments]
        self._e2 = e2

    def __str__ (self):
        return "ELet({},{},{})".format(self._ids,self._e1s,self._e2)

    def eval (self,prim_dict):
        new_e2 = self._e2.substitute(self._ids, self._e1s)
        return new_e2.eval(prim_dict)

    def substitute (self,ids, new_e1s):
        new_assignments = []
        new_e2 = self._e2
        e1s = self._e1s

        # goes through all of the assignments
        for j in range(len(self._ids)):
            # substitutes values from upper assignment as needed 
            for i in range(len(ids)):
                id = ids[i]
                new_e1 = new_e1s[i]
                e1s[j] = e1s[j].substitute(ids, new_e1s)
            # adds substituted values as assignments for the new ELet statement that will be returned
            new_assignments.append((self._ids[j], e1s[j]))
            if not id in self._ids:
                new_e2 = new_e2.substitute(ids,new_e1s)
        return ELet(new_assignments, new_e2)


class ELetS(Expr):
    """Sequential local binding"""

    def __init__(self, assignments, e2):
        self.ELet = 
        self._assignments = assignments

    def __str__ (self):
        return "ELets({},{},{})".format(self._ids,self._e1s,self._e2)

    def substitute(self, ids, new_e1s):
        to_sub = 


class EId (Exp):
    # identifier

    def __init__ (self,id):
        self._id = id

    def __str__ (self):
        return "EId({})".format(self._id)

    def eval (self,prim_dict):
        raise Exception("Runtime error: unknown identifier {}".format(self._id))

    def substitute (self,ids,new_es):
        for i in range(len(ids)):
            id = ids[i]
            new_e = new_es[i]
            if id == self._id:
                return new_e
        return self


    
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





# Primitive operations

def oper_plus (v1,v2): 
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value + v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")

def oper_minus (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value - v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")

def oper_times (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value * v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")


# Initial primitives dictionary

INITIAL_PRIM_DICT = {
    "+": oper_plus,
    "*": oper_times,
    "-": oper_minus
}
