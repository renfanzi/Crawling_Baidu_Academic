#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
from decimal import Decimal
from common.Base import MyPymysql, MyGuid, my_datetime, my_log


def CreateMetaProj(data):
    sql = "insert into `meta_project` SET ProjectID={}, UserID={}, ProjectName='{}', ProjectOrgan='{}', ProjectSubject='{}', " \
          "SubjectField={}, ProjectLevel={}, ProjectSource={}, FundsSource={}, ProjectSummary='{}', CycleType={}, CycleSpan='{}', " \
          "TeamIntroduction='{}', ProjectPublic={}, ProjectStatus={}, EditUserID={};".format(
        data["ProjectID"],
        data["UserID"],
        data["ProjectName"],
        data["ProjectOrgan"],
        data["ProjectSubject"],
        data["SubjectField"],
        data["ProjectLevel"],
        data["ProjectSource"],
        data["FundsSource"],
        data["ProjectSummary"],
        data["CycleType"],
        int(data["CycleSpan"]),
        data["TeamIntroduction"],
        data["ProjectPublic"],
        data["ProjectStatus"],
        data["EditUserID"])
    # print(sql)
    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()


class MyPagesAndPageDatas():
    """
    from common.util.MyPaging import Pagination

    res = MyPagesAndPageDatas()
    dataCount = res.SelectItemPagesCountModel("2017091710094680349524135490")
    obj = Pagination(dataCount, current_page=52)
    start = obj.start
    end = obj.end
    data = res.SelectItemPagesDataModel(start, end, obj.appear_page)
    print(len(data))

    res.close()
    """

    def __init__(self, libname="notdbMysql"):
        self.libname = libname
        self.res = MyPymysql(self.libname)

    def SelectItemPagesCountModel(self, QuesID):
        selectBaseTableSql = "select DataTableID, DataTableName, DatabaseName from db_metadata.meta_data_table WHERE `QuesID`='{}' AND DataTableStatus=1;".format(
            QuesID)
        self.baseTableData = self.res.selectone_sql(
            selectBaseTableSql)  # {'DataTableName': '', 'DataTableID': '', 'DatabaseName': ''}

        dataSql = """select count(1) as count from {}.{}""".format(self.baseTableData["DatabaseName"],
                                                                   self.baseTableData["DataTableName"])

        result = self.res.selectone_sql(dataSql)
        return result["count"]

    def SelectItemPagesDataModel(self, start, end, appear_page):
        sql = """select `StartTime`, `EndTime`, `NominalTime`, `SpaceName`, `Topic`, `Index`, `DataValue`, `DataDescription` from {}.{} limit {}, {};""".format(
            self.baseTableData["DatabaseName"],
            self.baseTableData["DataTableName"],
            start,
            appear_page)
        result = self.res.selectall_sql(sql)
        return result

    def close(self):
        self.res.close()


class InsertBaiduDataModel():
    def __init__(self, libname="baidu"):
        self.libname = libname
        self.res = MyPymysql(self.libname)

    # 写入文章
    def insert_articles(self, data):
        '''
                CREATE TABLE `article` (
                  `article_id` decimal(40) NOT NULL AUTO_INCREMENT,
                  `academic_title` varchar(1000) DEFAULT NULL,
                  `article_url` varchar(1000) DEFAULT NULL,
                  `article_contents` varchar(1000) DEFAULT NULL,
                  `reference_quantity` int(11) DEFAULT NULL COMMENT '引用量',
                  `reference_url` varchar(1000) DEFAULT NULL COMMENT '引用url',
                  `publications` varchar(255) DEFAULT NULL COMMENT '发表刊物',
                  `publications_url` varchar(255) DEFAULT NULL,
                  `create_time` varchar(30) DEFAULT NULL,
                  PRIMARY KEY (`article_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        # 先去查md5值存在不存在
        select_md5_sql = \
            """
             SELECT
                *
            FROM
                article
            WHERE
                 FIND_IN_SET("{}",article_md5)   
            """.format(data["article_md5"])
        # print(select_md5_sql)
        ret = self.res.selectall_sql(select_md5_sql)
        # print("len(ret): ", len(ret))
        flag = 0
        if len(ret) == 0:
            insert_article_sql = \
                """
                INSERT INTO article
                SET article_id = {article_id},
                    academic_title = "%s",
                    article_url = "%s",
                    article_contents = "%s",
                    reference_quantity = {reference_quantity},
                    reference_url = "%s",
                    publications = "%s",
                    publications_url = "%s",
                    create_time = "{create_time}",
                    article_md5 = "{article_md5}";
                """.format(**data)
            value = (
                data["academic_title"],
                data["article_url"],
                data["article_contents"],
                data["reference_url"],
                data["publications"],
                data["publications_url"],
            )
            # print(insert_article_sql)
            self.res.insert_sql(insert_article_sql, value=value)
        else:
            flag = 1
        return flag

    # 写入作者信息
    def insert_authors(self, data):
        '''
        CREATE TABLE `authors` (
          `author_id` decimal(11) NOT NULL,
          `article_id` decimal(40,0) NOT NULL,
          `author` varchar(255) DEFAULT NULL,
          `author_url` varchar(1000) DEFAULT NULL,
          `author_mechanism` varchar(255) DEFAULT NULL,
          `author_maybe_mechanism` varchar(1000) DEFAULT NULL,
          PRIMARY KEY (`author_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        insert_author_sql = \
            """
            INSERT INTO `authors`
            SET author_id = {author_id},
                article_id = {article_id},
                author = "%s",
                author_url = "%s",
                author_mechanism = "%s",
                author_maybe_mechanism = "%s";
            """.format(**data)

        value = (
            data["author"],
            data["author_url"],
            data["author_mechanism"],
            data["author_maybe_mechanism"],
        )
        self.res.insert_sql(insert_author_sql, value=value)

    # 写入标签信息
    def insert_tag(self, data):
        """
        CREATE TABLE `tag` (
          `tag_id` decimal(40,0) NOT NULL,
          `article_id` decimal(40,0) NOT NULL,
          `tag` varchar(255) DEFAULT NULL,
          `tag_url` varchar(1000) DEFAULT NULL,
          PRIMARY KEY (`tag_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
        insert_author_sql = \
            """
            INSERT INTO `tag`
            SET tag_id = {tag_id},
                article_id = {article_id},
                tag = "%s",
                tag_url = "%s";
            """.format(**data)

        value = (
            data["tag"],
            data["tag_url"],
        )
        self.res.insert_sql(insert_author_sql, value=value)

    # 写入信息源标签信息
    def insert_source(self, data):
        """
        CREATE TABLE `source` (
          `source_id` decimal(40,0) NOT NULL,
          `article_id` decimal(40,0) NOT NULL,
          `source_name` varchar(255) DEFAULT NULL,
          `source_free` varchar(255) DEFAULT NULL,
          `source_url` varchar(1000) DEFAULT NULL,
          PRIMARY KEY (`source_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
        insert_author_sql = \
            """
            INSERT INTO `source`
            SET source_id = {source_id},
                article_id = {article_id},
                source_name = "%s",
                source_free = {source_free},
                source_url = "%s";
            """.format(**data)

        value = (
            data["source_name"],
            data["source_url"],
        )
        self.res.insert_sql(insert_author_sql, value=value)

    def close(self):
        self.res.close()
