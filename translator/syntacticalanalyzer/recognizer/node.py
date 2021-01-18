class Node(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def print_(self, level=0):
        print("  " * level + str(self.value))
        for child in self.children:
            child.print_(level + 1)
