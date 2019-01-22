#coding: utf-8
from XlsParser import XlsParser

class Xls2PyParser(XlsParser):
    def __init__(self,sheet,cfg={}):
        indent = cfg.get("indent",4 * " ")
        colfmt = indent * 2 + '"%s" : %%(%s)s'
        tmp = []
        for col in range(0,sheet.max_col):
            tag = sheet.col2tag[col]
            if not tag:
                continue
            tmp.append(colfmt % (tag,tag))
        map_id = cfg.get("map_id")
        if not map_id:
            line_start = indent + "{\n"
        else:
            line_start = indent + "%%(%s)s : {\n" % (map_id)
        line_end = "\n" + indent + "}"
        linefmt = line_start + ",\n".join(tmp) + line_end
        cfg["linefmt"] = linefmt
        XlsParser.__init__(self,sheet,cfg)

    def line(self,row):
        line = XlsParser.line(self,row)
        for col_name in line.keys():
            v = line[col_name]
            col = self.sheet.tag2col[col_name]
            typename = self.sheet.col2type[col]
            if typename == "string":
                line[col_name] = repr(v)
        return line

    def parse(self):
        lines = self.lines()
        data = "{\n" + ",\n".join(lines) + "\n}"
        varname = self.cfg.get("varname")
        if varname:
            data = varname + " = " + data
        if self.cfg.get("comment"):
            data = "# " + self.desc() + "\n" + data
        return data
