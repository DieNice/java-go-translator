from translator.io.filereader import FileReader
from translator.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from translator.syntacticalanalyzer.syntacticalanalyzer import SyntacticalAnalyzer

if __name__ == '__main__':
    lexer = LexicalAnalyzer()
    synanalyzer = SyntacticalAnalyzer()
    reader = FileReader()
    indata = reader.read()
    if type(indata) is list:
        for i in indata:
            res = lexer.skan(i)
            print('file: {},data {}'.format(i[0], res[0]))
            textnow = synanalyzer.lextableToString(res[0])
            earlyres = synanalyzer.earley(rule=synanalyzer.PROGRAMM, text=textnow)
            tree = synanalyzer.right_parsing(earlyres)
            print(tree)
    else:
        lexer.skan(indata)
