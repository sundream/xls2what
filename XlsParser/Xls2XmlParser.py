#coding: utf-8
from XlsParser import XlsParser
from xml.dom.minidom import Document

class Xls2XmlParser(XlsParser):
    def parse(self):
        indent = self.cfg.get("indent") or 0
        id = self.cfg.get("id")
        varname = self.cfg.get("varname")
        encoding = self.cfg.get("encoding")
        doc = Document()
        startrow = self.sheet.startrow
        root = doc.createElement(varname+"s")
        if id:
            root.setAttribute("id",id)
        for row in xrange(startrow,self.sheet.max_row):
            line = self.sheet.line(row)
            line_elem = doc.createElement(varname)
            for col_name,value in line.iteritems():
                col = self.sheet.tag2col[col_name]
                typename = self.sheet.col2type[col]
                col_elem = self._buildXml(doc,value,col_name)
                col_elem.setAttribute("type",typename)
                line_elem.appendChild(col_elem)
            root.appendChild(line_elem)
        if indent > 0:
            indent = indent * " "
            return root.toprettyxml(indent=indent,encoding=encoding)
        else:
            return root.toprettyxml(encoding=encoding)

    def _buildXml(self,doc,obj,name):
        assert type(name) == str
        if isinstance(obj,dict):
            elem = doc.createElement(name)
            for key,value in obj.iteritems():
                child_elem = self._buildXml(doc,value,str(key))
                elem.appendChild(child_elem)
        elif isinstance(obj,(list,tuple)):
            elem = doc.createElement(name+"s")
            for value in obj:
                child_elem = self._buildXml(doc,value,name)
                elem.appendChild(child_elem)
        else:
            elem = doc.createElement(name)
            child = doc.createTextNode(str(obj))
            elem.appendChild(child)
        return elem
