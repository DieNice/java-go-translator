from __future__ import annotations
from ...lexicalanalyzer.env import Env
from ...lexicalanalyzer.idtable import IdTable
from ..recognizer.syntacticaltree import SyntacticalTree
from ..recognizer.syntacticaltree import Node
from ..recognizer.rule import Rule


class NodeStruct:
    def __init__(self, isNonterminal: bool, name: str, value: str = '', prev: NodeStruct = None) -> None:
        self.name = name
        self.value = value
        self.isNonterminal = isNonterminal
        self.prev: NodeStruct = prev
        self.childs: list(NodeStruct) = []

    def __str__(self):
        nonterm = "Nonterminal"
        if self.isNonterminal == False:
            nonterm = "Terminal"
        res = '[' + nonterm + ';' + self.name + ';' + self.value + ']'
        return res

    def __repr__(self):
        nonterm = "Nonterminal"
        if self.isNonterminal == False:
            nonterm = "Terminal"
        res = '[' + nonterm + ';' + self.name + ';' + self.value + ']'
        return res

    @property
    def me(self) -> NodeStruct:
        for i in range(len(self.prev.childs)):
            if self == self.prev.childs[i]:
                return self.prev.childs[i]

    @me.setter
    def me(self, newNode) -> None:
        if self.prev == None:
            self.childs = newNode.childs
            self.value = newNode.value
            self.isNonterminal = newNode.isNonterminal
            self.name = newNode.name
        else:
            for i in range(len(self.prev.childs)):
                if self == self.prev.childs[i]:
                    self.prev.childs[i].childs = newNode.childs
                    self.prev.childs[i].value = newNode.value
                    self.prev.childs[i].isNonterminal = newNode.isNonterminal
                    self.prev.childs[i].name = newNode.name
                    break

    @me.deleter
    def me(self):
        del self


class SyntacticsStructure:
    def __init__(self, stree: SyntacticalTree):
        self.uselessterms = ["public", "static", "void", "main", "(", "String[]", "args", ")", "{", "}", "class", ",",
                             "if",
                             "System.out.print", "System.out.println", "\'", "for", "while", "\"", ";", "do"]
        self.operations = ['+', '-', '*', '/', '%', '>', '<', '>=', '<=', '==', '!=', '&&', '||', '=']
        self.unaroperations = ['!', '++', '--']
        self.root = self._copytree(stree)
        self._reformattree(self.root)

    def _isoperation(self, ptr: NodeStruct) -> bool:
        '''Check if the node has signed descendants'''
        if self._havealonechild(ptr):
            if ptr.childs[0].name in self.operations + self.unaroperations:
                return True
        else:
            if self._getoperationchildcount(ptr) == 1:
                i = self._getoperationindex(ptr)
                if ptr.childs[i].childs == []:
                    return True
            elif self._getoperationchildcount(ptr) > 0:
                if len(ptr.childs) == 3 and ptr.childs[1].name in self.operations:
                    return True
                if len(ptr.childs) == 2 and ptr.childs[0].name in self.unaroperations:
                    return True
        return False

    def _deleteoperationterm(self, ptr: NodeStruct) -> None:
        '''Delete operation term in Node'''
        for i in ptr.childs:
            if i.name in self.operations:
                ptr.me.name = i.name
                ptr.me.isNonterminal = i.isNonterminal
                ptr.childs.remove(i)
                break

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
        for j in range(len(ptr.prev.childs)):
            if ptr.prev.childs[j] == ptr:
                for i in ptr.childs:
                    if i.name in self.uselessterms:
                        ptr.prev.childs[j].childs.remove(i)
                        break
                break

    def _checkcomplete(self) -> bool:
        '''checks the tree for nonterminal symbols step 1'''

        def _search(ptr: NodeStruct):
            if ptr.isNonterminal:
                return False
            if ptr.childs:
                for i in ptr.childs:
                    return _search(i)
            return True

        return _search(self.root)

    def _havealonechild(self, ptr: NodeStruct) -> bool:
        '''Does a node have a single descendant node'''
        return len(ptr.childs) == 1

    def _getoperationchildcount(self, ptr: NodeStruct) -> int:
        '''Does a node have a single operation descendant node'''
        opcount = 0
        for i in ptr.childs:
            if i.name in self.operations:
                opcount += 1
        return opcount

    def _getoperationindex(self, ptr: NodeStruct) -> int:
        '''Does a node have a single operation descendant node'''
        for i, t in enumerate(ptr.childs):
            if t.name in self.operations:
                return i
        return -1

    def _havenonterminalchilds(self, ptr: NodeStruct) -> bool:
        '''check non terminal childs of ptr Node'''

        def _search(ptr: NodeStruct):
            if ptr.isNonterminal:
                return False
            if ptr.childs:
                for i in ptr.childs:
                    if _search(i) == True:
                        return False
            return True

        return _search(ptr)

    def _replace_node(self, parent: NodeStruct, newNode: NodeStruct) -> None:
        '''Replacing a node with a new node'''
        parent.me = newNode

    def _reformattree(self, ptr: NodeStruct) -> None:
        '''Modification of algorithm for converting an output tree into an operation tree https://studopedia.su/14_133217_derevo-razbora-preobrazovanie-dereva-razbora-v-derevo-operatsiy.html'''
        #self.printast()
        while not self._checkcomplete():  # step 1
            while True:
                lastnode = self.getlastnonterm(ptr)  # step 2
                if self._havealonechild(lastnode):  # step3
                    lastnode.me = lastnode.childs[0]
                    self._reformattree(ptr)  # return to step1
                elif self._haveuselessterm(lastnode):  # step 4
                    self._deleteuslessterm(lastnode)
                elif self._isoperation(lastnode):  # step 5
                    self._deleteoperationterm(lastnode)
                    self._reformattree(ptr)
                elif lastnode.isNonterminal == True and lastnode.name == "IDENTIFICATOR" and lastnode.prev.name == "IDENTIFICATOR":
                    prevbuf = lastnode.prev
                    lastnode.prev.childs.remove(lastnode)
                    for child in lastnode.childs:
                        child.prev = prevbuf
                        prevbuf.childs.append(child)
                elif lastnode.isNonterminal == True:
                    lastnode.me.isNonterminal = False
                elif not self._havenonterminalchilds(lastnode):  # step 6
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
        print()
        search(self.root, level)
