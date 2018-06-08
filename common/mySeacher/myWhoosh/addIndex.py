#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os.path
from whoosh.filedb.filestore import FileStorage
from whoosh.index import FileIndex
from whoosh.writing import AsyncWriter
from decimal import Decimal
import pymysql

"""
    添加索引数据
"""


def incremental_index(indexdir, indexname, rowData):
    """
    注意这里，　每次增加索引都会产生一个新的ｓｅｇ文件，　会占用空间，　所以这里需要注意
    :param rowData: 每一行的数据
    :param indexdir:
    :param indexname:
    :return:
    """
    # print(indexdir)

    storage = FileStorage(indexdir)
    ix = FileIndex(storage, indexname=indexname)

    writer = AsyncWriter(ix)
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
    exec(docline)
    # print(docline) # writer.add_document(content="撸啊撸啊德玛西亚", ID="abc")
    # writer.add_document(content="人在塔在", ID="hik")

    writer.commit()


if __name__ == '__main__':
    indexname = "test"
    indexdir = "indexdir"
    incremental_index(indexdir, indexname, {})
