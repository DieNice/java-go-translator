from .syntacticstructure import SyntacticsStructure
from .syntacticstructure import NodeStruct
from ...lexicalanalyzer.env import Env
from ...lexicalanalyzer.env import IdTable

class Semanticalanalizer:

    def __init__(self):
        self.env = Env()
        self.envptr = self.env.root
        self.depth = 0
        self.MAXDEPTH = 5
        self.bisoperations = ['+', '-', '*', '/', '%', '>', '<', '>=', '<=', '==', '!=', '&&', '||']
        self.unaroperations = ['!', '++', '--']
        self.numbisoperations = ['+', '-', '*', '/', '%']
        self.numunaroperations = ['++', '--']
        self.logbisoperations = ['>', '<', '>=', '<=', '==', '!=', '&&', '||']
        self.logunaroperations = ['!']
        self.strbisoperations = ['+']
        self.logtypes = ['boolean']
        self.inttypes = ['byte', 'short', 'int', 'long', 'char']
        self.floattypes = ['float', 'double']
        self.stringtypes = ['char', 'String']

    def __settotype(self, node: NodeStruct, type: str):
        pass

    def __getoperationtype(self, oper1: NodeStruct, oper2: NodeStruct):
        type1 = self.__gettype(oper1)
        type2 = self.__gettype(oper2)
        if self.__istransformable(type1, type2):
            return type2
        elif self.__istransformable(type2, type1):
            return type1
        raise Exception('cant transform types {} and {}'.format(type1, type2))

    def __istransformable(self, typefrom: str, typeto: str) -> bool:
        if typefrom == typeto:
            return True
        transfomations = {
            'byte': ['short', 'boolean'],
            'short': ['int', 'boolean'],
            'char': ['int', 'boolean'],
            'int': ['long', 'double', 'float', 'boolean'],
            'long': ['double', 'float', 'boolean'],
            'float': ['double', 'boolean'],
            'double': ['boolean'],
            'boolean': [],
        }
        def search(tmp: str, typeto: str):
            for t in transfomations[tmp]:
                if t == typeto:
                    return True
                elif search(t, typeto):
                    return True
            return False
        return search(typefrom, typeto)

    def __gettype(self, ptr: NodeStruct):
        if ptr.name == 'IDENTIFICATOR':
            tmp = self.env.searchelem(self.envptr, ptr.value)
            if tmp != -1:
                return tmp
            else:
                raise Exception("identificator {} is not defined".format(ptr.value))
        elif ptr.name == 'INTEGER NUMBER':
            if -128 < int(ptr.value) < 127:
                return 'byte'
            elif -32768 < int(ptr.value) < 32767:
                return 'short'
            elif -2147483648 < int(ptr.value) < 2147483647:
                return 'int'
            elif -9223372036854775808 < int(ptr.value) < 9223372036854775807:
                return 'long'
            else:
                raise Exception('too large integer {}'.format(ptr.value))
        elif ptr.name == 'REAL NUMBER':
            return 'float'
        elif ptr.name == 'STRING':
            return 'char'
        elif ptr.name == 'BOOL VALUE':
            return 'boolean'
        elif ptr.name == 'OPERATOR':
            operation = ptr.value
            if len(ptr.childs) == 2:
                '''for bis operations'''
                if operation in self.bisoperations:
                    return self.__getoperationtype(ptr.childs[0], ptr.childs[1])
                else:
                    raise Exception('unknown bis operation {}'.format(operation))
            elif len(ptr.childs) == 1:
                '''for unar operations'''
                opertype_1 = self.__gettype(ptr.childs[0])
                if operation in self.numunaroperations and opertype_1 in self.inttypes + self.floattypes or \
                        operation in self.logunaroperations and opertype_1 in self.logtypes:
                    return opertype_1
                else:
                    raise Exception('unknown unar operation {}'.format(operation))

    def __addscopefor(self, ptr: NodeStruct) -> None:
        self.envptr = self.env.insertnewscope(self.envptr)
        self.depth += 1
        '''checkin nesting depth'''
        if self.depth > self.MAXDEPTH:
            raise Exception('nesting depth is over {}'.format(self.MAXDEPTH))
        self.__search(ptr)
        self.envptr = self.envptr.prev

    def __search(self, ptr: NodeStruct) -> None:
        for i in ptr.childs:
            if i.name in ['DECLARE A VARIABLES']:
                '''add ids to scope'''
                type = i.value
                for j in i.childs:
                    id = None
                    if j.name == 'ASSIGNMENT':
                        id = j.childs[0].value
                        inittype = self.__gettype(j.childs[1])
                        if not self.__istransformable(inittype, type):
                            raise Exception('incompatible types for id {} : {} cannot be converted to {}'.format(id, inittype, type))
                    elif j.name == 'IDENTIFICATOR':
                        id = j.value
                    else:
                        raise Exception('unknown declare variables')
                    self.envptr.addid(id, type)
                    j.idtable = self.envptr
            if i.name in ['CYCLE FOR', 'IF OPERATOR']:
                '''create new scope'''
                self.__addscopefor(i)
                continue
            self.__search(i)

    def scan(self, ast: SyntacticsStructure):
        astptr = ast.root
        self.__addscopefor(astptr)
        return self.env