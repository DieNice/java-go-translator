from .production import Production

class Node:
    def __init__(self, left, right = [], prev = None):

        self.left = left
        self.right = right
        self.prev = prev
        self.childs = []

    def __repr__(self):
        return "%s" % (self.left)

    def listToTree(self, list):
        i = 0
        for t in self.right[::-1]:
            if len(list) and list[0].name == str(t):
                left, right = (t, list[0].productions[0])
                newNode = Node(left, right, self)
                self.childs.append(newNode)
                list.pop(0)
                newNode.listToTree(list)
            else:
                self.childs.append(Node(t, [], self))

    def __str__(self):
        pass

class SyntacticalTree:

    def __init__(self, list = []):
        self.list = list
        tmp = self.list[0]
        self.root = Node(tmp.name, tmp.productions[0])
        list.pop(0)
        self.root.listToTree(list)
        pass

    def __str__(self):
        pass