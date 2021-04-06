from translator.io.filereader import FileReader
from translator.io.filewriter import FileWriter
from translator.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from translator.syntacticalanalyzer.recognizer.syntacticalanalyzer import SyntacticalAnalyzer
from translator.syntacticalanalyzer.semanticanalyzer.syntacticstructure import SyntacticsStructure
from translator.codegenerator.codegenerator import CodeGenerator

if __name__ == '__main__':
    lexer = LexicalAnalyzer()
    synanalyzer = SyntacticalAnalyzer()
    codegenerator = CodeGenerator()
    reader = FileReader()
    indata = reader.read(namepattern="Formula3")  # [^E].*
    outdata = []
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
            textprogram = codegenerator.translate(ast.root)
            print(textprogram)
            outdata.append((i[0], textprogram))
        except:
            print('error in file: {}'.format(i[0]))
        writer = FileWriter()
        writer.write(outdata)
