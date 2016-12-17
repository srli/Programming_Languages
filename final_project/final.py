############################################################
# Logic interpreter
#Lindsey & Sophie
#

import sys
import copy
import argparse

from pyparsing import Word, ZeroOrMore, OneOrMore, Forward, Optional, Keyword

def match_facts(query, facts):
    query_pred = query[0]
    query_terms = query[1]

    matching_fact_terms = facts.get(query_pred, None)
    matched_terms = []

    if matching_fact_terms:
        for term_set in matching_fact_terms:
            temp_term = []
            i = 0
            for i, qt in enumerate(query_terms):
                if qt[0].isupper():
                    temp_term.append(term_set[i])
                else:
                    if term_set[i] == qt:
                        temp_term.append(term_set[i])

            if len(temp_term) == len(query_terms):
                matched_terms.append(temp_term)

    return matched_terms

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

def match_clause(q, var_order, facts):
    if q[1] == "|":
        final_results = []
        messy_result = (match_clause(q[0], var_order, facts)) + (match_clause(q[2], var_order, facts))
        for item in messy_result:
            if type(item) == list:
                final_results.append(item)
            temp_term = []
            for v in var_order:
                if v in item:
                    temp_term.append(item[v])
            if len(temp_term) == len(var_order):
                final_results.append(temp_term)
        return final_results

    elif q[1] == "&":
        final_results = []
        ret1 = match_clause(q[0], var_order, facts)
        for r in ret1:
            q2_cpy = list(q[2])
            q2_cpy = [r[x] if x in r else x for x in q2_cpy]
            ret2 = match_clause(q2_cpy, var_order, facts)
            for r2 in ret2:
                res = merge_two_dicts(r, r2)
                temp_term = []
                for v in var_order:
                    temp_term.append(res.get(v, None))
                final_results.append(temp_term)

        return final_results

    else:
        #####MATCHING FACTS
        matched_terms = match_facts((q[0], list(q[1:])), facts)
        query_var_order = list(q[1:]) #the var order of the query i.e mom(A,B) is [A,B]

        final_matched_terms = []
        for mt in matched_terms:
            temp_term = {}
            for i, v in enumerate(query_var_order):
                temp_term[v] = mt[i]

            final_matched_terms.append(temp_term)

        return final_matched_terms

def match_rules(query, facts, rules):
    query_pred = query[0]
    query_terms = query[1]

    matching_rule_clauses = rules.get(query_pred, None)
    final_matched_terms = []

    if matching_rule_clauses:
        for clause in matching_rule_clauses:
            var_order = clause[0]
            queries = clause[1]

            res = match_clause(queries, var_order, facts)

            for l in res:
                if type(l) == dict:
                    temp_term = []
                    for v in var_order:
                        temp_term.append(l[v])
                    final_matched_terms.append(temp_term)
                else:
                    final_matched_terms.append(l)

    return final_matched_terms

def execute_query(query, facts, rules):
    results = match_facts(query, facts) + match_rules(query, facts, rules)
    query_vars = query[1]
    rough_results = []

    for res in results:
        temp_term = []
        for i, term in enumerate(query_vars):
            if term[0].isupper():
                temp_term.append(res[i])
            else:
                if res[i] == term:
                    temp_term.append(res[i])
                else:
                    continue
        if len(temp_term) == len(query[1]):
            rough_results.append(temp_term)

    cleaned_res = []
    for r in rough_results:
        if r not in cleaned_res:
            cleaned_res.append(r)
            print query[0] + "(" + ', '.join(r) + ")"

def interpret_parse(result):
    if result[1] == ".":
        return ("fact", (result[0][0], list(result[0][1:])))

    elif result[1] == "?":
        return ("query", (result[0][0], list(result[0][1:])))

    elif result[1] == ":-":
        defined_predicate = result[0]
        return ("rule", ((result[0][0], list(result[0][1:])), result[2]))

def parse_ptail(result):
    if len(result) > 3:
        return (result[1], result[2], result[3])
    else:
        return (result[1])

def parse_lit(result):
    return tuple([result[0]] + result[2:-1][::2])

def parse_imp (input):
    stringChars = "abcdefghijklmnopqrstuvwxyz0123456789_"
    varChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    ######VALUES
    pVARIABLE = Word(varChars, stringChars + varChars)
    pSTRING = Word(stringChars, stringChars + varChars)

    pLIT = Forward()
    pTERM = Forward()

    pLITERAL = pSTRING + "(" + pSTRING + ZeroOrMore("," + pSTRING) + ")"
    pLITERAL.setParseAction(lambda result: parse_lit(result))

    pQUERY_LITERAL = pSTRING + "(" + (pVARIABLE|pSTRING) + ZeroOrMore("," + (pVARIABLE|pSTRING)) + ")"
    pQUERY_LITERAL.setParseAction(lambda result: parse_lit(result))

    pLIT_STATEMENT = pLITERAL + "."
    pLIT_STATEMENT.setParseAction(lambda result: interpret_parse(result))

    pLIT_QUERY = pQUERY_LITERAL + "?"
    pLIT_QUERY.setParseAction(lambda result: interpret_parse(result))

    pLIT_DELETE = "#delete" + pSTRING
    pLIT_DELETE.setParseAction(lambda result: [result])

    pTAIL = "(" + pTERM + Optional((Word("|")|Word("&")) + pTERM) + ")"
    pTAIL.setParseAction(lambda result: parse_ptail(result))

    pLIT_DEFINE = pQUERY_LITERAL + ":-" + pTAIL
    pLIT_DEFINE.setParseAction(lambda result: interpret_parse(result))

    pTERM << (pTAIL | pQUERY_LITERAL)
    pLIT << (pLIT_DEFINE | pLIT_STATEMENT | pLIT_QUERY | pLIT_DELETE)

    result = pLIT.parseString(input)[0]
    return result    # the first element of the result is the expression


class Shell():
    def __init__(self):
        self.facts = {'married': [['alice', 'bob'], ['ivan', 'carl'], ['elise', 'fred']], 'parent': [['alice', 'carl'], ['alice', 'diane'], ['alice', 'elise'], ['ivan', 'jimmy'], ['ivan', 'kendra'], ['elise', 'greg'], ['elise', 'helen']], 'cat': [['elise', 'meow']]}
        self.rules = {'chp': [(['A', 'B'], ((('cat', 'B', 'A'), '&', ('parent', 'C', 'B')), '|', ('married', 'A', 'B')))]}

    def shell_imp (self):
        # A simple shell
        # Repeatedly read a line of input, parse it, and evaluate the result

        print "Final Project - Logic Language Interpreter"
        print "Hello world! :D"
        while True:
            inp = raw_input("imp> ")
            try:
                if inp == "#env":
                    print "FACTS: ", self.facts
                    print "RULES: ", self.rules
                    continue
                elif inp == "#clear":
                    print "CLEARING ENVIRONMENT"
                    self.facts.clear()
                    self.rules.clear()
                    continue

                result = parse_imp(inp)

                if result[0] == "fact":
                    new_facts = self.facts.get(result[1][0], [])
                    new_facts.append(result[1][1])
                    self.facts[result[1][0]] = new_facts

                elif result[0] == "query":
                    execute_query(result[1], self.facts, self.rules)

                elif result[0] == "rule":
                    new_rules = self.rules.get(result[1][0][0], [])
                    new_rules.append((result[1][0][1], result[1][1]))
                    self.rules[result[1][0][0]] = new_rules

                elif result[0] == "#delete":
                    del self.rules[result[1]]

            except Exception as e:
                print "Exception: {}".format(e)

        return


s = Shell()
s.shell_imp()
