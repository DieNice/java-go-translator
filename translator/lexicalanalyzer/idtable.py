class IdTable:
    def __init__(self, p):
        self.table = {}
        self.next = p

    def put(self, s: str, sym: str):
        self.table[s] = sym

    def get(self, s: str) -> str:
        return self.table[s]
