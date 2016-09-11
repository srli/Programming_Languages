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

    def test_Vector_simple_math(self):
        v1 = EVector([EInteger(2),EInteger(3)])
        v2 = EVector([EInteger(33),EInteger(66)])

        self.assertEqual(pair(EPlus(v1,v2).eval()),(35, 69))
        self.assertEqual(pair(EMinus(v1,v2).eval()),(-31, -63))

    def test_Vector_boolean_logic(self):
        b1 = EVector([EBoolean(True),EBoolean(False)])
        b2 = EVector([EBoolean(False),EBoolean(False)])

        self.assertEqual(pair(EAnd(b1,b2).eval()), (False, False))
        self.assertEqual(pair(EOr(b1,b2).eval()), (True, False))
        self.assertEqual(pair(ENot(b1).eval()), (False, True))

    def test_ETimes(self):
        v1 = EVector([EInteger(2),EInteger(3)])
        v2 = EVector([EInteger(33),EInteger(66)])

        self.assertEqual(ETimes(v1,v2).eval().value, 264)
        self.assertEqual(ETimes(v1,EPlus(v2,v2)).eval().value, 528)
        self.assertEqual(ETimes(v1,EMinus(v2,v2)).eval().value, 0)

    def test_vector_scalar_math(self):
        v1 = EVector([EInteger(2),EInteger(3)])
        v2 = EVector([EInteger(33),EInteger(66)])

        self.assertEqual(pair(EPlus(v1,EInteger(100)).eval()), (102, 103))
        self.assertEqual(pair(EPlus(EInteger(100),v1).eval()), (102, 103))
        self.assertEqual(pair(EMinus(v1,EInteger(100)).eval()), (-98, -97))
        self.assertEqual(pair(EMinus(EInteger(100),v1).eval()), (98, 97))
        self.assertEqual(pair(ETimes(v1,EInteger(100)).eval()), (200, 300))
        self.assertEqual(pair(ETimes(EInteger(100),v1).eval()), (200, 300))

        self.assertEqual(pair(EAnd(EVector([EBoolean(True),EBoolean(False)]),EBoolean(True)).eval()), (True, False))
        self.assertEqual(pair(EOr(EVector([EBoolean(True),EBoolean(False)]),EBoolean(True)).eval()), (True, True))

    # def test_VRational(self):
    #     self.assertEqual(VRational(1,3).numer, 1)
    #     self.assertEqual(VRational(1,3).denom, 3)
    #     self.assertEqual(VRational(2,3).numer, 2)
    #     self.assertEqual(VRational(2,3).denom, 3)

    # def test_EDiv(self):
    #     self.assertEqual(rat(EDiv(EInteger(1),EInteger(2)).eval()), '1/2')
    #     self.assertEqual(rat(EDiv(EInteger(2),EInteger(3)).eval()), '2/3')
    #     self.assertEqual(rat(EDiv(EDiv(EInteger(2),EInteger(3)),EInteger(4)).eval()), '1/6')
    #     self.assertEqual(rat(EDiv(EInteger(2),EDiv(EInteger(3),EInteger(4))).eval()), '8/3')

    # def test_rational_math(self):
    #     half = EDiv(EInteger(1),EInteger(2))
    #     third = EDiv(EInteger(1),EInteger(3))

    #     self.assertEqual(rat(EPlus(half,third).eval()), '5/6')
    #     self.assertEqual(rat(EPlus(half,EInteger(1)).eval()), '3/2')
    #     self.assertEqual(rat(EMinus(half,third).eval()), '1/6')
    #     self.assertEqual(rat(EMinus(half,EInteger(1)).eval()), '-1/2')
    #     self.assertEqual(rat(ETimes(half,third).eval()), '1/6')
    #     self.assertEqual(rat(ETimes(half,EInteger(1)).eval()), '1/2')

    # def test_simplest_form(self):
    #     self.assertEqual(rat(EDiv(EInteger(3),EInteger(6)).eval()), '1/2')
    #     self.assertEqual(rat(EDiv(EInteger(4),EInteger(6)).eval()), '2/3')
    #     self.assertEqual(rat(EDiv(EInteger(-4),EInteger(6)).eval()), '-2/3')
    #     self.assertEqual(rat(EDiv(EInteger(-4),EInteger(-6)).eval()), '2/3')

    #     self.assertEqual(EDiv(EInteger(2),EInteger(1)).eval(), <__main__.VInteger object at 0x100f5e590>)
    #     self.assertEqual(EDiv(EInteger(2),EInteger(1)).eval().value, 2)
    #     self.assertEqual(EDiv(EInteger(4),EInteger(2)).eval(), <__main__.VInteger object at 0x100f5e650>)
    #     self.assertEqual(EDiv(EInteger(4),EInteger(2)).eval().value, 2 )


if __name__ == '__main__':
    unittest.main()
