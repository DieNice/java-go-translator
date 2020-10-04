from translator.io.filereader import FileReader
from translator.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from translator.lexicalanalyzer.lexicaltable import LexicalTable

if __name__ == '__main__':
    lexer = LexicalAnalyzer()
    reader = FileReader()
    indata = reader.read(namepattern=r'Invalid')
    if type(indata) is list:
        for i in indata:
            lexer.skan(i)
    else:
        lexer.skan(indata)
