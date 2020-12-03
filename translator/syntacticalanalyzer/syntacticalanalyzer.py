from column import Column
from node import Node
from production import Production
from rule import Rule
from state import State
import copy


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


def earley(rule, text):
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
            return table
    else:
        raise ValueError("parsing failed")


def right_parsing(table):
    state = None
    for st in table[-1]:
        if st.name == GAMMA_RULE and st.completed():
            state = st
    return sub_parsing([], table, state, state.end_column.index)


def sub_parsing(acc, table, state: State, j: int):
    acc.append(Rule(state.name,state.production))
    k = len(state.production)
    c = j
    while k != 0:
        Xk = state.production[k - 1]
        if not isinstance(Xk, Rule):
            k -= 1
            c -= 1
        else:
            Ic = table[c]
            # founding the state for Nonterminal Xk
            for st in Ic:
                if st.completed() and st.name == Xk.name:
                    r = st.start_column.index
                    Ir = table[r]
                    # founding the previous state of Nonterminal Xk
                    for prevst in Ir:
                        expectedst = copy.copy(state)
                        expectedst.dot_index = prevst.getindexXk(Xk)
                        expectedst.start_column = prevst.start_column
                        expectedst.end_column = prevst.end_column
                        if not prevst.completed() and prevst == expectedst:
                            sub_parsing(acc, table, st, c)
                            k -= 1
                            c = r
    return acc


if __name__ == '__main__':
    LETTER = Rule("LETTER", Production("A"), Production("B"), Production("C"), Production("D"), Production("E"),
                  Production("F"), Production("G"), Production("H"), Production("I"), Production("J"),
                  Production("K"),
                  Production("L"), Production("M"), Production("N"), Production("O"), Production("P"),
                  Production("Q"),
                  Production("R"), Production("S"), Production("T"), Production("U"), Production("V"),
                  Production("W"),
                  Production("X"), Production("Y"), Production("Z"),
                  Production("a"), Production("b"), Production("c"), Production("d"), Production("e"),
                  Production("f"),
                  Production("g"), Production("h"), Production("i"), Production("j"), Production("k"),
                  Production("l"),
                  Production("m"), Production("n"), Production("o"), Production("p"), Production("q"),
                  Production("r"),
                  Production("s"), Production("t"), Production("u"), Production("v"), Production("w"),
                  Production("x"),
                  Production("y"), Production("z"))

    DIGIT = Rule("DIGIT", Production("1"), Production("2"), Production("3"), Production("4"), Production("5"),
                 Production("6"), Production("7"), Production("8"), Production("9"), Production("0"))
    SIGN = Rule("SIGN", Production("+"), Production("-"), Production(""))
    BOOL_VAL = Rule("BOOL VALUE", Production("true"), Production("false"))
    TYPE_NAME = Rule("TYPE NAME", Production("byte"), Production("short"), Production("int"), Production("long"),
                     Production("float"), Production("double"), Production("char"), Production("boolean"),
                     Production("String"))
    ID_SYMBOLS = Rule("IDENTIFICATOR SYMBOLS", Production(DIGIT), Production(LETTER), Production("_"))
    ID_SYMBOLS.add(Production(DIGIT, ID_SYMBOLS), Production(LETTER, ID_SYMBOLS), Production("_", ID_SYMBOLS))
    IDENTIFICATOR = Rule("IDENTIFICATOR", Production("_", ID_SYMBOLS), Production(LETTER, ID_SYMBOLS),
                         Production(LETTER))

    STRING = Rule("STRING", Production(DIGIT), Production(SIGN), Production(LETTER))
    STRING.add(Production(DIGIT, STRING), Production(SIGN, STRING), Production(LETTER, STRING))
    STR_SGN_SUM = Rule("STRING SUM SIGN", Production("+"))
    STR_SGN_MUL = Rule("STRING MUL SIGN", Production("*"))
    STR_MUL = Rule("STRING MULTIPLIER", Production(IDENTIFICATOR), Production("'", STRING, "'"),
                   Production("\"", STRING, "\""))
    STR_SUM = Rule("STRING ADDENDUM", Production(STR_MUL))
    STR_SUM.add(Production(STR_MUL, STR_SGN_MUL, STR_SUM))
    STR_EXPR = Rule("STRING EXPRESSION", Production(STR_SUM))
    STR_EXPR.add(Production(STR_SUM, STR_SGN_SUM, STR_EXPR))
    STR_MUL.add(Production("(", STR_EXPR, ")"))

    INT_NUM = Rule("INTEGER NUMBER", Production(DIGIT))
    INT_NUM.add(Production(DIGIT, INT_NUM))
    REAL_NUM = Rule("REAL NUMBER", Production(INT_NUM, ".", INT_NUM))
    NUM = Rule("NUMBER", Production(INT_NUM), Production(REAL_NUM))
    ARITH_SGN_SUM = Rule("ARITHMETIC SUM SIGN", Production("+"), Production("-"))
    ARITH_SGN_MUL = Rule("ARITHMETIC MUL SIGN", Production("*"), Production("/"))
    ARITH_MUL = Rule("ARITHMETIC MULTIPLIER", Production(IDENTIFICATOR), Production(NUM))
    ARITH_SUM = Rule("ARITHMETIC ADDENUM", Production(ARITH_MUL))
    ARITH_SUM.add(Production(ARITH_MUL, ARITH_SGN_MUL, ARITH_SUM))
    ARITH_EXPR = Rule("ARITHMETIC EXPRESSION", Production(ARITH_SUM))
    ARITH_EXPR.add(Production(ARITH_SUM, ARITH_SGN_SUM, ARITH_EXPR))
    ARITH_MUL.add(Production("(", ARITH_EXPR, ")"))


    LOG_SGN_SUM = Rule("LOGIC SUM SIGN", Production("||"))
    LOG_SGN_MUL = Rule("LOGIC MUL SIGN", Production("&&"))
    LOG_SGN_CMP = Rule("LOGIC COMPARE SIGN", Production("=="), Production("!="), Production(">"),
                       Production("<"), Production(">="), Production("<="))
    LOG_MUL = Rule("LOGIC MULTIPLIER", Production(IDENTIFICATOR),
                   Production(BOOL_VAL), Production(ARITH_EXPR, LOG_SGN_CMP, ARITH_EXPR))
    LOG_SUM = Rule("LOGIC ADDENUM", Production(LOG_MUL))
    LOG_SUM.add(Production(LOG_MUL, LOG_SGN_MUL, LOG_SUM))
    LOG_EXPR = Rule("LOGIC EXPRESSION", Production(LOG_SUM))
    LOG_EXPR.add(Production(LOG_SUM, LOG_SGN_SUM, LOG_EXPR))
    LOG_MUL.add(Production(LOG_EXPR, LOG_SGN_CMP, LOG_EXPR), Production("(", LOG_EXPR, ")"))

    EXPR = Rule("EXPRESSION", Production(STR_EXPR), Production(ARITH_EXPR), Production(LOG_EXPR))

    ARGS = Rule("ARGUMENTS", Production(EXPR))
    ARGS.add(Production(EXPR, ",", ARGS))
    STD_FUNCS = Rule("STANDARD FUNCTIONS", Production("Math.log", "(", ARGS, ")"),
                     Production("Math.pow", "(", ARGS, ")"),
                     Production("Math.sqtr", "(", ARGS, ")"))
    ARITH_MUL.add(Production(STD_FUNCS))

    UNARY_OPERS = Rule("UNARY OPERATORS", Production("++"), Production("--"))
    ASSGN = Rule("ASSIGNMENT", Production(IDENTIFICATOR, "=", EXPR), Production(EXPR, UNARY_OPERS))
    OUTPUT_FUNC = Rule("OUTPUT FUNCTION", Production("System.out.print", "(", STR_EXPR, ")"))

    DECLARE_ONE_VAR = Rule("DECLARE A ONE VARIABLE", Production(TYPE_NAME, IDENTIFICATOR),
                           Production(TYPE_NAME, IDENTIFICATOR, "=", EXPR))
    DECLARE_VAR = Rule("DECLARE A VARIABLE", Production(DECLARE_ONE_VAR))
    DECLARE_VAR.add(Production(DECLARE_ONE_VAR, ",", DECLARE_VAR))

    SUGGESTION = Rule("SUGGESTION", Production(DECLARE_VAR), Production(OUTPUT_FUNC), Production(ASSGN))
    SUGGESTION_LIST = Rule("SUGGESTION_LIST", Production(SUGGESTION, ";"))
    SUGGESTION_LIST.add(Production(SUGGESTION, ";", SUGGESTION_LIST))

    MAIN_FUNC = Rule("MAIN FUNCTION", Production("public", "static", "void", "main",
                                                 "(", "String[]", "args", ")", "{", SUGGESTION_LIST, "}"))

    PROGRAMM = Rule("PROGRAMM", Production("public", "class", IDENTIFICATOR, "{", MAIN_FUNC, "}"))

    BREAK_OPERS = Rule("BREAK OPEARTORS", Production("break"), Production("continue"))
    INIT_COUNT = Rule("INIT COUNTER", Production(""), Production(DECLARE_VAR), Production(ASSGN))
    MOD_COUNT = Rule("MODIFY COUNTER", Production(""), Production(ASSGN))
    COND = Rule("CONDITION", Production(LOG_EXPR))
    CYCLE_FOR = Rule("CYCLE FOR", Production("for", "(", INIT_COUNT, ";",
                                             COND, ";", MOD_COUNT, ")", "{",
                                             SUGGESTION_LIST, "}"),
                     Production("for", "(", INIT_COUNT, ";", COND, ";", MOD_COUNT,
                                ")", SUGGESTION))
    CYCLE_WHILE = Rule("CYCLE WHILE", Production("while", "(", COND, ")", "{",
                                                 SUGGESTION_LIST, "}"))
    CYCLE_DO = Rule("CYCLE DO", Production("do", "{", SUGGESTION_LIST, "}",
                                           "while", "(", COND, ")", ))
    CYCLE = Rule("CYCLE", Production(CYCLE_FOR), Production(CYCLE_DO), Production(CYCLE_WHILE))

    IF_OPER = Rule("IF OPERATOR", Production("if", "(", COND, ")", "{",
                                             SUGGESTION_LIST, "}"),
                   Production("if", "(", COND, ")", "{", SUGGESTION_LIST, "}",
                              "else", "{", SUGGESTION_LIST, "}"),
                   Production("if", "(", COND, ")", "{", SUGGESTION_LIST, "}",
                              "else", SUGGESTION),
                   Production("if", "(", COND, ")", SUGGESTION,
                              "else", "{", SUGGESTION_LIST, "}"),
                   Production("if", "(", COND, ")", SUGGESTION))
    SUGGESTION.add(Production(IF_OPER), Production(CYCLE))

    F = Rule("F", Production('a'))
    T = Rule("T", Production(F))
    E = Rule("E", Production(T))
    T.add(Production(F, '*', T))
    E.add(Production(T))
    F.add(Production('(', E, ')'))
    E.add(Production(T, '+', E))

    print(right_parsing(earley(E, '( a + a ) * a')))
