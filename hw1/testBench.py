from homework1 import *
import unittest

class TestCases(unittest.TestCase):

    def test_EIsZero(self):
        self.assertTrue(EIsZero(EInteger(0)).eval().value)
        self.assertFalse(EIsZero(EInteger(1)).eval().value)
        self.assertFalse(EIsZero(EInteger(9)).eval().value)
        self.assertFalse(EIsZero(EInteger(-1)).eval().value)
        self.assertFalse(EIsZero(EPlus(EInteger(1),EInteger(1))).eval().value)
        self.assertTrue(EIsZero(EMinus(EInteger(1),EInteger(1))).eval().value)

    def test_EAnd(self):
        tt = EBoolean(True)
        ff = EBoolean(False)

        self.assertTrue(EAnd(tt,tt).eval().value)
        self.assertFalse(EAnd(tt,ff).eval().value)
        self.assertFalse(EAnd(ff,tt).eval().value)
        self.assertFalse(EAnd(ff,ff).eval().value)

        self.assertTrue(EAnd(EOr(tt,ff),EOr(ff,tt)).eval().value)
        self.assertFalse(EAnd(EOr(tt,ff),EOr(ff,ff)).eval().value)
        self.assertFalse(EAnd(tt,ENot(tt)).eval().value)
        self.assertTrue(EAnd(tt,ENot(ENot(tt))).eval().value)

    def test_EOr(self):
        tt = EBoolean(True)
        ff = EBoolean(False)

        self.assertTrue(EOr(tt,tt).eval().value)
        self.assertTrue(EOr(tt,ff).eval().value)
        self.assertTrue(EOr(ff,tt).eval().value)
        self.assertFalse(EOr(ff,ff).eval().value)


    def test_ENot(self):
        tt = EBoolean(True)
        ff = EBoolean(False)

        self.assertFalse(ENot(tt).eval().value)
        self.assertTrue(ENot(ff).eval().value)

    def test_conj_short_circuit(self):
        tt = EBoolean(True)
        ff = EBoolean(False)

        self.assertFalse(EAnd(ff,EInteger(10)).eval().value)
        self.assertFalse(EAnd(ff,EInteger(0)).eval().value)
        self.assertTrue(EOr(tt,EInteger(10)).eval().value)
        self.assertTrue(EOr(tt,EInteger(0)).eval().value)

    def test_VVector(self):
        self.assertEqual(VVector([]).length, 0)
        self.assertEqual(VVector([VInteger(10),VInteger(20),VInteger(30)]).length, 3)
        self.assertEqual(VVector([VInteger(10),VInteger(20),VInteger(30)]).get(0).value, 10)
        self.assertEqual(VVector([VInteger(10),VInteger(20),VInteger(30)]).get(1).value, 20)
        self.assertEqual(VVector([VInteger(10),VInteger(20),VInteger(30)]).get(2).value, 30)

    def test_EVector(self):
        self.assertEqual(EVector([]).eval().length, 0)
        self.assertEqual(EVector([EInteger(10),EInteger(20),EInteger(30)]).eval().length, 3)
        self.assertEqual(EVector([EInteger(10),EInteger(20),EInteger(30)]).eval().get(0).value, 10)
        self.assertEqual(EVector([EInteger(10),EInteger(20),EInteger(30)]).eval().get(1).value, 20)
        self.assertEqual(EVector([EInteger(10),EInteger(20),EInteger(30)]).eval().get(2).value, 30)
        self.assertEqual(EVector([EPlus(EInteger(1),EInteger(2)),EInteger(0)]).eval().length, 2)
        self.assertEqual(EVector([EPlus(EInteger(1),EInteger(2)),EInteger(0)]).eval().get(0).value, 3)
        self.assertEqual(EVector([EPlus(EInteger(1),EInteger(2)),EInteger(0)]).eval().get(1).value, 0)
        self.assertEqual(EVector([EBoolean(True),EAnd(EBoolean(True),EBoolean(False))]).eval().length, 2)
        self.assertEqual(EVector([EBoolean(True),EAnd(EBoolean(True),EBoolean(False))]).eval().get(0).value, True)
        self.assertEqual(EVector([EBoolean(True),EAnd(EBoolean(True),EBoolean(False))]).eval().get(1).value, False)


if __name__ == '__main__':
    unittest.main()
