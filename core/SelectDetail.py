#!/usr/bin/env python
# -*- coding:utf-8 -*-

from common.tools.xueshu import search_academic, search_user
from common.Base import my_log, my_datetime
from models.CreateModel import InsertBaiduDataModel

from decimal import Decimal
import datetime, time, uuid, re, json
import hashlib


def MyGuid():
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    us = ("%.7f" % time.time())[-7:]

    res = "".join(re.findall('\d+', str(uuid.uuid4())))[:7]

    ret = date + us + res

    return ret


def xueshu_search_academic(pn, search_content):
    # 得到数据
    data = search_academic(search_content, pn)

    obj = InsertBaiduDataModel()

    # for sub_data_dict in data:
    for sub_data in range(len(data)):
        '''
        print("学术标题:", sub_data_dict["academic_title"])
        print("学术主要内容:", sub_data_dict["academic_content"])
        print("学术链接:", sub_data_dict["academic_href"])
        print("作者:", sub_data_dict["academic_author"])
        print("作者连接:", sub_data_dict["academic_author_href"])
        print("被引量:", sub_data_dict["academic_count"])
        print("被引用文章链接:", sub_data_dict["academic_count_href"])
        print("标签:", sub_data_dict["academic_label"])
        print("标签链接:", sub_data_dict["academic_label_href"])
        print("发表刊物地方:", sub_data_dict["academic_publish_school"])
        print("发表刊物链接:", sub_data_dict["academic_publish_school_href"])
        print("来源:", sub_data_dict["academic_article_source"])
        '''

        """
        # -----<学术标题: str>----- #
        academic_title = sub_data_dict["academic_title"]
        # -----<学术主要内容: str>----- #
        academic_content = sub_data_dict["academic_content"]
        # -----<学术链接: str>----- #
        academic_href = sub_data_dict["academic_href"]
        # -----<作者: li>----- #
        academic_author = sub_data_dict["academic_author"]
        # -----<作者连接: li>----- #
        academic_author_href = sub_data_dict["academic_author_href"]
        # -----<被引量: int>----- #
        academic_count = sub_data_dict["academic_count"]
        # -----<被引用文章链接: str>----- #
        academic_count_href = sub_data_dict["academic_count_href"]
        # -----<标签: li>----- #
        academic_label = sub_data_dict["academic_label"]
        # -----<标签链接: li>----- #
        academic_label_href = sub_data_dict["academic_label_href"]
        # -----<发表刊物地方: li （但只有一个）>----- #
        academic_publish_school = sub_data_dict["academic_publish_school"]
        # -----<发表刊物链接: str>----- #
        academic_publish_school_href = sub_data_dict["academic_publish_school_href"]
        # -----<来源: li>----- #
        academic_article_source = sub_data_dict["academic_article_source"]
        """

        # -----<学术标题: str>----- #
        academic_title = data[sub_data]["academic_title"]
        # -----<学术主要内容: str>----- #
        academic_content = data[sub_data]["academic_content"]
        # -----<学术链接: str>----- #
        academic_href = data[sub_data]["academic_href"]
        # -----<作者: li>----- #
        academic_author = data[sub_data]["academic_author"]
        # -----<作者连接: li>----- #
        academic_author_href = data[sub_data]["academic_author_href"]
        # -----<被引量: int>----- #
        academic_count = data[sub_data]["academic_count"]
        # -----<被引用文章链接: str>----- #
        academic_count_href = data[sub_data]["academic_count_href"]
        # -----<标签: li>----- #
        academic_label = data[sub_data]["academic_label"]
        # -----<标签链接: li>----- #
        academic_label_href = data[sub_data]["academic_label_href"]
        # -----<发表刊物地方: li （但只有一个）>----- #
        academic_publish_school = data[sub_data]["academic_publish_school"]
        # -----<发表刊物链接: str>----- #
        academic_publish_school_href = data[sub_data]["academic_publish_school_href"]
        # -----<来源: li>----- #
        academic_article_source = data[sub_data]["academic_article_source"]

        # 写入文章基本数据
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

        article_id = MyGuid()
        create_time = my_datetime.str_datetime()
        article_data = {}
        article_data["article_id"] = article_id
        article_data["academic_title"] = academic_title
        article_data["article_url"] = academic_href
        article_data["article_contents"] = academic_content
        article_data["reference_quantity"] = academic_count
        article_data["reference_url"] = academic_count_href
        article_data["publications"] = academic_publish_school[0] if academic_publish_school else ''
        article_data["publications_url"] = academic_publish_school_href
        article_data["create_time"] = create_time


        md5_obj = hashlib.md5()
        t_c = academic_title + academic_content
        md5_obj.update(t_c.encode("utf-8"))
        article_md5 = md5_obj.hexdigest()
        article_data["article_md5"] = article_md5

        # 得到作者信息
        '''
        CREATE TABLE `authors` (
          `author_id` int(11) NOT NULL,
          `article_id` decimal(40,0) NOT NULL,
          `author` varchar(255) DEFAULT NULL,
          `author_url` varchar(1000) DEFAULT NULL,
          `author_mechanism` varchar(255) DEFAULT NULL,
          `author_maybe_mechanism` varchar(1000) DEFAULT NULL,
          PRIMARY KEY (`author_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        author_li = []
        for i in range(len(academic_author)):
            authors_data = {}
            author_id = MyGuid()
            # -----<作者ID: decimal>----- #
            authors_data["author_id"] = author_id
            # -----<文章ID: decimal>----- #
            authors_data["article_id"] = article_id
            # -----<作者: str>----- #
            authors_data["author"] = academic_author[i]
            # -----<作者URL: str>----- #
            authors_data["author_url"] = academic_author_href[i]
            # -----<作者机构: str>----- #
            author_data = search_user(url=academic_author_href[i])
            author_mechanism = ""
            author_maybe_mechanism = []
            if len(author_data) == 1:
                author_mechanism = author_data[0]["description"]
            elif len(author_data) > 1:
                for j in author_data:
                    author_maybe_mechanism.append(j["description"])
            authors_data["author_mechanism"] = author_mechanism
            # # -----<作者可能机构: str＝json（li）>----- #
            authors_data["author_maybe_mechanism"] = json.dumps(author_maybe_mechanism,
                                                                ensure_ascii=False) if author_maybe_mechanism else ""
            author_li.append(authors_data)

        # 得到标签信息
        """
        CREATE TABLE `tag` (
          `tag_id` decimal(40,0) NOT NULL,
          `article_id` decimal(40,0) NOT NULL,
          `tag` varchar(255) DEFAULT NULL,
          `tag_url` varchar(1000) DEFAULT NULL,
          PRIMARY KEY (`tag_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
        tag_li = []
        for j in range(len(academic_label)):
            tag_data = {}
            tag_id = MyGuid()
            tag_data["tag_id"] = tag_id
            tag_data["article_id"] = article_id
            tag_data["tag"] = academic_label[j]
            tag_data["tag_url"] = academic_label_href[j]
            tag_li.append(tag_data)

        # 得到数据源信息
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
        source_li = []
        for k in range(len(academic_article_source)):
            source_data = {}
            source_id = MyGuid()
            source_data["source_id"] = source_id
            source_data["article_id"] = article_id
            source_data["source_name"] = academic_article_source[k]["name"]
            source_data["source_free"] = academic_article_source[k]["free"]
            source_data["source_url"] = academic_article_source[k]["url"]
            source_li.append(source_data)

        # 写入数据

        # ++++++++++++
        # flag = obj.insert_articles(article_data)
        # #注意判断去重问题, 如果重复， 就可以不用执行下面
        # if not flag:
        #     for authors in author_li:
        #         obj.insert_authors(authors)
        #
        #     for tags in tag_li:
        #         obj.insert_tag(tags)
        #
        #     for sources in source_li:
        #         obj.insert_source(sources)
        #
        # obj.res.commit()
        # ++++++++++++

        try:

            flag = obj.insert_articles(article_data)
            # 注意判断去重问题, 如果重复， 就可以不用执行下面
            # print("flag: ", flag)
            if flag == 0:
                for authors in author_li:
                    obj.insert_authors(authors)

                for tags in tag_li:
                    obj.insert_tag(tags)

                for sources in source_li:
                    obj.insert_source(sources)

                obj.res.commit()

        except Exception as e:
            my_log.error(e)
            my_log.error("error: pn->%s and i->%s"%(pn, sub_data))
            obj.res.rollback()

    obj.close()


if __name__ == '__main__':
    pn = 10000
    search_content = "医" # 共计68页， 639条数据

    # ==============

    # xueshu_search_academic(16, search_content)

    # ==============


    for i in range(pn):
        a1 = time.time()
        xueshu_search_academic(i, search_content)
        import random
        print("time: ", time.time() - a1, "\n i: ", i)
        # print(i)
        # time.sleep(random.randrange(15, 25))
        print("random:", time.sleep(random.randrange(15, 25)))
