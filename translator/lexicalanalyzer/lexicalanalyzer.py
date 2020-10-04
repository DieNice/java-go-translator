from .lexicaltable import LexicalTable
from .idtable import IdTable
import re


class LexicalAnalyzer:
    '''returns table of lexems'''
    TABLEKEYWORDS = {
        'break': 'К1',
        'class': 'К2',
        'const': 'К3',
        'continue': 'К4',
        'do': 'К5',
        'else': 'К6',
        'for': 'К7',
        'goto': 'К8',
        'if': 'К9',
        'static': 'К10',
        'void': 'К11',
        'while': 'К12',
        'public': 'К13',
        'return': 'К14',
    }
    TABLERESERVEDNAMES = {
        'boolean': 'R1',
        'byte': 'R2',
        'char': 'R3',
        'double': 'R4',
        'float': 'R5',
        'int': 'R6',
        'long': 'R7',
        'short': 'R8',
        'min': 'R9',
        'log': 'R10',
        'pow': 'R11',
        'sqrt': 'R12',
        'time': 'R13',
        'System.out.println': 'R14',
        'True': 'R15',
        'False': 'R16',
    }
    DELIMETERS = "()[]{}'\",;?:.+-*/%|&^~=!?><,; "
    VALIDCHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+_-[]'\",;-%/*~<>&^|!.=(){} \n"

    def check(self, str):
        checklist = []
        for i in str:
            if i not in self.VALIDCHARS:
                checklist.append(i)
        return checklist

    def deletecomments(self, instr):
        res = re.sub(r'\s+//[\w\s]+\n', '', instr)
        res = re.sub(r'\s+/\*[\w\s]+\*/\n', '', res)
        return res

    def skan(self, instr):
        lextable = LexicalTable()
        namefile = instr[0]
        filedata = instr[1]
        checkdata = self.check(filedata)
        if checkdata:
            return print("Invalid chars {0} in program {1}".format(checkdata, namefile))
        else:
            filedata = self.deletecomments(filedata)
            print(filedata)
            return lextable
