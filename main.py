from translator.io.filereader import FileReader
from translator.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from translator.syntacticalanalyzer.recognizer.syntacticalanalyzer import SyntacticalAnalyzer
from translator.syntacticalanalyzer.semanticanalyzer.syntacticstructure import SyntacticsStructure

if __name__ == '__main__':
    lexer = LexicalAnalyzer()
    synanalyzer = SyntacticalAnalyzer()
    reader = FileReader()
    indata = reader.read(namepattern='Cycle2.java') #[^E].*
    if type(indata) is list:
        for i in indata:
            try:
                res = lexer.skan(i)
                print('file: {},data {}'.format(i[0], res[0]))
                res[1].printenv()
                textnow = synanalyzer.lextableToString(res[0])
                earlyres = synanalyzer.earley(rule=synanalyzer.PROGRAMM, text=textnow)
                parselist = synanalyzer.right_parsing(earlyres)
                print(parselist)
                dirtytree = synanalyzer.toTree(parselist)
                dirtytree.printTree()
                ast = SyntacticsStructure(dirtytree)
                ast.printast()
            except:
                print('error in file: {}'.format(i[0]))
    else:
        lexer.skan(indata)
