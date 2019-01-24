#coding: utf-8
import sys
import optparse
from pyExcelerator import *
from XlsParser import *

def main():
    usage = \
"""usage: python %prog [options]
e.g:
    python %prog --config=config
    python %prog --config=config --limit=test.xls,nest_test.xls"""
    parser = optparse.OptionParser(usage=usage,version="%prog 0.0.1")
    parser.add_option("-c","--config",help="[required] python config file")
    parser.add_option("-l","--limit",help="[optional] qualify which xls need to export data,default is no limit")
    options,args = parser.parse_args()
    required = ["config"]
    for r in required:
        if options.__dict__.get(r) is None:
            parser.error("option '%s' required" % r)
    config = options.config
    limit = options.limit
    if limit:
        limit = string.split(limit,",")
    mod = __import__(config)
    if hasattr(mod,"parser_package"):
        parser_package = getattr(mod,"parser_package")
        if parser_package is not None:
            exec("from " + parser_package + " import *")
    export = mod.export

    for task in export:
        xls_filename = task["xls_filename"]
        if limit and not xls_filename in limit:
            print(readable("ignore %s" % (xls_filename)))
            continue
        sheet_list = parse_xls(xls_filename.decode("utf-8"))
        sheets = {}
        for sheet_name,sheet_data in sheet_list:
            sheets[sheet_name] = sheet_data
        for cfg in task["sheets"]:
            sheet_name = cfg["sheet_name"]
            sheet_data = sheets.get(sheet_name.decode("utf-8"))
            if not sheet_data:
                print(readable("no parser %s#%s" % (xls_filename,sheet_name)))
                continue
            print(readable("parser %s#%s ..." % (xls_filename,sheet_name)))
            cfg["xls_filename"] = xls_filename
            cfg["sheet_name"] = sheet_name
            sheet = Sheet(sheet_data,cfg)
            ParserClass = eval(cfg["parser"])
            parser = ParserClass(sheet,cfg)
            data = parser.parse()
            if cfg.get("filename"):
                parser.write(cfg.get("filename"),data)
            print(readable("parser %s#%s ok" % (xls_filename,sheet_name)))

if __name__ == "__main__":
    main()
