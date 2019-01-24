#coding: utf-8
from XlsParser import XlsParser
import json

class Xls2JsonParser(XlsParser):
    def lines(self):
        startrow = self.sheet.startrow
        lines = []
        for row in xrange(startrow,self.sheet.max_row):
            line = self.sheet.line(row)
            lines.append(line)
        return lines

    def parse(self):
        lines = self.lines()
        indent = self.cfg.get("indent")
        id = self.cfg.get("id")
        if not id:
            return json.dumps(lines,indent=indent)
        else:
            dct = {}
            for line in lines:
                id_value = line[id]
                dct[id_value] = line
            return json.dumps(dct,indent=indent)
