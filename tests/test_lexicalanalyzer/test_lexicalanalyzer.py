import unittest
import sys
import os
sys.path.append("../../translator/lexicalanalyzer/")
from lexicalanalyzer import LexicalAnalyzer
from tok import Token
from env import Env

class ScanTestCase(unittest.TestCase):
    LA = LexicalAnalyzer()
    pathdir = os.getcwd() + "../../in/"
    pathdir = os.path.abspath(pathdir)

    def test_comment1(self):
        name = "\Comment1.java"
        file = open(self.pathdir + name).read()
        result = self.LA.skan((name, file))

        tempTokenList = [
            Token("public", Token.TYPETOKEN[2]),
            Token("class", Token.TYPETOKEN[2]),
            Token("Comment1", Token.TYPETOKEN[0]),
            Token("{", Token.TYPETOKEN[6]),
            Token("public", Token.TYPETOKEN[2]),

            Token("static", Token.TYPETOKEN[2]),
            Token("void", Token.TYPETOKEN[2]),
            Token("main", Token.TYPETOKEN[2]),
            Token("(", Token.TYPETOKEN[6]),
            Token("String[]", Token.TYPETOKEN[2]),

            Token("args", Token.TYPETOKEN[2]),
            Token(")", Token.TYPETOKEN[6]),
            Token("{", Token.TYPETOKEN[6]),
            Token("}", Token.TYPETOKEN[6]),
            Token("}", Token.TYPETOKEN[6]),
        ]

        tempEnv = Env()
        ptr = tempEnv.root
        ptr = tempEnv.insertnewscope(ptr)
        ptr = tempEnv.insertnewscope(ptr)

        self.assertEqual(result[0].tokenslist, tempTokenList)
        self.assertEqual(result[1], tempEnv)


if __name__ == '__main__':
    unittest.main()
