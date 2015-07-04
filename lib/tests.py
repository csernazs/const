from pprint import pprint
import unittest
import bytecode
from const import const, PERMITTED


class TestByteCode(unittest.TestCase):

    def test_simple(self):
        def func():
            a, b, c = range(3)

        actual = [bytecode.command_to_string(command, arg) for command, arg in bytecode.ByteCode(func.func_code.co_code)]
        expected = ['LOAD_GLOBAL 0',
                    'LOAD_CONST 1',
                    'CALL_FUNCTION 1',
                    'UNPACK_SEQUENCE 3',
                    'STORE_FAST 0',
                    'STORE_FAST 1',
                    'STORE_FAST 2',
                    'LOAD_CONST 0',
                    'RETURN_VALUE']

        self.assertEqual(expected, actual)

    def test_extended(self):
        code_str = ",".join(["v_%d" % idx for idx in xrange(70000)]) + "= range(70000)"
        actual = list(bytecode.ByteCode(compile(code_str, "a.py", "exec").co_code))
        actual = [bytecode.command_to_string(command, arg) for command, arg in actual]
        expected = ['STORE_NAME 69993',
                    'STORE_NAME 69994',
                    'STORE_NAME 69995',
                    'STORE_NAME 69996',
                    'STORE_NAME 69997',
                    'STORE_NAME 69998',
                    'STORE_NAME 69999',
                    'STORE_NAME 70000',
                    'LOAD_CONST 1',
                    'RETURN_VALUE']

        self.assertEqual(expected, actual[-10:])


class TestConst(unittest.TestCase):

    def test_class(self):
        class Example(object):
            CONST_A, CONST_B, CONST_C_WITH_UNDERSCORES = const("DASH")
            CONST_D, CONST_E = const("NUMBER0")
            CONST_F, CONST_G = const("SAME")

            N1, N2 = const("NUMBER1")
            SINGLE = const("DASH")

        self.assertEqual("const-a", Example.CONST_A)
        self.assertEqual("const-b", Example.CONST_B)
        self.assertEqual("const-c-with-underscores", Example.CONST_C_WITH_UNDERSCORES)
        self.assertEqual(0, Example.CONST_D)
        self.assertEqual(1, Example.CONST_E)
        self.assertEqual("CONST_F", Example.CONST_F)
        self.assertEqual("CONST_G", Example.CONST_G)
        self.assertEqual(1, Example.N1)
        self.assertEqual(2, Example.N2)
        self.assertEqual("single", Example.SINGLE)

    def test_prefix(self):
        class Example(object):
            PERMITTED_VALUES, CONST_A, CONST_B, CONST_C = const("SAME", PERMITTED)

        self.assertEqual("CONST_A", Example.CONST_A)
        self.assertEqual("CONST_B", Example.CONST_B)
        self.assertEqual("CONST_C", Example.CONST_C)

        self.assertEqual({"CONST_A", "CONST_B", "CONST_C"}, Example.PERMITTED_VALUES)

if __name__ == "__main__":
    unittest.main()
