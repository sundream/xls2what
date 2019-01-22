import re

# like as go type
# buildin type: bool/int/float/string/raw
# array: []type
# map: map[key_type]value_type
def checktype(obj,typename):
    typ = type(obj)
    if typ == unicode:
        obj = obj.encode("utf-8")
        typ = type(obj)
    if typename[0:2] == "[]":
        if typ != str and typ != list and typ != tuple:
            return False,"expect type %r,got %r" % (typename,obj)
        if typ == str:
            try:
                py_obj = eval(obj)
                assert type(py_obj) == list
                obj = py_obj
            except Exception as e:
                return False,"expect type %r,got %r" % (typename,obj)
        sub_typename = typename[2:]
        for i in range(0,len(obj)):
            value = obj[i]
            ok,value = checktype(value,sub_typename)
            if not ok:
                return False,"list's item " + value
            obj[i] = value
        return True,obj
    elif typename[0:3] == "map":
        if typ != str and typ != dict:
            return False,"expect type %r,got %r" % (typename,obj)
        if typ == str:
            try:
                py_obj = eval(obj)
                assert type(py_obj) == dict
                obj = py_obj
            except Exception as e:
                return False,"expect type %r,got %r" % (typename,obj)
        sub_typename = typename[3:]
        m = re.match("\[(.+?)\](.+)",sub_typename)
        if not m or m.lastindex < 2:
            return False,"invalid type: %r" % (typename)
        key_type,value_type = m.group(1),m.group(2)
        for key in obj.keys():
            value = obj[key]
            ok,key = checktype(key,key_type)
            if not ok:
                return False,"map's key " + key
            ok,value = checktype(value,value_type)
            if not ok:
                return False,"map's value " + value
            obj[key] = value
        return True,obj
    else:
        # buildin type
        if typename == "bool":
            # 0 means False,1 means True
            if obj != 0 and obj != 1:
                return False,"expect 0 or 1"
            return True,bool(obj)
        if typename == "int":
            if typ == int or (typ == float and int(obj) == obj):
                return True,int(obj)
            return False,"expect type %r,got %r" % (typename,obj)
        if typename == "float":
            if typ != float and typ != int:
                return False,"expect type %r,got %r" % (typename,obj)
            return True,float(obj)
        if typename == "string":
            if typ != str:
                return False,"expect type %r,got %r" % (typename,obj)
            return True,str(obj)
        if typename == "raw":
            return True,obj
    return False,"unknow type: %r" % (typename)
