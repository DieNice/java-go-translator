import unittest
import sys
sys.path.append("../../translator/lexicalanalyzer/")
from idtable import IdTable
from idtable import IdTableFactory

class AddIdTestCase(unittest.TestCase):
    factory = IdTableFactory()

    def test_addid_one(self):
        idname = "i1"
        idtype = "tmp"
        a = self.factory.createtable()
        a.addid(idname, idtype)
        self.assertEqual(a.getid(idname), idtype)

    def test_addid_many(self):
        idname = "i"
        idtype = "tmp"
        a = self.factory.createtable()
        for i in range(10):
            a.addid(idname + str(i), idtype + str(i))
        self.assertEqual(a.getid(idname+"5"), idtype+"5")

class AppendTestCase(unittest.TestCase):
    factory = IdTableFactory()

    def test_append(self):
        a = self.factory.createtable()
        for i in range(10):
            tmp = self.factory.createtable()
            a.append(tmp)
        self.assertEqual(len(a), 10)

if __name__ == '__main__':
    unittest.main()
