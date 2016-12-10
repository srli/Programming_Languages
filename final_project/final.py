############################################################
# Simple imperative language
# C-like surface syntac
# with S-expression syntax for expressions
# (no recursive closures)
#

"""
Changes made:
-while loops and for loops have a final semicolon after the closing curly bracket
-spaces are required between arithmetic: ie. 1 + 1 not 1+1
-i don't even know what's wrong with sample-dict, but dictionary operations are working from our unit tests.... but not on sample-dict.pj
-anonymous functions are non-functional. return values aren't actually returned
-for loops are non-functional
"""

import sys
import copy
import argparse

from pyparsing import Word, ZeroOrMore, OneOrMore, Forward

def initial_env_imp():
    print "hello"

def print_res(result):
    print result

def parse_imp (input):
    stringChars = "abcdefghijklmnopqrtuvwxyz0123456789_"
    varChars = "ABCDEFGHIJKLMNOPQRTUVWXYZ"

    ######VALUES
    pVARIABLE = Word(varChars, stringChars + varChars)
    pVARIABLE.setParseAction(lambda result: print_res(result))

    pSTRING = Word(stringChars)
    pSTRING.setParseAction(lambda result: print_res(result))

    pLIT = Forward()

    pLITERAL = pSTRING + "(" + (pVARIABLE|pSTRING) + "," + (pVARIABLE|pSTRING) + ")"
    pLITERAL.setParseAction(lambda result: print_res(result))

    pLIT_STATEMENT = pLITERAL + "."
    pLIT_STATEMENT.setParseAction(lambda result: print_res(result))

    pLIT_QUERY = pLITERAL + "?"
    pLIT_QUERY.setParseAction(lambda result: print_res(result))

    pLIT_DEFINE = pLITERAL + ":-" + "[" + pLITERAL + ZeroOrMore("," + pLITERAL) + "]"
    pLIT_DEFINE.setParseAction(lambda result: print_res(result))

    pLIT << (pLIT_DEFINE | pLIT_STATEMENT | pLIT_QUERY )

    result = pLIT.parseString(input)[0]
    return result    # the first element of the result is the expression


class Shell():
    def __init__(self):
        self.env = initial_env_imp()

    def shell_imp (self):
        # A simple shell
        # Repeatedly read a line of input, parse it, and evaluate the result

        print "Final Project - Logic Language Interpreter"

        while True:
            inp = raw_input("imp> ")
            try:
                result = parse_imp(inp)
                print result
                # if result["result"] == "statement":
                #     stmt = result["stmt"]
                #     print "Abstract representation:", stmt
                #     v = stmt.eval(self.env)
                #
                # elif result["result"] == "abstract":
                #     print_res(result)["stmt"]
                #
                # elif result["result"] == "quit":
                #     return
                #
                # elif result["result"] == "declaration":
                #     (name,expr) = result["decl"]
                #     v = expr.eval(self.env)
                #     self.env.insert(0,(name,VRefCell(v)))
                #     print "{} defined".format(name)


            except Exception as e:
                print "Exception: {}".format(e)

        return


s = Shell()
s.shell_imp()
