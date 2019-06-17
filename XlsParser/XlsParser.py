#coding: utf-8
import os
import sys
import string
import traceback
import json

class XlsParser(object):
    def __init__(self,sheet,cfg={}):
        self.sheet = sheet
        self.cfg = cfg

    def linefmt(self,linefmt,line,row):
        import re
        # extract fmt "%[(name)][flags][width].[precision]typecode" to %(name)fmt => (name,fmt)
        pat = "%\(([^()]+)\)([-+0]?[1-9]?[.]?[1-9]?[fdsr])"
        lst = re.findall(pat,linefmt)
        s1 = set([v[0] for v in lst])
        s2 = set(line.keys())
        s = s1 - s2
        #print("linefmt",lst)
        if s:
            errmsg = self.sheet.message(row,-1,"unknow format: %s" % s)
            raise Exception(errmsg)
        try:
            aline = linefmt % line
        except Exception as e:
            errmsg = self.sheet.message(row,-1,e.message + "\n" + str(line))
            raise Exception(errmsg)
        return aline

    def line(self,row):
        return self.sheet.line(row)

    def lines(self):
        linefmt = self.cfg.get("linefmt","%s")
        startrow = self.sheet.startrow
        lines = []
        for row in xrange(startrow,self.sheet.max_row):
            line = self.line(row)
            line = self.linefmt(linefmt,line,row)
            lines.append(line)
        return lines

    def parse(self):
        lines = self.lines()
        return "{\n" + ",\n".join(lines) + "\n}"

    def _write(self,filename,data):
        parent_dir = os.path.dirname(filename)
        #print("parent_dir:",parent_dir)
        if parent_dir != "" and not os.path.isdir(parent_dir):
            os.makedirs(parent_dir)
        fd = open(filename,"wb")
        fd.write(data)
        fd.close()

    def write(self,filename,data):
        data = data.strip("\r\n")
        startline = self.cfg.get("startline")
        endline = self.cfg.get("endline")
        if not (startline and endline):
            self._write(filename,data)
            return
        strip_startline = startline.strip()
        strip_endline = endline.strip()
        try:
            fd = open(filename,"rb")
            lines = fd.readlines()
            fd.close()
        except Exception as e:
            # file not exist?
            lines = []
        start_lineno = end_lineno = -1
        old_data = "".join(lines)
        if lines:
            for lineno,line in enumerate(lines):
                line = line.strip()
                if start_lineno == -1 and strip_startline == line:
                    start_lineno = lineno
                elif strip_endline == line:
                    end_lineno = lineno
                    #print(start_lineno,end_lineno)
                    assert(start_lineno != -1 and end_lineno > start_lineno)
                    break
            if start_lineno == -1 or end_lineno == -1:
                print("ignore filename %r" % filename)
                return False
            data = "".join(lines[:start_lineno+1]).rstrip("\r\n") + "\n" + data +"\n" + "".join(lines[end_lineno:])
        else:
            data = startline + "\n" + data + "\n" + endline
        if old_data != data:
            self._write(filename,data)
        return True

    def desc(self):
        lst = traceback.extract_stack(limit=3)
        lst = lst[1]
        filename,lineno,func_name = lst[0],lst[1],lst[2]
        filename = os.path.split(filename)[-1]
        msg = "sheet: %s#%s parser: %s:%s:%s" % (self.sheet.xls_filename,self.sheet.name,filename,lineno,func_name)
        return msg
