#!/usr/bin/env python
# -*- coding:utf-8 -*-
from whoosh.filedb.filestore import FileStorage
from whoosh.index import exists_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser


def search(indices, inpval=1):
    qparsers = []

    if inpval == 1:
        categories = []
        # 注意这里有问题，　当增量索引文档的时候，　容易出现重复，　那么数据也会重复，　尼玛原点文档就在ａｐｐ函数里
        for ix in indices:  # ix: FileIndex(FileStorage('indexdir'), 'superfamicom.db')
            cat = list(ix.schema._fields.keys())
            # ix.schema:  <Schema: ['Developer', 'Publisher', 'ReleaseDate', 'Title']>
            # ix.schema._fields {'ReleaseDate': TEXT(format=Positions(boost=1.0), scorable=True, stored=True, unique=None),....

            # cat:  ['Developer', 'ReleaseDate', 'Publisher', 'Title']
            print("cat:", cat)
            for val in cat:
                if val in categories:
                    val = val + " - " + ix.indexname  # 如果有重复的， 假设得以区分

                categories.append(val)

        print("categories", categories)

        # ----------------->以上是得到categories【】， 实际是为了区分每个表的字段是否重复并都放都一个list

        s = "如果为1的话，是按类别选择， 选择按照那种分类: \n"

        # print(categories)
        inpval = 0
        # indices:
        # [FileIndex(FileStorage('indexdir'), 'dinosaur.db'), FileIndex(FileStorage('indexdir'), 'mmorpg.db'), FileIndex(FileStorage('indexdir'), 'superfamicom.db')]

        for i in range(0, len(categories)):  # go through all catergories giving options
            s += "\t" + str(i) + " to search in [" + categories[i] + "]  \n"
        s += "--->: "

        inpval = int(input(s))  # 输入从哪项进行查询

        for i in range(0, len(indices)):
            qparsers.append(QueryParser(categories[inpval], indices[i].schema))





            # results 为结果

    else:
        print("全文索引")
        categories = []
        for ix in indices:  # to be able to search through all the keys
            categories.extend(list(ix.schema._fields.keys()))
            qparsers.append(MultifieldParser(categories,
                                             ix.schema))  # let user search through multiple fields with multifield parser

    print("你要查询的内容:")
    inp = input("--->")

    data = inp.split('<==>')
    queries = [qparsers[i].parse(data[0].strip()) for i in range(0, len(qparsers))]
    if len(data) > 1:
        limits = int(data[1].strip())
        limits = 10

    # limits 为显示结果的数量
    results = []
    stats = {}

    for i in range(0, len(indices)):
        # indices: [FileIndex(FileStorage('indexdir'), 'dinosaur.db'),
        searcher = indices[i].searcher()
        res = searcher.search(queries[i], limit=50)

        if len(res) != 0:
            # ix.indexname--> superfamicom.db
            stats[indices[i].indexname] = len(res)
        else:
            continue
        results.extend(res)

    my_result = []
    for i in results:
        my_result.append(dict(i))

    print(my_result)


def test():
    # encoding=utf-8
    import jieba

    seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
    print(seg_list)
    print("Full Mode: " + "/ ".join(seg_list))  # 全模式

    seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
    print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

    seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
    print(", ".join(seg_list))

    seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    print(", ".join(seg_list))


def app():
    indexdir = "indexdir"
    storage = FileStorage(indexdir)
    """
    ['dinosaur.db_loh0qsax01wwdijy.seg', 'dinosaur.db_WRITELOCK', 'mmorpg.db_1mwe4pojwea459cm.seg', 'mmorpg.db_WRITELOCK',]
    """
    fname = storage.list()
    print(fname)
    """
    [
        FileIndex(FileStorage('indexdir'), 'dinosaur.db'), 
        FileIndex(FileStorage('indexdir'), 'mmorpg.db'), 
        FileIndex(FileStorage('indexdir'), 'superfamicom.db')
    ]  
    """
    indices = []

    """
        测试
    """
    indList = ["logProject", "logQuest"]
    for ind in indList:
        indices.append(open_dir(indexdir, ind))

    """
        ===========下面这么写是重复的===============
            因为这样是拿的文件的部分，作为ind， 会出现重复， 应该用set
            或者，就直接用indexName也可以
    """

    # for f in fname:
    #     if not f.endswith(".seg"):
    #         continue
    #     ind = f.split('_')[0]
    #     print(ind)
    #
    #     if exists_in(indexdir, indexname=ind):
    #         indices.append(open_dir(indexdir, ind))

    search(indices, 2)


if __name__ == '__main__':
    app()
