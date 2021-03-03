from ...lexicalanalyzer.env import Env
from ...lexicalanalyzer.idtable import IdTable
from ..recognizer.syntacticaltree import SyntacticalTree
from ..recognizer.syntacticaltree import Node
from ..recognizer.rule import Rule


class NodeStruct:
    def __init__(self, isNonterminal: bool, name: str, value: str = '', prev=None) -> None:
        self.name = name
        self.value = value
        self.isNonterminal = isNonterminal
        self.prev = prev
        self.childs = []

    def __str__(self):
        nonterm = "Nonterminal"
        if self.isNonterminal == False:
            nonterm = "Terminal"
        res = '[' + nonterm + ';' + self.name + ';' + self.value + ']'
        return res


class SyntacticsStructure:
    def __init__(self, stree: SyntacticalTree):
        self.uselessterms = ["public", "void", "main", "(", "String[]", "args", ")", "{", "}", "class", ",", "if",
                             "System.out.print", "System.out.println", "\'", "for", "while", "\"", ";", "do"]
        self.operations = ['+', '-', '*', '/', '%', '++', '--', '>', '<', '>=', '<=', '==', '!=', '&&', '||', '!', '=']
        self.root = self._copytree(stree)
        self._reformattree(self.root)

    def _isoperation(self, ptr: NodeStruct) -> bool:
        '''Check if the node has signed descendants'''
        for i in ptr.childs:
            if i.name in self.operations:
                return True
        return False

    def _deleteoperationterm(self, ptr: NodeStruct) -> None:
        '''Delete operation term in Node'''
        for i in ptr.childs:
            if i.name in self.operations:
                ptr.name = i.name
                ptr.childs.remove(i)

    def _haveuselessterm(self, ptr: NodeStruct):
        '''checks the tree for useless symbols'''
        res = False
        for i in ptr.childs:
            if i.name in self.uselessterms:
                res = True
                break
        return res

    def _deleteuslessterm(self, ptr: NodeStruct) -> None:
        '''Delete useless terminal symbol'''
        for i in ptr.childs:
            if i.name in self.uselessterms:
                ptr.remove(i)
                break

    def _checkcomplete(self) -> bool:
        '''checks the tree for nonterminal symbols step 1'''

        def _search(ptr: NodeStruct):
            if ptr.isNonterminal:
                return False
            if ptr.childs:
                for i in ptr.childs:
                    if _search(i, newnode) == True:
                        return False
            return True

        return _search(self.root)

    def _havealonechild(self, ptr: NodeStruct) -> bool:
        '''Does a node have a single descendant node'''
        return len(ptr.childs) == 1

    def _havenonterminalchilds(self, ptr: NodeStruct) -> bool:
        '''check non terminal childs of ptr Node'''

        def _search(ptr: NodeStruct):
            if ptr.isNonterminal:
                return False
            if ptr.childs:
                for i in ptr.childs:
                    if _search(i, newnode) == True:
                        return False
            return True

        return _search(ptr)

    def _replace_node(self, parent: NodeStruct, newNode: NodeStruct) -> None:
        for i in range(len(parent.prev.childs)):
            if parent == parent.prev.childs[i]:
                prevbuf = parent.prev
                parent.prev.childs[i] = newNode
                parent.prev.childs[i].prev = prevbuf
                break

    def _reformattree(self, ptr: NodeStruct) -> None:
        '''Algorithm for converting an output tree into an operation tree https://studopedia.su/14_133217_derevo-razbora-preobrazovanie-dereva-razbora-v-derevo-operatsiy.html'''
        while not self._checkcomplete():  # step 1
            while True:
                lastnode = self.getlastnonterm(ptr)  # step 2
                if self._havealonechild(lastnode):  # step3
                    self._replace_node(lastnode, lastnode.childs[0])
                    # return to step1
                    self._reformattree(ptr)
                    break
                else:
                    if self._haveuselessterm(lastnode):  # step 4
                        self._deleteuslessterm(lastnode)
                    else:
                        if self._isoperation(ptr):  # step 5
                            self._deleteoperationterm(ptr)
                            self._reformattree(ptr)
                            break
                        else:
                            if not self._havenonterminalchilds(lastnode):  # step 6
                                break
            break

    def getlastnonterm(self, ptr) -> NodeStruct:
        '''Select the leftmost tree node marked with a nonterminal symbol'''

        def _search(ptr: NodeStruct):
            for i in ptr.childs:
                if i.isNonterminal:
                    return _search(i)
            return ptr

        return _search(ptr)

    def _copytree(self, stree: SyntacticalTree):
        '''Constructor of copying'''

        def _search(ptr1: Node, ptr2: NodeStruct):
            if ptr1.childs:
                for i in ptr1.childs:
                    n = ''
                    flag = True
                    if isinstance(i.left, Rule):
                        n = i.left.name
                    else:
                        n = i.left
                        flag = False
                    newnode = NodeStruct(flag, n, prev=ptr2)
                    ptr2.childs.append(newnode)
                    _search(i, newnode)

        n = str(stree.root.left)
        res = NodeStruct(True, n)
        _search(stree.root, res)
        return res

    def printast(self):
        '''Output of ast tree'''
        def search(ptr: NodeStruct, level):
            print(str(level) + ':' + '|' + level * ' ' + '├-' + str(ptr))
            if ptr.childs:
                for i in ptr.childs:
                    search(i, level + 1)

        level = 0
        search(self.root, level)
