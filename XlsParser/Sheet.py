#coding:utf-8
import os
import sys
import string
import traceback
import json
from checktype import checktype

def readable(msg):
    if sys.platform == "win32":
        msg = msg.decode("utf-8").encode("gbk")
    return msg

class Sheet(object):
    AnyRow = -1
    AnyCol = -1
    def __init__(self,values,cfg):
        self.xls_filename = cfg.get("xls_filename")
        self.name = cfg.get("sheet_name")
        # default:  0--titlerow 1--tagrow 2--typerow 3--startrow
        self.tagrow = cfg.get("tagrow",1)
        self.typerow = cfg.get("typerow",2)
        self.startrow = cfg.get("startrow",3)
        self.values = values
        self.tag2col = {}
        self.col2tag = {}
        self.col2type = {}
        self.cell_parsers = {}
        row_cols = self.values.keys()
        self.max_row = sorted(row_cols)[-1][0] + 1
        self.max_col = sorted((col,row) for row,col in iter(row_cols))[-1][0] + 1
        col = 0
        while col < self.max_col:
            if (self.tagrow,col) in self.values:
                v = self.values[(self.tagrow,col)]
                ok,v = checktype(v,"string")
                assert ok,v
                self.tag2col[v] = col
                self.col2tag[col] = v
            if (self.typerow,col) in self.values:
                v = self.values[(self.typerow,col)]
                ok,v = checktype(v,"string")
                assert ok,v
                self.col2type[col] = v
            col += 1
        #print("Sheet.__init__",self.tagrow,self.tag2col,self.col2tag,self.max_row,self.max_col)

    def message(self,row,col,msg):
        return readable("sheet=%s#%s,row=%d,col=%d: %s" % (self.xls_filename,self.name,row+1,col+1,msg))

    def value(self,row,col):
        if type(col) == str:
            col = self.tag2col[col]
        typename = self.col2type[col]
        val = self.values.get((row,col),None)
        ok,val = checktype(val,typename)
        if not ok:
            raise Exception(self.message(row,col,val))
        parser = self.get_parser(row, col)
        if parser:
            try:
                val = parser(val)
            except Exception as e:
                raise Exception(self.message(row,col,e.message))
        return val

    def line(self,row):
        ret = {}
        for col in range(0,self.max_col):
            if col in self.col2tag:
                ret[self.col2tag[col]] = self.value(row,col)
        return ret

    def register_parser(self,row,col,func):
        if type(col) == str:
            col = self.tag2col[col]
        if not self.cell_parsers.get(row,None):
            self.cell_parsers[row] = {}
        self.cell_parsers[row][col] = func

    def get_parser(self,row,col):
        row_funcs = self.cell_parsers.get(row,None)
        if not row_funcs:
            row_funcs = self.cell_parsers.get(Sheet.AnyRow,None)
        if not row_funcs:
            return None
        func = row_funcs.get(col,None)
        if not func:
            func = row_funcs.get(Sheet.AnyCol,None)
        return func
