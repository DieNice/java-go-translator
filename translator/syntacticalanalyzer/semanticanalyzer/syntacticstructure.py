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
        self.root = self.copytree(stree)

    def checkcomplete(self) -> bool:
        pass

    def copytree(self, stree: SyntacticalTree):
        def search(ptr1: Node, ptr2: NodeStruct):
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
                    search(i, newnode)

        n = str(stree.root.left)
        res = NodeStruct(True, n)
        search(stree.root, res)
        return res

    def printast(self):
        def search(ptr: NodeStruct, level):
            print(str(level) + ':' + '|' + level * ' ' + '├-' + str(ptr))
            if ptr.childs:
                for i in ptr.childs:
                    search(i, level + 1)

        level = 0
        search(self.root, level)
