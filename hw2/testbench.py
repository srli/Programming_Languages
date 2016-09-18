from homework2 import *
import unittest

class TestCases(unittest.TestCase):

    def test_one(self):
        self.assertEqual(ELet([("a",EInteger(99))],EId("a")).eval(INITIAL_PRIM_DICT).value,  99)
        self.assertEqual(ELet([("a",EInteger(99)),("b",EInteger(66))],EId("a")).eval(INITIAL_PRIM_DICT).value, 99)
        self.assertEqual(ELet([("a",EInteger(99)),("b",EInteger(66))],EId("b")).eval(INITIAL_PRIM_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],ELet([("a",EInteger(66)),("b",EId("a"))],EId("a"))).eval(INITIAL_PRIM_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],ELet([("a",EInteger(66)),("b",EId("a"))],EId("b"))).eval(INITIAL_PRIM_DICT).value, 99)
        self.assertEqual(ELet([("a",EInteger(5)),("b",EInteger(20))],ELet([("a",EId("b")),("b",EId("a"))],EPrimCall("-",[EId("a"),EId("b")]))).eval(INITIAL_PRIM_DICT).value,15)

if __name__ == '__main__':
    unittest.main()
