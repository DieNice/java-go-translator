import os
import re
from typing import Tuple, List


class FileWriter:
    def write(self, outdata: List[Tuple[str, str]], pathdir=os.getcwd() + "/tests/out/"):
        '''The method write all files to a directory "pathdir"'''
        pathdir = os.path.abspath(pathdir)
        if not os.path.isdir(pathdir):
            os.mkdir(pathdir)
        for i in outdata:
            self.__writefile(pathdir + '/' + i[0].replace('java', 'go'), i[1])

    def __writefile(self, filepath: str, data: str):
        fin = open(filepath, 'w')
        fin.write(data)
