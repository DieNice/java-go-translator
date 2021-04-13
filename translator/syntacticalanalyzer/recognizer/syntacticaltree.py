from .production import Production
from .rule import Rule

class Node:
    def __init__(self, left, right = [], prev = None):

        self.left = left
        self.right = right
        self.prev = prev
        self.childs = []

    def __repr__(self):
        return "%s" % (self.left)

    def listToTree(self, rulelist):
        i = 0
        for t in self.right[::-1]:
            if len(rulelist) and rulelist[0].name == str(t):
                left, right = (t, rulelist[0].productions[0])
                newNode = Node(left, right, self)
                self.childs.insert(0, newNode)
                rulelist.pop(0)
                newNode.listToTree(rulelist)
            else:
                self.childs.insert(0, Node(t, [], self))

    def __str__(self):
        pass

class SyntacticalTree:

    def __init__(self, list=[]):
        self.list = list
        tmp = self.list[0]
        self.root = Node(tmp.name, tmp.productions[0])
        list.pop(0)
        self.root.listToTree(list)
        pass

    def printTree(self):
        def search(ptr: Node, level):
            if ptr.prev is None:
                l = 0
            else:
                if isinstance(ptr.prev.left, Rule):
                    l = len(ptr.prev.left.name)
                else:
                    l = len(ptr.prev.left)
            print(str(level) + ':' + '|' + level * ' ' + '├-' + str(ptr.left))
            if ptr.childs:
                for i in ptr.childs:
                    search(i, level + 1)

        level = 0
        search(self.root, level)
        print()

    def __str__(self):
        return 'None'
