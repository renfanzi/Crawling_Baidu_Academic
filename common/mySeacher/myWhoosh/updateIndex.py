#!/usr/bin/env python
# -*- coding:utf-8 -*-

from whoosh.filedb.filestore import FileStorage
from whoosh.index import FileIndex
from whoosh.writing import AsyncWriter
from decimal import Decimal
import pymysql



def update_index(indexdir, indexname, rowData):
    """
    注意这里，　每次增加索引都会产生一个新的ｓｅｇ文件，　会占用空间，　所以这里需要注意
    :param indexdir: 索引目录
    :param indexname: 索引名
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

    # 其实就是在创建索引的时候要求唯一， 要不数据重复是追加了
    # Because "path" is marked as unique, calling update_document with path="/a"
    # will delete any existing documents where the "path" field contains "/a".
    # writer.update_document(path=u"/a", content="Replacement for the first document")
    writer.commit()

if __name__ == '__main__':
    indexname = "test"
    indexdir = "indexdir"
    update_index(indexdir, indexname)
