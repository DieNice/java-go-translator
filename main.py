from translator.io.filereader import FileReader
from translator.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer

if __name__ == '__main__':
    lexer = LexicalAnalyzer()
    reader = FileReader()
    indata = reader.read()
    if type(indata) is list:
        for i in indata:
            res = lexer.skan(i)
            print('file: {},data {}'.format(i[0], res[0]))
    else:
        lexer.skan(indata)
