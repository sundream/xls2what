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
        map_id = self.cfg.get("map_id")
        if not map_id:
            return json.dumps(lines,indent=indent)
        else:
            dct = {}
            for line in lines:
                id = line[map_id]
                dct[id] = line
            return json.dumps(dct,indent=indent)
