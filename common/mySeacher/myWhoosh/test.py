#!/usr/bin/env python
# -*- coding:utf-8 -*-


from whoosh.filedb.filestore import FileStorage
from whoosh.index import exists_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from common.Base import Config, MyPymysql







def search(indices, indexflag, clientContent):
    inpval = indexflag
    qparsers = []
    if inpval == 1:
        categories = []
        for ix in indices:
            cat = list(ix.schema._fields.keys())
            for val in cat:
                if val in categories:
                    val = val + " - " + ix.indexname
                categories.append(val)

        for i in range(0, len(indices)):
            # qparsers.append(QueryParser(categories[inpval], indices[i].schema))
            qparsers.append(QueryParser("VarLebel", indices[i].schema))
    else:

        categories = []
        for ix in indices:
            categories.extend(list(ix.schema._fields.keys()))
            qparsers.append(MultifieldParser(categories,
                                             ix.schema))
    inp = clientContent

    data = inp.split('<==>')
    queries = [qparsers[i].parse(data[0].strip()) for i in range(0, len(qparsers))]

    if len(data) > 1:
        limits = int(data[1].strip())
        limits = 10

    results = []
    stats = {}

    for i in range(0, len(indices)):
        searcher = indices[i].searcher()
        res = searcher.search(queries[i], limit=500)
        if len(res) != 0:
            stats[indices[i].indexname] = len(res)
        else:
            continue
        results.extend(res)

    # print(my_result)
    return results



def selectApp(clientContent, quesID=False, indexflag=1):
    myIndexDirFilePath = Config().get_content("indexFilePath")["filepath"]
    my_add_indexdir = "indexdir"
    indexdir = my_add_indexdir
    storage = FileStorage(indexdir)

    fname = storage.list()
    indices = []

    indList = ["logProject"]
    for ind in indList:
        indices.append(open_dir(indexdir, ind))

    ret = search(indices, indexflag, clientContent)
    print(ret)

if __name__ == '__main__':
    # indexflag = 2 # 1是分类索引2是全局索引
    clientContent = "唯一"
    quesID = ""
    # selectApp(clientContent, quesID=quesID)
    res = selectApp(clientContent)
    print(res)
