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
            #' public class F o r m u l a 2 { public static void main ( String[] args ) { int a = 0 , b = 2 0 , c = 4 0 , d = 6 0 , e = 8 0 , f = 1 0 0 , g = 2 , h = 4 ; a = b + c ; a = e - d ; a = f / b ; a = d % c ; } }'
            earlyres = synanalyzer.earley(rule=synanalyzer.PROGRAMM, text=textnow)
            tree = synanalyzer.right_parsing(earlyres)
            print(tree)
    else:
        lexer.skan(indata)
