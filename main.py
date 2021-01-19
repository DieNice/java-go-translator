from translator.io.filereader import FileReader
from translator.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from translator.syntacticalanalyzer.recognizer.syntacticalanalyzer import SyntacticalAnalyzer

if __name__ == '__main__':
    lexer = LexicalAnalyzer()
    synanalyzer = SyntacticalAnalyzer()
    reader = FileReader()
    indata = reader.read()
    if type(indata) is list:
        for i in indata:
            try:
                res = lexer.skan(i)
                print('file: {},data {}'.format(i[0], res[0]))
                textnow = synanalyzer.lextableToString(res[0])
                earlyres = synanalyzer.earley(rule=synanalyzer.PROGRAMM, text=textnow)
                parselist = synanalyzer.right_parsing(earlyres)
                tree = synanalyzer.toTree(parselist.copy())
                print(tree)
            except:
                print('error in file: {}'.format(i[0]))
    else:
        lexer.skan(indata)
