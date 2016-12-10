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

def execute_query(query, facts, rules):
    query_pred = query[0]
    query_terms = query[1]

    matching_fact_terms = facts.get(query_pred, None)
    matched_terms = []

    if matching_fact_terms:
        for term_set in matching_fact_terms:
            temp_term = []
            for qt in enumerate(i, query_terms):
                if qt[0].isupper():
                    temp_term.append(term_set[i])
                else:
                    if term_set[i] == qt:
                        temp_term.append(temp_set[i])

            if len(temp_term) == len(query_terms):
                matched_terms.append(temp_term)
    print "MATCHED: ", matched_terms
    # matching_rule_terms = rules[query_pred]

def interpret_parse(result):
    if result[-1] == ".":
        predicate = result[0]
        terms = []
        i = 2
        while result[i] != ")":
            if result[i] != ",":
                terms.append(result[i])
            i += 1

        return ("fact", (predicate, terms))

    elif result[-1] == "?":
        predicate = result[0]
        terms = []
        i = 2
        while result[i] != ")":
            if result[i] != ",":
                terms.append(result[i])
            i += 1

        return ("query", (predicate, terms))

    elif result[-1] == "]":
        def_pred = result[0]
        def_terms = []
        i = 2
        while result[i] != ")":
            if result[i] != ",":
                def_terms.append(result[i])
            i += 1
        defined_predicate = (def_pred, def_terms)

        definitions = []
        i += 3
        while result[i] != "]":
            print "I'M AT: ", result[i]
            pred = result[i]
            terms = []
            i += 2
            while result[i] != ")":
                if result[i] != ",":
                    terms.append(result[i])
                i += 1

            definitions.append((pred, terms))
            if result[i + 1] != "]":
                i += 2
            else:
                i += 1

        return ("rule", (defined_predicate, definitions))

def parse_imp (input):
    stringChars = "abcdefghijklmnopqrtuvwxyz0123456789_"
    varChars = "ABCDEFGHIJKLMNOPQRTUVWXYZ"

    ######VALUES
    pVARIABLE = Word(varChars, stringChars + varChars)
    pSTRING = Word(stringChars)

    pLIT = Forward()

    pLITERAL = pSTRING + "(" + pSTRING + "," + pSTRING + ")"
    pQUERY_LITERAL = pSTRING + "(" + (pVARIABLE|pSTRING) + "," + (pVARIABLE|pSTRING) + ")"

    pLIT_STATEMENT = pLITERAL + "."
    pLIT_STATEMENT.setParseAction(lambda result: interpret_parse(result))

    pLIT_QUERY = pQUERY_LITERAL + "?"
    pLIT_QUERY.setParseAction(lambda result: interpret_parse(result))

    pLIT_DEFINE = pQUERY_LITERAL + ":-" + "[" + pQUERY_LITERAL + ZeroOrMore("," + pQUERY_LITERAL) + "]"
    pLIT_DEFINE.setParseAction(lambda result: interpret_parse(result))

    pLIT << (pLIT_DEFINE | pLIT_STATEMENT | pLIT_QUERY )

    result = pLIT.parseString(input)[0]
    return result    # the first element of the result is the expression


class Shell():
    def __init__(self):
        self.facts = {}
        self.rules = {}

    def shell_imp (self):
        # A simple shell
        # Repeatedly read a line of input, parse it, and evaluate the result

        print "Final Project - Logic Language Interpreter"

        while True:
            inp = raw_input("imp> ")
            try:
                result = parse_imp(inp)
                print result
                if result[0] == "fact":
                    self.facts[result[1][0]] = result[1][1]
                elif result[0] == "query":
                    print "EXECUTE QUERY: ", result[1]
                    execute_query(result[1], self.facts, self.rules)
                elif result[0] == "rule":
                    print "GOT: ", result
                    self.rules[result[1][0][0]] = (result[1][0][1], result[1][1])

                print "FACTS: ", self.facts
                print "RULES: ", self.rules

            except Exception as e:
                print "Exception: {}".format(e)

        return


s = Shell()
s.shell_imp()
