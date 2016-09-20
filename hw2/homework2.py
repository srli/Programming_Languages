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

    def eval (self,prim_dict,func_dict):
        return VInteger(self._integer)

    def substitute (self,ids,new_es):
        return self


class EBoolean (Exp):
    # Boolean literal

    def __init__ (self,b):
        self._boolean = b

    def __str__ (self):
        return "EBoolean({})".format(self._boolean)

    def eval (self,prim_dict,func_dict):
        return VBoolean(self._boolean)

    def substitute (self,ids,new_es):
        return self


class EPrimCall (Exp):

    def __init__ (self,name,es):
        self._name = name
        self._exps = es

    def __str__ (self):
        return "EPrimCall({},[{}])".format(self._name,",".join([ str(e) for e in self._exps]))

    def eval (self,prim_dict,func_dict):
        vs = [ e.eval(prim_dict,func_dict) for e in self._exps ]
        return apply(prim_dict[self._name],vs)

    def substitute (self,ids,new_es):
        new_es = [ e.substitute(ids,new_es) for e in self._exps]
        return EPrimCall(self._name,new_es)

class ECall (Exp):

    def __init__(self, name, param_values):
        self._name = name
        self._param_values = param_values

    def __str__(self):
        return "ECall({},[{}])".format(self._name,",".join([ str(e) for e in self._param_values]))

    def eval(self, prim_dict, func_dict):
            params = func_dict.get(self._name).get("params")
            if len(params) != len(self._param_values):
                raise Exception("Runtime error: incorrect number of parameters given")
            assignments = [(params[i], self._param_values[i]) for i in range(len(params))]
            function_binding = ELet(assignments, func_dict.get(self._name).get("body"))

            return function_binding.eval(prim_dict, func_dict)

    def substitute (self,ids,new_es):
        new_es = [ e.substitute(ids,new_es) for e in self._param_values]
        return ECall(self._name,new_es)

class EIf (Exp):
    # Conditional expression

    def __init__ (self,e1,e2,e3):
        self._cond = e1
        self._then = e2
        self._else = e3

    def __str__ (self):
        return "EIf({},{},{})".format(self._cond,self._then,self._else)

    def eval (self,prim_dict,func_dict):
        v = self._cond.eval(prim_dict,func_dict)
        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval(prim_dict,func_dict)
        else:
            return self._else.eval(prim_dict,func_dict)

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
        # TODO: update this
        return "ELet({},{},{})".format(self._ids,self._e1s,self._e2)

    def eval (self,prim_dict,func_dict):
        # print(self._e2.__str__())

        new_e2 = self._e2.substitute(self._ids, self._e1s)
        # print([x.value for x in self._e1s])
        return new_e2.eval(prim_dict,func_dict)

    def substitute (self,ids, new_e1s):
        new_assignments = []
        new_e2 = self._e2
        e1s = self._e1s
        # print self

        # goes through all of the assignments
        for j in range(len(self._ids)):
            # substitutes values from upper assignment as needed
            for i in range(len(ids)):
                id = ids[i]
                new_e1 = new_e1s[i]
                e1s[j] = e1s[j].substitute(ids, new_e1s)

                if not id in self._ids:
                    new_e2 = new_e2.substitute(ids,new_e1s)

            # adds substituted values as assignments for the new ELet statement that will be returned
            new_assignments.append((self._ids[j], e1s[j]))

        return ELet(new_assignments, new_e2)

class ELetS (Exp):
    # local binding

    def __init__ (self,assignments,e2):
        self._ids = [a[0] for a in assignments]
        # self._ids.reverse()
        self._e1s = [a[1] for a in assignments]
        # self._e1s.reverse()
        self._e2 = e2

        self._elet_result = self._e2
        # self.builder()

    def __str__ (self):
        # TODO: update this
        return "ELetS({},{},{})".format(self._ids,self._e1s,self._e2)

    # def builder(self, ids, new_e1s):
    #     for i in range(len(self._ids)):
    #         self._elet_result = ELet([(self._ids[i], self._e1s[i])], self._elet_result)

    #     # print self._elet_result
    #     # print "-------"
    #     return self._elet_result

    def eval (self,prim_dict,func_dict):
        # print(self._e2.__str__())

        new_e2 = self._e2.substitute(self._ids, self._e1s)
        # print([x.value for x in self._e1s])
        return new_e2.eval(prim_dict,func_dict)

    def substitute (self,ids, new_e1s):
        new_assignments = []
        new_e2 = self._e2
        # print self

        # goes through all of the assignments
        for j in range(len(self._ids)):
            # first sub the other parameters
            for i in range(j,len(self._ids)):
                self._e1s[i] = self._e1s[i].substitute([j], [self._e1s[i]])
            print(self._ids, self._e1s)

            # substitutes values from upper assignment as needed
            for i in range(len(ids)):
                id = ids[i]
                new_e1 = new_e1s[i]
                self._e1s[j] = self._e1s[j].substitute(ids, new_e1s)

                if not id in self._ids:
                    new_e2 = new_e2.substitute(ids,new_e1s)

            # adds substituted values as assignments for the new ELet statement that will be returned
            new_assignments.append((self._ids[j], self._e1s[j]))

        return ELet(new_assignments, new_e2)

class ELetV (Exp):
    # local binding

    def __init__ (self,id,e1,e2):
        self._id = id
        self._e1 = e1
        self._e2 = e2

    def __str__ (self):
        return "ELet({},{},{})".format(self._id,self._e1,self._e2)

    def eval (self,prim_dict,func_dict):
        new_e = EInteger(self._e1.eval(prim_dict,func_dict).value)
        new_e2 = self._e2.substitute(self._id,new_e)
        return new_e2.eval(prim_dict,func_dict)

    def substitute (self,id,new_e):
        if id == self._id:
            return ELetV(self._id,
                        self._e1.substitute(id,new_e),
                        self._e2)
        return ELetV(self._id,
                    self._e1.substitute(id,new_e),
                    self._e2.substitute(id,new_e))

class ELetN (Exp):
    # local binding

    def __init__ (self,id,e1,e2):
        self._id = id
        self._e1 = e1
        self._e2 = e2
        self._evaluated_ids = {}

    def __str__ (self):
        return "ELet({},{},{})".format(self._id,self._e1,self._e2)

    def eval (self,prim_dict,func_dict):
        new_e2 = self._e2.substitute(self._id,self._e1)
        return new_e2.eval(prim_dict,func_dict)

    def substitute (self,id,new_e):
        if id == self._id:
            return ELet(self._id,
                        self._e1.substitute(id,new_e),
                        self._e2)
        return ELet(self._id,
                    self._e1.substitute(id,new_e),
                    self._e2.substitute(id,new_e))


class EId (Exp):
    # identifier

    def __init__ (self,id):
        self._id = id

    def __str__ (self):
        return "EId({})".format(self._id)

    def eval (self,prim_dict,func_dict):
        raise Exception("Runtime error: unknown identifier {}".format(self._id))

    def substitute (self,ids,new_es):
        if type(new_es) == list:
            for i in range(len(ids)):
                id = ids[i]
                new_e = new_es[i]
                if id == self._id:
                    return new_e
        else:
            if ids == self._id:
                return new_es
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

def oper_zero (v1):
    if v1.type == "integer":
        return VBoolean(v1.value==0)
    raise Exception ("Runtime error: type error in zero?")


# Initial primitives dictionary

INITIAL_PRIM_DICT = {
    "+": oper_plus,
    "*": oper_times,
    "-": oper_minus,
    "zero?": oper_zero
}

FUN_DICT = {
      "square": {"params":["x"],
                 "body":EPrimCall("*",[EId("x"),EId("x")])},
      "=": {"params":["x","y"],
            "body":EPrimCall("zero?",[EPrimCall("-",[EId("x"),EId("y")])])},
      "+1": {"params":["x"],
             "body":EPrimCall("+",[EId("x"),EInteger(1)])},
      "sum_from_to": {"params":["s","e"],
                      "body":EIf(ECall("=",[EId("s"),EId("e")]),
                                EId("s"),EPrimCall("+",[EId("s"),
                                ECall("sum_from_to",[ECall("+1",[EId("s")]), EId("e")])]))}
    }
