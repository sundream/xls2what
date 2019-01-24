#coding: utf-8
from XlsParser import XlsParser
from Xls2LuaParser import Xls2LuaParser

class Xls2LuaParser_NestTable(Xls2LuaParser):
    def __init__(self,sheet,cfg={}):
        nest_id = cfg.get("nest_id")
        nest_fields = cfg.get("nest_fields")
        indent = cfg.get("indent",4 * " ")

        colfmt = indent * 2 + "%s = %%(%s)s"
        fmts = []
        nest_fmts = []
        for col in range(0,sheet.max_col):
            if col not in sheet.col2tag:
                continue
            tag = sheet.col2tag[col]
            if tag not in nest_fields:
                if tag != nest_id:
                    fmts.append(colfmt % (tag,tag))
            else:
                nest_fmts.append(indent + colfmt % (tag,tag))
        id = cfg.get("id")
        if not id:
            line_start = indent + "{\n"
        else:
            line_start = indent + "[%%(%s)s] = {\n" % (id)
        line_start = line_start + "%(nestline)s\n"
        line_end = "\n" + indent + "}"
        linefmt = line_start + ",\n".join(fmts) + line_end
        cfg["linefmt"] = linefmt
        if not nest_id:
            nest_line_start = indent * 2 + "{\n"
        else:
            nest_line_start = indent * 2 + "[%%(%s)s] = {\n" % (nest_id)
        nest_line_end = "\n" + indent * 2 + "},"
        nestlinefmt = nest_line_start + ",\n".join(nest_fmts) + nest_line_end
        cfg["nestlinefmt"] = nestlinefmt
        XlsParser.__init__(self,sheet,cfg)

    def lines(self):
        startrow = self.sheet.startrow
        outer_id = self.cfg.get("outer_id")
        nestlinefmt = self.cfg.get("nestlinefmt")
        linefmt = self.cfg.get("linefmt")
        firstline_row = None
        firstline = None
        lastid = None
        lines = []
        nestlines = []
        for row in xrange(startrow,self.sheet.max_row):
            line = self.line(row)
            line2 = self.linefmt(nestlinefmt,line,row)
            if lastid == None or (line[outer_id] != None and lastid != line[outer_id]):
                if firstline != None:
                    nestline = "\n".join(nestlines)
                    firstline["nestline"] = nestline
                    aline = self.linefmt(linefmt,firstline,firstline_row)
                    lines.append(aline)
                    nestlines = []
                    firstline = None
                    firstline_row = None
                lastid = line[outer_id]
                firstline = line
                firstline_row = row
            nestlines.append(line2)

        if firstline != None:
            nestline = "\n".join(nestlines)
            firstline["nestline"] = nestline
            lines.append(self.linefmt(linefmt,firstline,firstline_row))
        return lines
