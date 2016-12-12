############################################################
# Logic interpreter
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

def match_rules(query, facts, rules):
    query_pred = query[0]
    query_terms = query[1]

    matching_rule_clause = rules.get(query_pred, None)

    final_matched_terms = []
    temp_term = []

    if matching_rule_clause:

        all_matched_terms_per_clause = []
        for clause in matching_rule_clause:
            matched_terms_clause = []

            var_order = clause[0]
            queries = clause[1]

            for query in queries:

                #####MATCHING FACTS
                matched_terms = match_facts(query, facts)
                query_var_order = query[1]
                var_order_key = []

                for var in var_order:
                    if var[0].isupper():
                        ind = query_var_order.index(var[0])
                        var_order_key.append(ind)
                    else:
                        var_order_key.append(var)

                print "VOK: ", var_order_key

                for mt in matched_terms:
                    temp_term = []
                    for v in var_order_key:
                        if type(v) == int:
                            temp_term.append(mt[v])
                        else:
                            temp_term.append(v)

                    if len(temp_term) == len(query_terms):
                        final_matched_terms.append(temp_term)

                #####MATCHING RULES
                match_rules_res = match_rules(query, facts, rules)
                for res in match_rules_res:
                    temp_term = []
                    for v in var_order_key:
                        if type(v) == int:
                            temp_term.append(res[v])
                        else:
                            temp_term.append(v)

                    if len(temp_term) == len(query_terms):
                        final_matched_terms.append(temp_term)
                        matched_terms_clause.append(temp_term)

            all_matched_terms_per_clause.append(matched_terms_clause)

    return final_matched_terms

def execute_query(query, facts, rules):
    results = match_facts(query, facts) + match_rules(query, facts, rules)
    for r in results:
        print query[0] + "(" + ', '.join(r) + ")"

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

    else:
        print "GOT: ", result
        return ("rule", ("hi", "bye"))

def parse_ptail(result):
    print "PARSE: ", result
    if len(result) > 3:
        return (result[1], result[2], result[3])
    else:
        return (result[1])

def parse_lit(result):
    print "LIT: ", result
    return (result[0], result[2], result[4])

def parse_imp (input):
    stringChars = "abcdefghijklmnopqrstuvwxyz0123456789_"
    varChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    ######VALUES
    pVARIABLE = Word(varChars, stringChars + varChars)
    pSTRING = Word(stringChars)

    pLIT = Forward()
    pTERM = Forward()

    pLITERAL = pSTRING + "(" + pSTRING + "," + pSTRING + ")"
    pLITERAL.setParseAction(lambda result: parse_lit(result))

    pQUERY_LITERAL = pSTRING + "(" + (pVARIABLE|pSTRING) + "," + (pVARIABLE|pSTRING) + ")"
    pQUERY_LITERAL.setParseAction(lambda result: parse_lit(result))

    pLIT_STATEMENT = pLITERAL + "."
    pLIT_STATEMENT.setParseAction(lambda result: interpret_parse(result))

    pLIT_QUERY = pQUERY_LITERAL + "?"
    pLIT_QUERY.setParseAction(lambda result: interpret_parse(result))

    pTAIL = "(" + pQUERY_LITERAL + Optional((Word("|")|Word("&")) + pTERM) + ")"
    pTAIL.setParseAction(lambda result: parse_ptail(result))

    pLIT_DEFINE = pQUERY_LITERAL + ":-" + pTAIL
    pLIT_DEFINE.setParseAction(lambda result: interpret_parse(result))

    pTERM << (pTAIL | pQUERY_LITERAL)
    pLIT << (pLIT_DEFINE | pLIT_STATEMENT | pLIT_QUERY )

    result = pLIT.parseString(input)[0]
    return result    # the first element of the result is the expression


class Shell():
    def __init__(self):
        self.facts = {'mom': [['john', 'steve'], ['bob', 'sven']]}
        self.rules =  {'dad': [(['A', 'B'], [('mom', ['A', 'B'])])], 'ancs': [(['A', 'B'], [('dad', ['A', 'B'])])]}

    def shell_imp (self):
        # A simple shell
        # Repeatedly read a line of input, parse it, and evaluate the result

        print "Final Project - Logic Language Interpreter"

        while True:
            inp = raw_input("imp> ")
            try:
                if inp == "#env":
                    print "FACTS: ", self.facts
                    print "RULES: ", self.rules
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

            except Exception as e:
                print "Exception: {}".format(e)

        return


s = Shell()
s.shell_imp()
