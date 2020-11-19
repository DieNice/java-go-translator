from column import Column
from node import Node
from production import Production
from rule import Rule
from state import State


def predict(col, rule):
    for prod in rule.productions:
        col.add(State(rule.name, prod, 0, col))


def scan(col, state, token):
    if token != col.token:
        return
    col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))


def complete(col, state):
    if not state.completed():
        return
    for st in state.start_column:
        term = st.next_term()
        if not isinstance(term, Rule):
            continue
        if term.name == state.name:
            col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))


GAMMA_RULE = u"GAMMA"


def parse(rule, text):
    table = [Column(i, tok) for i, tok in enumerate([None] + text.lower().split())]
    table[0].add(State(GAMMA_RULE, Production(rule), 0, table[0]))

    for i, col in enumerate(table):
        for state in col:
            if state.completed():
                complete(col, state)
            else:
                term = state.next_term()
                if isinstance(term, Rule):
                    predict(col, term)
                elif i + 1 < len(table):
                    scan(table[i + 1], state, term)
    for st in table[-1]:
        if st.name == GAMMA_RULE and st.completed():
            return st
    else:
        raise ValueError("parsing failed")


def build_trees(state):
    return build_trees_helper([], state, len(state.rules) - 1, state.end_column)


def build_trees_helper(children, state, rule_index, end_column):
    if rule_index < 0:
        return [Node(state, children)]
    elif rule_index == 0:
        start_column = state.start_column
    else:
        start_column = None

    rule = state.rules[rule_index]
    outputs = []
    for st in end_column:
        if st is state:
            break
        if st is state or not st.completed() or st.name != rule.name:
            continue
        if start_column is not None and st.start_column != start_column:
            continue
        for sub_tree in build_trees(st):
            for node in build_trees_helper([sub_tree] + children, state, rule_index - 1, st.start_column):
                outputs.append(node)
    return outputs


if __name__ == '__main__':
    SYM = Rule("SYM", Production("a"))
    OP = Rule("OP", Production("+"))
    EXPR = Rule("EXPR", Production(SYM))
    EXPR.add(Production(EXPR, OP, EXPR))

    for i in range(1, 9):
        text = " + ".join(["a"] * i)
        q0 = parse(EXPR, text)
        forest = build_trees(q0)
        print(len(forest), text)

    N = Rule("N", Production("time"), Production("flight"), Production("banana"),
             Production("flies"), Production("boy"), Production("telescope"))
    D = Rule("D", Production("the"), Production("a"), Production("an"))
    V = Rule("V", Production("book"), Production("eat"), Production("sleep"), Production("saw"))
    P = Rule("P", Production("with"), Production("in"), Production("on"), Production("at"),
             Production("through"))

    PP = Rule("PP")
    NP = Rule("NP", Production(D, N), Production("john"), Production("houston"))
    NP.add(Production(NP, PP))
    PP.add(Production(P, NP))

    VP = Rule("VP", Production(V, NP))
    VP.add(Production(VP, PP))
    S = Rule("S", Production(NP, VP), Production(VP))

    for tree in build_trees(parse(S, "book the flight through houston")):
        print("--------------------------")
        tree.print_()

    for tree in build_trees(parse(S, "john saw the boy with the telescope")):
        print("--------------------------")
        tree.print_()
