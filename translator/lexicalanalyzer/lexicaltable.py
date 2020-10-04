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
