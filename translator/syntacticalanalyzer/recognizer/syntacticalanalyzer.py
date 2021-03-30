from .column import Column
from .node import Node
from .production import Production
from .rule import Rule
from .state import State
from translator.lexicalanalyzer.tok import Token
from .syntacticaltree import SyntacticalTree
import copy


class SyntacticalAnalyzer:

    def __init__(self):
        self.LETTER = Rule("LETTER", Production("A"), Production("B"), Production("C"), Production("D"),
                           Production("E"),
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

        self.DIGIT = Rule("DIGIT", Production("1"), Production("2"), Production("3"), Production("4"), Production("5"),
                          Production("6"), Production("7"), Production("8"), Production("9"), Production("0"))
        self.SIGN = Rule("SIGN", Production("+"), Production("-"), Production(""))
        self.BOOL_VAL = Rule("BOOL VALUE", Production("true"), Production("false"))
        self.TYPE_NAME = Rule("TYPE NAME", Production("byte"), Production("short"), Production("int"),
                              Production("long"),
                              Production("float"), Production("double"), Production("char"), Production("boolean"),
                              Production("String"))
        self.DIGIT_ID = Rule("DIGIT_ID", Production(self.DIGIT))
        self.IDENTIFICATOR = Rule("IDENTIFICATOR", Production("_", self.DIGIT_ID),
                                  Production(self.LETTER, self.DIGIT_ID),
                                  Production(self.LETTER))
        self.DIGIT_ID.add(Production(self.DIGIT, self.DIGIT_ID), Production(self.DIGIT, self.IDENTIFICATOR))
        self.IDENTIFICATOR.add(Production("_", self.IDENTIFICATOR), Production(self.LETTER, self.IDENTIFICATOR))

        for i in self.IDENTIFICATOR.productions:
            for j in range(len(i)):
                if not i.terms[j]:
                    i.terms[j] = self.IDENTIFICATOR
        self.STRING = Rule("STRING", Production(self.DIGIT), Production(self.SIGN), Production(self.LETTER))
        self.STRING.add(Production(self.DIGIT, self.STRING), Production(self.SIGN, self.STRING),
                        Production(self.LETTER, self.STRING))
        self.STR_SGN_SUM = Rule("STRING SUM SIGN", Production("+"))
        self.STR_SGN_MUL = Rule("STRING MUL SIGN", Production("*"))
        self.STR_MUL = Rule("STRING MULTIPLIER", Production(self.IDENTIFICATOR), Production("'", self.STRING, "'"),
                            Production("\"", self.STRING, "\""))
        self.STR_SUM = Rule("STRING ADDENDUM", Production(self.STR_MUL))
        self.STR_SUM.add(Production(self.STR_MUL, self.STR_SGN_MUL, self.STR_SUM))
        self.STR_EXPR = Rule("STRING EXPRESSION", Production(self.STR_SUM))
        self.STR_EXPR.add(Production(self.STR_SUM, self.STR_SGN_SUM, self.STR_EXPR))
        self.STR_MUL.add(Production("(", self.STR_EXPR, ")"))

        self.INT_NUM = Rule("INTEGER NUMBER", Production(self.DIGIT))
        self.INT_NUM.add(Production(self.DIGIT, self.INT_NUM))
        self.REAL_NUM = Rule("REAL NUMBER", Production(self.INT_NUM, ".", self.INT_NUM))
        self.NUM = Rule("NUMBER", Production(self.INT_NUM), Production(self.REAL_NUM),
                        Production(self.SIGN, self.INT_NUM), Production(self.SIGN, self.REAL_NUM))
        self.ARITH_SGN_SUM = Rule("ARITHMETIC SUM SIGN", Production("+"), Production("-"))
        self.ARITH_SGN_MUL = Rule("ARITHMETIC MUL SIGN", Production("*"), Production("/"), Production("%"))
        self.ARITH_MUL = Rule("ARITHMETIC MULTIPLIER", Production(self.IDENTIFICATOR), Production(self.NUM))
        self.ARITH_SUM = Rule("ARITHMETIC ADDENUM", Production(self.ARITH_MUL))
        self.ARITH_SUM.add(Production(self.ARITH_MUL, self.ARITH_SGN_MUL, self.ARITH_SUM))
        self.ARITH_EXPR = Rule("ARITHMETIC EXPRESSION", Production(self.ARITH_SUM))
        self.ARITH_EXPR.add(Production(self.ARITH_SUM, self.ARITH_SGN_SUM, self.ARITH_EXPR))
        self.ARITH_MUL.add(Production("(", self.ARITH_EXPR, ")"))

        self.LOG_SGN_SUM = Rule("LOGIC SUM SIGN", Production("||"))
        self.LOG_SGN_MUL = Rule("LOGIC MUL SIGN", Production("&&"))
        self.LOG_SGN_CMP = Rule("LOGIC COMPARE SIGN", Production("=="), Production("!="), Production(">"),
                                Production("<"), Production(">="), Production("<="))
        self.LOG_MUL = Rule("LOGIC MULTIPLIER", Production(self.IDENTIFICATOR),
                            Production(self.BOOL_VAL), Production(self.ARITH_EXPR, self.LOG_SGN_CMP, self.ARITH_EXPR))
        self.LOG_SUM = Rule("LOGIC ADDENUM", Production(self.LOG_MUL))
        self.LOG_SUM.add(Production(self.LOG_MUL, self.LOG_SGN_MUL, self.LOG_SUM))
        self.LOG_EXPR = Rule("LOGIC EXPRESSION", Production(self.LOG_SUM))
        self.LOG_EXPR.add(Production(self.LOG_SUM, self.LOG_SGN_SUM, self.LOG_EXPR))
        self.LOG_MUL.add(Production(self.LOG_EXPR, self.LOG_SGN_CMP, self.LOG_EXPR),
                         Production("(", self.LOG_EXPR, ")"))

        self.EXPR = Rule("EXPRESSION", Production(self.STR_EXPR), Production(self.ARITH_EXPR),
                         Production(self.LOG_EXPR))

        self.ARGS = Rule("ARGUMENTS", Production(self.EXPR))
        self.ARGS.add(Production(self.EXPR, ",", self.ARGS))
        self.STD_FUNCS = Rule("STANDARD FUNCTIONS", Production("Math.log", "(", self.ARGS, ")"),
                              Production("Math.pow", "(", self.ARGS, ")"),
                              Production("Math.sqrt", "(", self.ARGS, ")"))
        self.ARITH_MUL.add(Production(self.STD_FUNCS))

        self.UNARY_OPERS = Rule("UNARY OPERATORS", Production("++"), Production("--"))
        self.ASSGN = Rule("ASSIGNMENT", Production(self.IDENTIFICATOR, "=", self.EXPR),
                          Production(self.EXPR, self.UNARY_OPERS))
        self.OUTPUT_FUNC = Rule("OUTPUT FUNCTION", Production("System.out.print", "(", self.STR_EXPR, ")"))

        ''' 
        '''
        self.DECLARE_VAR_ONE = Rule("DECLARE A ONE VARIABLE", Production(self.IDENTIFICATOR),
                                    Production(self.IDENTIFICATOR, "=", self.EXPR))
        self.DECLARE_VAR_LIST = Rule("DECLARE A VARIABLE LIST", Production(self.DECLARE_VAR_ONE))
        self.DECLARE_VAR_LIST.add(Production(self.DECLARE_VAR_ONE, ",", self.DECLARE_VAR_LIST))
        self.DECLARE_VAR = Rule("DECLARE A VARIABLES", Production(self.TYPE_NAME, self.DECLARE_VAR_LIST))
        '''
        self.DECLARE_VAR_ONE = Rule("DECLARE A ONE VARIABLE", Production(self.TYPE_NAME, self.IDENTIFICATOR),
                                    Production(self.TYPE_NAME, self.IDENTIFICATOR, "=", self.EXPR))
        self.DECLARE_VAR = Rule("DECLARE A VARIABLE", Production(self.DECLARE_VAR_ONE))
        self.DECLARE_VAR.add(Production(self.DECLARE_VAR_ONE, ",", self.DECLARE_VAR))
        '''

        self.SUGGESTION = Rule("SUGGESTION", Production(self.DECLARE_VAR), Production(self.OUTPUT_FUNC),
                               Production(self.ASSGN))
        self.SUGGESTION_LIST = Rule("SUGGESTION_LIST", Production(self.SUGGESTION, ";"))
        self.SUGGESTION_LIST.add(Production(self.SUGGESTION, ";", self.SUGGESTION_LIST))

        self.MAIN_FUNC = Rule("MAIN FUNCTION", Production("public", "static", "void", "main",
                                                          "(", "String[]", "args", ")", "{", self.SUGGESTION_LIST, "}"),
                              Production("public", "static", "void", "main",
                                         "(", "String[]", "args", ")", "{", "}")
                              )

        self.PROGRAMM = Rule("PROGRAMM", Production("public", "class", self.IDENTIFICATOR, "{", self.MAIN_FUNC, "}"))

        self.BREAK_OPERS = Rule("BREAK OPEARTORS", Production("break"), Production("continue"))
        self.INIT_COUNT = Rule("INIT COUNTER", Production(""), Production(self.DECLARE_VAR), Production(self.ASSGN))
        self.MOD_COUNT = Rule("MODIFY COUNTER", Production(""), Production(self.ASSGN))
        self.COND = Rule("CONDITION", Production(self.LOG_EXPR))
        self.CYCLE_FOR = Rule("CYCLE FOR", Production("for", "(", self.INIT_COUNT, ";",
                                                      self.COND, ";", self.MOD_COUNT, ")", "{",
                                                      self.SUGGESTION_LIST, "}"),
                              Production("for", "(", self.INIT_COUNT, ";", self.COND, ";", self.MOD_COUNT,
                                         ")", self.SUGGESTION))
        self.CYCLE_WHILE = Rule("CYCLE WHILE", Production("while", "(", self.COND, ")", "{",
                                                          self.SUGGESTION_LIST, "}"))
        self.CYCLE_DO = Rule("CYCLE DO", Production("do", "{", self.SUGGESTION_LIST, "}",
                                                    "while", "(", self.COND, ")", ))
        self.CYCLE = Rule("CYCLE", Production(self.CYCLE_FOR), Production(self.CYCLE_DO), Production(self.CYCLE_WHILE))

        self.IF_OPER = Rule("IF OPERATOR", Production("if", "(", self.COND, ")", "{",
                                                      self.SUGGESTION_LIST, "}"),
                            Production("if", "(", self.COND, ")", "{", self.SUGGESTION_LIST, "}",
                                       "else", "{", self.SUGGESTION_LIST, "}")
                            )
        self.SUGGESTION.add(Production(self.IF_OPER), Production(self.CYCLE))

        self.GAMMA_RULE = u"GAMMA"

    def predict(self, col, rule):
        for prod in rule.productions:
            col.add(State(rule.name, prod, 0, col))

    def scan(self, col, state, token):
        if token != col.token:
            return
        col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))

    def complete(self, col, state):
        if not state.completed():
            return
        for st in state.start_column:
            term = st.next_term()
            if not isinstance(term, Rule):
                continue
            if term.name == state.name:
                col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))


    def earley(self, rule, text):
        table = [Column(i, tok) for i, tok in enumerate([None] + text.split())]
        table[0].add(State(self.GAMMA_RULE, Production(rule), 0, table[0]))

        for i, col in enumerate(table):
            for state in col:
                if state.completed():
                    self.complete(col, state)
                else:
                    indextoken = i
                    term = state.next_term()
                    if isinstance(term, Rule):
                        self.predict(col, term)
                    elif i + 1 < len(table):
                        self.scan(table[i + 1], state, term)
        for st in table[-1]:
            if st.name == self.GAMMA_RULE and st.completed():
                return table
        else:
            raise ValueError(
                "SyntaxError \'{} {}\':invalid syntax, Expected:{}".format(table[indextoken].token,
                                                                       table[indextoken + 1].token, term))

    def right_parsing(self, table):
        state = None
        for st in table[-1]:
            if st.name == self.GAMMA_RULE and st.completed():
                state = st
        return self.sub_parsing([], table, state, state.end_column.index)

    def sub_parsing(self, acc, table, state: State, j: int):
        acc.append(Rule(state.name, state.production))
        k = len(state.production) - 1
        c = j
        while k >= 0:
            Xk = state.production[k]
            if not isinstance(Xk, Rule):
                k -= 1
                c -= 1
            else:
                Ic = table[c]
                # founding the state for Nonterminal Xk
                searchstate = None
                searchflag = False
                for st in Ic:
                    if searchflag:
                        break
                    if st.completed() and st.name == Xk.name:
                        r = st.start_column.index
                        Ir = table[r]
                        # founding the previous state of Nonterminal Xk
                        for prevst in Ir:
                            if state.production == prevst.production and prevst.dot_index == k and state.name == prevst.name \
                                    and state.start_column == prevst.start_column:
                                searchstate = st
                                searchflag = True
                                break
                self.sub_parsing(acc, table, searchstate, c)
                k -= 1
                c = r
        return acc

    def lextableToString(self, lextable):
        '''return a special format string for earley alghoritm from lexical table'''
        res = ""
        for i in lextable:
            if i.type == Token.TYPETOKEN[0] or i.type == Token.TYPETOKEN[3] or i.type == Token.TYPETOKEN[5]:
                for j in i.name:
                    res += ' ' + j
            else:
                res += ' ' + i.name
        return res

    def toTree(self, rules):
        return SyntacticalTree(rules)
