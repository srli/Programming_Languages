from homework2 import *
import unittest

class TestCases(unittest.TestCase):

    def test_one(self):
        self.assertEqual(ELet([("a",EInteger(99))],EId("a")).eval(INITIAL_PRIM_DICT, FUN_DICT).value,  99)
        self.assertEqual(ELet([("a",EInteger(99)),("b",EInteger(66))],EId("a")).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 99)
        self.assertEqual(ELet([("a",EInteger(99)),("b",EInteger(66))],EId("b")).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],ELet([("a",EInteger(66)),("b",EId("a"))],EId("a"))).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],ELet([("a",EInteger(66)),("b",EId("a"))],EId("b"))).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 99)
        self.assertEqual(ELet([("a",EInteger(5)),("b",EInteger(20))],ELet([("a",EId("b")),("b",EId("a"))],EPrimCall("-",[EId("a"),EId("b")]))).eval(INITIAL_PRIM_DICT, FUN_DICT).value,15)

        self.assertEqual(ELetS([("a",EInteger(99))],EId("a")).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 99)
        self.assertEqual(ELetS([("a",EInteger(99)),
           ("b",EInteger(66))],EId("a")).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 99)
        self.assertEqual(ELetS([("a",EInteger(99)),
           ("b",EInteger(66))],EId("b")).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],
         ELetS([("a",EInteger(66)),
                ("b",EId("a"))],
               EId("a"))).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],
         ELetS([("a",EInteger(66)),
                ("b",EId("a"))],
               EId("b"))).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 66)

        self.assertEqual(ELetS([("a",EInteger(5)),
           ("b",EInteger(20))],
          ELetS([("a",EId("b")),
                 ("b",EId("a"))],
                EPrimCall("-",[EId("a"),EId("b")]))).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 0)

    def test_two(self):
        self.assertEqual(ELetV("a",EInteger(10),EId("a")).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 10)
        self.assertEqual(ELetV("a",EInteger(10),ELetV("b",EInteger(20),EId("a"))).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 10)
        self.assertEqual(ELetV("a",EInteger(10),ELetV("a",EInteger(20),EId("a"))).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 20)
        self.assertEqual(ELetV("a",EPrimCall("+",[EInteger(10),EInteger(20)]), ELetV("b",EInteger(20),EId("a"))).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 30)
        self.assertEqual(ELetV("a",EPrimCall("+",[EInteger(10),EInteger(20)]), ELetV("b",EInteger(20),
        EPrimCall("*",[EId("a"),EId("a")]))).eval(INITIAL_PRIM_DICT, FUN_DICT).value, 900)

    def test_three(self):
        self.assertEqual(ECall("+1",
          [EInteger(100)]).eval(INITIAL_PRIM_DICT,FUN_DICT).value, 101)

        self.assertEqual(ECall("+1",
          [EPrimCall("+",[EInteger(100),EInteger(200)])]).eval(INITIAL_PRIM_DICT,FUN_DICT).value, 301)

        self.assertEqual(ECall("+1",
          [ECall("+1",
                 [EInteger(100)])]).eval(INITIAL_PRIM_DICT,FUN_DICT).value, 102)

        self.assertEqual(ECall("=",[EInteger(1),EInteger(2)]).eval(INITIAL_PRIM_DICT,FUN_DICT).value, False)

        self.assertEqual(ECall("=",[EInteger(1),EInteger(1)]).eval(INITIAL_PRIM_DICT,FUN_DICT).value, True)

        self.assertEqual(ECall("sum_from_to",[EInteger(0),EInteger(10)]).eval(INITIAL_PRIM_DICT,FUN_DICT).value, 55)

if __name__ == '__main__':
    unittest.main()
