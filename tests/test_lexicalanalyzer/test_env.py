import unittest
import sys
sys.path.append("../../translator/lexicalanalyzer/")
from env import Env


class InsertNewTestCase(unittest.TestCase):
    env = None
    ptr = None

    def setUp(self) -> None:
        self.env = Env()
        self.ptr = self.env.root

    def tearDown(self) -> None:
        self.env = None

    def test_insert_onelvl(self):
        self.ptr = self.env.insertnewscope(self.ptr)
        self.assertEqual(self.ptr, self.env.root)

    def test_insert_twolvl(self):
        self.ptr = self.env.insertnewscope(self.ptr)
        self.ptr = self.env.insertnewscope(self.ptr)
        self.assertEqual(self.ptr, self.env.root[0])

    def test_insert_threelvl(self):
        self.ptr = self.env.insertnewscope(self.ptr)
        self.ptr = self.env.insertnewscope(self.ptr)
        self.ptr = self.env.insertnewscope(self.ptr)
        self.assertEqual(self.ptr, self.env.root[0][0])




if __name__ == '__main__':
    unittest.main()
