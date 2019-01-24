#coding: utf-8
# user defined's parser package
#parser_package = "MyParser"
export = [
    {
        "xls_filename" : "xls/test.xls",
        "sheets" : [
            {
                "sheet_name" : "test",
                # output's filename
                "filename" : "gencode/lua/data_test.lua",
                "parser" : "Xls2LuaParser",
                "varname" : "data_test",
                # export a list if you don't set id,otherwise export a dict
                "id" : "id",
                # export data in range (startline,endline)
                "startline" : "-- generate by XlsParser,DO NOT EDIT!!!",
                "endline" : "-- generate by XlsParser,DO NOT EDIT!!!",
                # add comment: where is data source
                "comment" :  True,
            },
            {
                "sheet_name" : "test",
                "filename" : "gencode/py/data_test.py",
                "parser" : "Xls2PyParser",
                "varname" : "data_test",
                "id" : "id",
                "startline" : "# generate by XlsParser,DO NOT EDIT!!!",
                "endline" : "# generate by XlsParser,DO NOT EDIT!!!",
                "comment" :  True,
            },
            {
                "sheet_name" : "test",
                "filename" : "gencode/json/data_test.json",
                "parser" : "Xls2JsonParser",
                "id" : "id",
                # see json.dumps
                "indent" : 4,
            },
            {
                "sheet_name" : "test",
                "filename" : "gencode/xml/data_test.xml",
                "varname" : "data_test",
                "parser" : "Xls2XmlParser",
                "id" : "id",
                "indent" : 4,
            },
        ]
    },
    {
        "xls_filename" : "xls/nest_test.xls",
        "sheets" : [
            {
                "sheet_name" : "test",
                "filename" : "gencode/lua/data_nest_table.lua",
                "parser" : "Xls2LuaParser_NestTable",
                "id" : "id",
                "outer_id" : "id",
                "nest_id" : "nest_id",
                "nest_fields" : {"nest_key1","nest_key2"},
                # test more
                "tag_alias" : {"key1":"key1_alia"},
                "exclude_tags" : {"key2"},
                "comment" :  True,
            },
        ]
    },
]
