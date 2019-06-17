# coding: utf-8
# modify from https://github.com/bangbao/py2lua


class Py2Js(object):
    """trans python object to js object
    """
    number_types = (int, float, long)
    bool_types = (bool,)
    string_types = (basestring,)
    table_array_types = (tuple, list)
    table_dict_types = (dict,)

    def __init__(self,tab=4*' ',newline='\n'):
        self.depth = 0
        self.tab = tab
        self.newline = newline

    def encode(self, obj):
        self.depth = 0
        return self._encode(obj)

    def _encode(self, obj):
        if obj is None:
            return 'nil'

        if isinstance(obj, self.bool_types):
            return str(obj).lower()

        if isinstance(obj, self.number_types):
            return str(obj)

        if isinstance(obj, self.string_types):
            if obj.find("'") != -1:
                return '"' + obj + '"'
            elif obj.find('"') != -1:
                return "'" + obj + "'"
            return '"' + obj + '"'
            #return repr(obj)

        if isinstance(obj, self.table_array_types):
            s = []
            s.append("[" + self.newline)
            self.depth += 1
            for el in obj:
                s.append(self.tab * self.depth + self._encode(el) + ',' + self.newline)
            self.depth -= 1
            s.append(self.tab * self.depth + "]")
            return ''.join(s)

        if isinstance(obj, self.table_dict_types):
            s = []
            s.append("{" + self.newline)
            self.depth += 1
            for key, value in obj.iteritems():
                if isinstance(key,self.number_types):
                    s.append(self.tab * self.depth + ('[%s]' % key) + ' = ' + self._encode(value) + ',' + self.newline)
                else:
                    s.append(self.tab * self.depth + ('["%s"]' % key) + ' = ' + self._encode(value) + ',' + self.newline)
            self.depth -= 1
            s.append(self.tab * self.depth + "}")
            return ''.join(s)
