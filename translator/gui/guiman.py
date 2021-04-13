# -*- coding: utf-8 -*-

import sys
import os
from os.path import expanduser

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from MainWindow import Ui_summerizer
from mainwindow import Ui_MainWindow
from translator.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from translator.syntacticalanalyzer.recognizer.syntacticalanalyzer import SyntacticalAnalyzer
from translator.syntacticalanalyzer.semanticanalyzer.syntacticstructure import SyntacticsStructure
from translator.codegenerator.codegenerator import CodeGenerator


class guiMan(QtWidgets.QMainWindow):

    def file_open(self):
        try:
            # warning don't remove [0]
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Text files(*.java)")[0]
            print(fname)
            # fname.endswith('.java') - precaution to guarantee correct file extension
            if fname.endswith('.java'):
            # clear fields in case of input file change
                self.ui.textEdit.clear()
                self.ui.lineEdit.clear()
                self.ui.textEdit_2.clear()
                f = open(fname, 'r')
                with f:
                    data = f.read()
                    self.ui.textEdit.setText(data)
                    self.ui.lineEdit.setText(os.path.basename(fname))
                f.close()
            else:
                raise Exception("insufficient input file extension")
        except:
            self.ui.textEdit_3.append("insufficient input file extension")

    def file_save(self):
        try:
            if self.ui.lineEdit_2.text().endswith('.go'):
                # allows to open directories
                directory = QFileDialog.getExistingDirectory(self, "Open a folder", expanduser("~"), QFileDialog.ShowDirsOnly)
                file = open(directory + '/' + self.ui.lineEdit_2.text(), 'w')
                text = self.ui.textEdit_2.toPlainText()
                file.write(text)
                file.close()
            else:
                raise Exception("insufficient file extension provided")
        except: self.ui.textEdit_3.append("insufficient file extension provided")



    def reader(self):
        file = self.ui.textEdit.toPlainText()
        title = self.ui.lineEdit.text()
        input_data = [(title, file)]
        return input_data

    def translate(self):
        self.ui.progressBar.show()
        self.ui.progressBar.reset()
        inputdata = self.reader()
        lexer = LexicalAnalyzer()
        synanalyzer = SyntacticalAnalyzer()
        codegenerator = CodeGenerator()
        for i in inputdata:
            try:
                if self.ui.textEdit.toPlainText():
                    res = lexer.skan(i)
                    self.ui.progressBar.setValue(10)
                    res[1].printenv()
                    self.ui.progressBar.setValue(20)
                    textnow = synanalyzer.lextableToString(res[0])
                    self.ui.progressBar.setValue(30)
                    earlyres = synanalyzer.earley(rule=synanalyzer.PROGRAMM, text=textnow)
                    self.ui.progressBar.setValue(40)
                    parselist = synanalyzer.right_parsing(earlyres)
                    self.ui.progressBar.setValue(50)
                    dirtytree = synanalyzer.toTree(parselist)
                    self.ui.progressBar.setValue(60)
                    dirtytree.printTree()
                    self.ui.progressBar.setValue(70)
                    ast = SyntacticsStructure(dirtytree)
                    self.ui.progressBar.setValue(80)
                    ast.printast()
                    self.ui.progressBar.setValue(90)
                    textprogram = codegenerator.translate(ast.root)
                    self.ui.progressBar.setValue(100)

                    self.ui.textEdit_2.setText(textprogram)
                    self.ui.lineEdit_2.setEnabled(1)
                    self.ui.lineEdit_2.setText(self.ui.lineEdit.text().replace('java', 'go'))
                    self.ui.pushButton_3.show()
                    self.ui.pushButton_3.setEnabled(1)
                else:
                    raise Exception('no file provided')


            except:
                self.ui.textEdit_3.append('error in file: {}'.format(i[0]))

    def __init__(self):
        super(guiMan, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label_4.setStyleSheet("""font: bold italic;color: #d4f1f4;""")
        self.ui.label_6.setStyleSheet("""font: bold italic;color: #d4f1f4;""")
        self.ui.pushButton_2.setStyleSheet("background-color: #75e6da;"
                                           """font: bold italic;color: black;""")
        self.ui.pushButton_3.setStyleSheet("background-color: #75e6da;"
                                           """font: bold italic;color: black;""")
        self.ui.groupBox.setStyleSheet("""font: bold italic;color: #d4f1f4;""")
        self.ui.label_9.setStyleSheet("""font: bold italic;color: #d4f1f4;""")
        self.ui.centralwidget.setStyleSheet("background-color: #05445e;")
        self.ui.textEdit.setStyleSheet("background-color: white;")
        self.ui.textEdit_2.setStyleSheet("background-color: white;")
        self.ui.textEdit_3.setStyleSheet("background-color: white;")
        self.ui.lineEdit.setStyleSheet("background-color: white;"
                                       """font:  ubuntu;color: black;""")
        self.ui.lineEdit_2.setStyleSheet("background-color: white;"
                                         """font:  ubuntu;color: black;""")
        self.ui.pushButton.setStyleSheet("background-color: #189ab4;")
        self.ui.progressBar.hide()
        self.ui.pushButton_3.hide()
        self.ui.progressBar.reset()
        self.ui.lineEdit.setReadOnly(1)
        self.ui.pushButton_2.setShortcut('Ctrl+O')
        self.ui.pushButton_2.clicked.connect(self.file_open)
        self.ui.pushButton.clicked.connect(self.translate)
        self.ui.pushButton_3.clicked.connect(self.file_save)


def main():
    app = QtWidgets.QApplication([])
    application = guiMan()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
