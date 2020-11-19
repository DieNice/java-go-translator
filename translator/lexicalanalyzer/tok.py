class Token:
    TYPETOKEN = ("ID", "RESERVED", "KEYWORD", "NUM", "OPERATION", "STRING", "DELIMETER")

    def __init__(self, nametoken, typetoken):
        self.name = nametoken
        self.type = typetoken

    def __str__(self):
        return "{},{}".format(self.name, self.type)

    def __eq__(self, other):
        if not isinstance(other, Token):
            raise Exception("comparable object isn't Token")
        return (self.name == other.name) and (self.type == other.type)

    def __ne__(self, other):
        return not self == other
