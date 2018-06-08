#!/usr/bin/env python
# -*- coding:utf-8 -*-


import pymysql, os, configparser
from whoosh.index import create_in
from jieba.analyse import ChineseAnalyzer
from decimal import Decimal
from whoosh.fields import Schema, TEXT, ID
from common.mySeacher.myWhoosh.addIndex import incremental_index

analyzer = ChineseAnalyzer()

"""
    创建索引文件系统
"""


def CreateIndexFilesPattern(indexname, schema, indexdir, columnName, uniqueValue):
    """
        注意， 如果更新数据，在创建和添加的时候， 某个字段必须唯一， 才OK， 同是在更新的时候， 也要有那个唯一字段
        :param columnName: 是给Schema用的， 数据是数据库的字段， 只是列的字段名
        :param indexname: 这里的indexname  ==》 当分类搜索的时候就是根据这个indexname来的, 通常用库名， 但不能有下划线等字符
        :param schema: # 初始空字符， 然后进来拼接
        :param indexdir: 索引目录
        :return:
        """
    # keys = {"ID": "abc", "content": "撸啊撸啊德玛西亚"}  # 表示从数据库得到的模拟数据

    """
        # ID(stored=True, unique=True)
        unique:  的作用表示唯一值， 由于update的原因， 所以这里某个值要求唯一，否则将会出现两条数据 
    """
    s = "Schema("
    for key in columnName:
        if key == uniqueValue:
            s += key.replace('\n', '').replace('/r', '').replace('\t', '').replace(' ',
                                                                                   '') + '=ID(stored=True, unique=True), '
        else:
            s += key.replace('\n', '').replace('/r', '').replace('\t', '').replace(' ',
                                                                                   '') + '=TEXT(stored=True, analyzer=analyzer), '
            # TEXT(stored=True, analyzer=analyzer) 其实就是结合分词了

    s = s.rstrip(", ")
    s += ")"
    # print(s) # Schema(ID=TEXT(stored=True, analyzer=analyzer), content=TEXT(stored=True, analyzer=analyzer))
    schema = eval(s)
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)

    create_in(indexdir, schema=schema, indexname=indexname)  # from whoosh.index import create_in 创建索引文件


def parse_db(indexname, schema, indexdir, columnName, rowData):
    """
    注意， 如果更新数据，在创建和添加的时候， 某个字段必须唯一， 才OK， 同是在更新的时候， 也要有那个唯一字段
    :param columnName: 是给Schema用的， 数据是数据库的字段， 只是列的字段名
    :param indexname: 这里的indexname  ==》 当分类搜索的时候就是根据这个indexname来的, 通常用库名， 但不能有下划线等字符
    :param schema: # 初始空字符， 然后进来拼接
    :param indexdir: 索引目录
    :return:
    """
    # keys = {"ID": "abc", "content": "撸啊撸啊德玛西亚"}  # 表示从数据库得到的模拟数据
    s = "Schema("
    for key in columnName:
        if key == "LogID":
            s += key.replace('\n', '').replace('/r', '').replace('\t', '').replace(' ',
                                                                                   '') + '=ID(stored=True, unique=True), '
        else:
            s += key.replace('\n', '').replace('/r', '').replace('\t', '').replace(' ',
                                                                                   '') + '=TEXT(stored=True, analyzer=analyzer), '
            # TEXT(stored=True, analyzer=analyzer) 其实就是结合分词了

    s = s.rstrip(", ")
    s += ")"
    # print(s) # Schema(ID=TEXT(stored=True, analyzer=analyzer), content=TEXT(stored=True, analyzer=analyzer))
    schema = eval(s)
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)

    ix = create_in(indexdir, schema=schema, indexname=indexname)  # from whoosh.index import create_in 创建索引文件

    writer = ix.writer()  # 写入变成索引文件

    docline = """writer.add_document("""
    for key in rowData:
        val = rowData[key]

        if not val:
            val = ""
        elif isinstance(val, (Decimal,)):
            val = str(val)

        else:
            val = pymysql.escape_string(str(val))
        docline += key + '="' + val + '", '
    docline = docline.rstrip(", ")
    docline += """)"""
    # print(docline) # writer.add_document(content="撸啊撸啊德玛西亚", ID="abc")
    exec(docline)
    writer.commit()


def escape(s, obj="’"):
    ret = ''
    for x in s:
        if x == obj:
            ret += '\\'
        ret += x
    return ret


def app():
    from common.Base import MyPymysql, Config
    # notdbMysql = Config().get_content('notdbMysql')
    """
        获取一个表的每个字段
        
    """
    tableNameList = ["logProject", "logQuest"]
    dataBaseList = ["db_metadata", "db_metadata"]
    uniqueValueList = ["logProjectID", "logQuestID"]
    for i in range(len(tableNameList)):
        tableName = tableNameList[i]
        dataBase = dataBaseList[i]
        uniqueValue = uniqueValueList[i]
        columnName = []
        sql = "select COLUMN_NAME as columnName from information_schema.COLUMNS where table_name = '{}' and table_schema = '{}';".format(
            tableName,
            dataBase)
        dataSql = "select * from {}.{}".format(dataBase, tableName)
        ret = MyPymysql('notdbMysql')
        columnNameData = ret.selectall_sql(sql)
        data = ret.selectall_sql(dataSql)
        ret.close()
        for i in columnNameData:
            columnName.append(i["columnName"])

        print(columnName)

        indexDirectory = "indexdir"
        if not os.path.exists(indexDirectory):
            os.makedirs(indexDirectory)
        dbname = tableName
        CreateIndexFilesPattern(indexname=dbname, schema="", indexdir=indexDirectory, columnName=columnName,
                                uniqueValue=uniqueValue)
        for rowData in data:
            incremental_index(indexdir=indexDirectory, indexname=dbname, rowData=rowData)
            """
                下面这样写有问题， 原博文里面的问题， 应该把所有数据放进去， 然后循环write（）...， 而不是连Schema也循环
            """
            # parse_db(indexname=dbname, schema="", indexdir=indexDirectory, columnName=columnName, rowData=rowData)


if __name__ == '__main__':
    app()
