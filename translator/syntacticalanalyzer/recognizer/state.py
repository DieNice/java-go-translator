from .rule import Rule

class State(object):
    def __init__(self, name, production, dot_index, start_column):
        self.name = name
        self.production = production
        self.start_column = start_column
        self.end_column = None
        self.dot_index = dot_index
        self.rules = [t for t in production if isinstance(t, Rule)]

    def __repr__(self):
        terms = [str(p) for p in self.production]
        terms.insert(self.dot_index, u"$")
        return "%-5s -> %-16s [%s-%s]" % (self.name, " ".join(terms), self.start_column, self.end_column)

    def __eq__(self, other):
        return (self.name, self.production, self.dot_index, self.start_column) == \
               (other.name, other.production, other.dot_index, other.start_column)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.name, self.production))

    def completed(self):
        return self.dot_index >= len(self.production)

    def next_term(self):
        if self.completed():
            return None
        return self.production[self.dot_index]