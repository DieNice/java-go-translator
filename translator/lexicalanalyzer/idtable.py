class IdTableFactory:

    def createtable(self, pointer):
        newtable = IdTable(pointer)
        return newtable


class IdTable:
    '''Name table storing the name of the identifier and its description, child scopes and parent'''

    def __init__(self, prev=None):
        self.table = {}
        self.childs: IdTable = []
        self.prev: IdTable = prev

    def addid(self, identifier: str, type: str = ''):
        '''adds the name of the identifier'''
        self.table[identifier] = type

    def addtype(self, identifier: str, type):
        '''adds a type to an existing identifier'''
        self.table[identifier] = type

    def getid(self, identifier: str) -> str:
        '''return type of identifier'''
        return self.table.get(identifier)

    def __len__(self):
        return len(self.childs)

    def __getitem__(self, item):
        return self.childs[item]

    def append(self, new):
        self.childs.append(new)

    def __str__(self):
        res = ''
        for i in self.table:
            res = res + str(i) + ':' + str(self.table[i]) + '\n'
        return res
