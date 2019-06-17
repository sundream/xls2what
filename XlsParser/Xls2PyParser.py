#coding: utf-8
from XlsParser import XlsParser

class Xls2PyParser(XlsParser):
    def __init__(self,sheet,cfg={}):
        indent = cfg.get("indent",4 * " ")
        colfmt = indent * 2 + '"%s" : %%(%s)s'
        tmp = []
        for col in range(0,sheet.max_col):
            if col not in sheet.col2tag:
                continue
            tag = sheet.col2tag[col]
            tmp.append(colfmt % (tag,tag))
        id = cfg.get("id")
        if not id:
            line_start = indent + "{\n"
        else:
            line_start = indent + "%%(%s)s : {\n" % (id)
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
                if v.find("'") != -1:
                    v = '"' + v + '"'
                elif v.find('"') != -1:
                    v = "'" + v + "'"
                else:
                    v = '"' + v + '"'
                line[col_name] = v
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
