import re
import sys

from .env import Env
from .lexicaltable import LexicalTable
from .tok import Token


class LexicalAnalyzer:
    '''returns table of lexems'''
    VALIDCHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+_-[]'\",;-%/*~<>&^|!.=(){} \n"
    '''Strict order'''
    token_exprs = [
        (r"[\n\s]+", None),
        (r'\(', Token.TYPETOKEN[6]),
        (r'\)', Token.TYPETOKEN[6]),
        (r'\}', Token.TYPETOKEN[6]),
        (r'\{', Token.TYPETOKEN[6]),
        (r'\;', Token.TYPETOKEN[6]),
        (r'\"[A-Za-z][A-Za-z0-9_ ]*\"', Token.TYPETOKEN[5]),
        (r'\'', Token.TYPETOKEN[6]),
        (r'\,', Token.TYPETOKEN[6]),
        (r'\"', Token.TYPETOKEN[6]),
        (r'\:', Token.TYPETOKEN[6]),
        (r'\+\+', Token.TYPETOKEN[4]),
        (r'\+', Token.TYPETOKEN[4]),
        (r'\-\-', Token.TYPETOKEN[4]),
        (r'\-', Token.TYPETOKEN[4]),
        (r'\*', Token.TYPETOKEN[4]),
        (r'\/', Token.TYPETOKEN[4]),
        (r'\>\=', Token.TYPETOKEN[4]),
        (r'\>', Token.TYPETOKEN[4]),
        (r'\<\=', Token.TYPETOKEN[4]),
        (r'\<', Token.TYPETOKEN[4]),
        (r'\!\= ', Token.TYPETOKEN[4]),
        (r'\!', Token.TYPETOKEN[4]),
        (r'\==', Token.TYPETOKEN[4]),
        (r'\=', Token.TYPETOKEN[4]),
        (r'\%', Token.TYPETOKEN[4]),
        (r'\&\&', Token.TYPETOKEN[4]),
        (r'\|\|', Token.TYPETOKEN[4]),
        (r'break', Token.TYPETOKEN[2]),
        (r'class', Token.TYPETOKEN[2]),
        (r'continue', Token.TYPETOKEN[2]),
        (r'double', Token.TYPETOKEN[1]),
        (r'do', Token.TYPETOKEN[2]),
        (r'for', Token.TYPETOKEN[2]),
        (r'static', Token.TYPETOKEN[2]),
        (r'void', Token.TYPETOKEN[2]),
        (r'while', Token.TYPETOKEN[2]),
        (r'main', Token.TYPETOKEN[2]),
        (r'public', Token.TYPETOKEN[2]),
        (r'String\[\]', Token.TYPETOKEN[2]),
        (r'String', Token.TYPETOKEN[2]),
        (r'args', Token.TYPETOKEN[2]),
        (r'boolean', Token.TYPETOKEN[1]),
        (r'byte', Token.TYPETOKEN[1]),
        (r'char', Token.TYPETOKEN[1]),
        (r'float', Token.TYPETOKEN[1]),
        (r'int', Token.TYPETOKEN[1]),
        (r'long', Token.TYPETOKEN[1]),
        (r'short', Token.TYPETOKEN[1]),
        (r'Math\.log', Token.TYPETOKEN[1]),
        (r'Math\.pow', Token.TYPETOKEN[1]),
        (r'Math\.sqrt', Token.TYPETOKEN[1]),
        (r'System\.out\.println', Token.TYPETOKEN[1]),
        (r'System\.out\.print', Token.TYPETOKEN[1]),
        (r'true', Token.TYPETOKEN[1]),
        (r'false', Token.TYPETOKEN[1]),
        (r'(\d+(.\d+)?)', Token.TYPETOKEN[3]),
        (r'[A-Za-z_][A-Za-z0-9_]*', Token.TYPETOKEN[0]),
    ]

    def check(self, str):
        '''checks the entire string for the validity of characters'''
        checklist = []
        for i in str:
            if i not in self.VALIDCHARS:
                checklist.append(i)
        return checklist

    def deletecomments(self, instr):
        '''delete all comments from string '''
        res = re.sub(r'\s+//[\w\s]+\n', '', instr)
        res = re.sub(r'\s+/\*[\w\s]+\*/\n', '', res)
        return res

    def skan(self, indata):
        '''Parses text into tokens, forms a tree of name tables and returns a table of tokens'''
        lextable = LexicalTable()
        env = Env()
        namefile = indata[0]
        filedata = indata[1]
        checkdata = self.check(filedata)
        ptr = env.root
        if checkdata:
            return print("Invalid chars {0} in program {1}".format(checkdata, namefile))
        else:
            characters = self.deletecomments(filedata)
            pos = 0
            while pos < len(characters):
                match = None
                for token_expr in self.token_exprs:
                    pattern, tag = token_expr
                    regex = re.compile(pattern)
                    match = regex.match(str(characters), pos)
                    if match:
                        text = match.group(0)
                        if tag:
                            if text == '{':
                                ptr = env.insertnewscope(ptr)
                            if text == '}':
                                ptr = ptr.prev
                            token = Token(text, tag)
                            lextable.append(token)
                            if tag == Token.TYPETOKEN[0] and ptr is not None:
                                ptr.addid(token.name, token.type)
                        break
                if not match:
                    sys.stderr.write('Illegal character \'{}\',{}: %s\n'.format(namefile, pos) % characters[pos])
                    sys.exit(1)
                else:
                    pos = match.end(0)
            return [lextable, env]
