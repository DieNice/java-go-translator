class Token:
    TYPETOKEN = ("ID", "RESERVED", "KEYWORD", "NUM", "OPERATION", "STRING", "DELIMETER")

    def __init__(self, nametoken, typetoken, value=None):
        self.name = nametoken
        self.type = typetoken
        self.val = value

    def __str__(self):
        return "{},{},{}".format(self.name, self.type, self.val)
