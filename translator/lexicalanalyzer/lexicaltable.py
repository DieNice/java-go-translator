from tok import Token


class LexicalTable:
    def __init__(self):
        self.tokenslist: Token = []

    def __len__(self):
        return len(self.tokenslist)

    def __getitem__(self, item):
        return self.tokenslist[item]

    def append(self, new: Token):
        self.tokenslist.append(new)

    def __str__(self):
        return str([str(i) for i in self.tokenslist])

    def __eq__(self, other):
        if not isinstance(other, LexicalTable):
            raise Exception("comparable object isn't LexicalTable")
        return self.tokenslist == other.tokenslist

    def __ne__(self, other):
        return not self == other

