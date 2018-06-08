#!/usr/bin/env python
# -*- coding:utf-8 -*-

import configparser
import os
import datetime
import time
import pymongo
# import MySQLdb
import pymysql
from common.myLog.MyProjectLog import Logger
import datetime, time, uuid, re


class Config(object):
    """
    # Config().get_content("user_information")
    """

    def __init__(self, config_filename="my.cnf"):
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


class MongoDb(object):
    def __init__(self, host, port, user=None, password=None):
        self._db_host = host
        self._db_port = int(port)
        self._user = user
        self._password = password
        self.conn = None

    def connect(self):
        self.conn = pymongo.MongoClient(self._db_host, self._db_port)
        return self.conn

    def get_db(self, db_name):
        collection = self.conn.get_database(db_name)
        if self._user and self._password:
            collection.authenticate(self._user, self._password)
        return collection

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None


class base_pymysql(object):
    def __init__(self, host, port, user, password, db_name=None):
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pymysql.connect(host=self.db_host, port=self.db_port, user=self.user,
                                    passwd=self.password, db=self.db, charset="utf8")
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)


class MyPymysql(base_pymysql):
    """
    Basic Usage:

        ret = My_Pymysql('test1')
        res = ret.selectone_sql("select * from aaa")
        print(res)
        ret.close()
        --------------
        class writer_information_tables():
            def __init__(self, libname="metadata"):
                self.libname = libname
                self.res = MyPymysql('metadata')

            def insert_sql(self, data):
                sql = '''insert INTO `meta_variable` SET DataTableID={}, VarValues="%s";'''.format(
                    data["DataTableID"])
                value = (data["VarValues"])
                # print(sql)
                # self.res.idu_sql(sql)
                self.res.insert_sql(sql, value=value)
            def close(self):

                self.res.close()

    Precautions:
        Config.__init__(self, config_filename="my.cnf")

    """

    def __init__(self, conf_name):
        self.conf = Config().get_content(conf_name)
        super(MyPymysql, self).__init__(**self.conf)
        self.connect()

    def idu_sql(self, sql, value=None):
        # adu: insert, delete, update的简写
        # 考虑到多语句循环, try就不写在这里了
        self.cursor.execute(sql, value)
        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def insert_sql(self, sql, value=None):
        # adu: insert, delete, update的简写
        # 防止sql注入
        self.cursor.execute(sql, value)
    def update_sql(self, sql, value=None):
        # adu: insert, delete, update的简写
        # 防止sql注入
        self.cursor.execute(sql, value)
    def delete_sql(self, sql, value=None):
        # adu: insert, delete, update的简写
        # 防止sql注入
        self.cursor.execute(sql, value)

    def selectone_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchone()

    def selectall_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchall()

    def select_sql(self, sql, value=None):
        # 防止sql注入
        self.cursor.execute(sql, value)
        self.conn.commit()
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
        self.conn = None
        self.cursor = None


def result(status, value=None, messageValue=None):
    """
    staatus:
    2000, 什么都ok
    4000, 客户上传的文件格式不正确
    4001， 客户上传的文件列超过5400
    4002， 值传递错误
    5000， 服务器错误
    5001， 数据表已经存在
    5002,  sql语句错误
    """
    if status == 2000:
        message = u"True"
    elif status == 4000:
        message = u"客户上传的文件格式不正确"
    elif status == 4001:
        message = u"客户上传的文件列超过1024"
    elif status == 4002:
        message = u"未传值或值传递错误!"
    elif status == 4003:
        message = u"文件数据不对"
    elif status == 4004:
        message = u"已经存在"
    elif status == 4005:
        message = u"用户未认证或认证不成功"
    elif status == 4006:
        message = u"无法进行数据分析"
    elif status == 5000:
        message = u"服务器错误"
    elif status == 5001:
        message = u"数据表已经存在"
    elif status == 5002:
        message = u"sql语句错误"
    else:
        if messageValue:
            message = str(messageValue)
        else:
            message = u"未知错误"
    return {
        "statuscode": status,
        "statusmessage": message,
        "value": value
    }


class my_datetime():
    """
    Basic usage:

        a = datetime.datetime(2016, 9, 21, 13, 42, 8)
        b = "2016-11-15 15:32:12"
        c = u'2016-09-21 13:37:34'
        print type(c)
        d = 1474436826.0
        e = 13710788676.0
        ret = my_datetime()
        res = ret.become_datetime(e)
        print res
        print type(res)
    """

    def __init__(self):
        # 缺少对utc时间的判断
        pass

    def become_timestamp(self, dtdt):
        # 将时间类型转换成时间戳
        if isinstance(dtdt, datetime.datetime):
            timestamp = time.mktime(dtdt.timetuple())
            return timestamp

        elif isinstance(dtdt, str):
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d  %H:%M:%S")
                timestamp = time.mktime(a_datetime.timetuple())
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
                timestamp = time.mktime(a_datetime.timetuple())
            return timestamp

        elif isinstance(dtdt, float):
            return dtdt

            # elif isinstance(dtdt, unicode):
            #     if dtdt.split(" ")[1:]:
            #         a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
            #         timestamp = time.mktime(a_datetime.timetuple())
            #     else:
            #         a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
            #         timestamp = time.mktime(a_datetime.timetuple())
            #     return timestamp

    def become_datetime(self, dtdt):
        # 将时间类型转换成datetime类型
        if isinstance(dtdt, datetime.datetime):
            return dtdt

        elif isinstance(dtdt, str):
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
            return a_datetime

        elif isinstance(dtdt, float):
            # 把时间戳转换成datetime类型
            a_datetime = datetime.datetime.fromtimestamp(dtdt)
            return a_datetime

            # elif isinstance(dtdt, unicode):
            #     if dtdt.split(" ")[1:]:
            #         a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
            #     else:
            #         a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
            #     return a_datetime

    def become_str(self, dtdt):
        # 把时间类型转换成字符串
        if isinstance(dtdt, datetime.datetime):
            a_datetime = dtdt.strftime("%Y-%m-%d %H:%M:%S")
            return a_datetime

        elif isinstance(dtdt, str):
            return dtdt

        elif isinstance(dtdt, float):
            a_datetime_local = datetime.datetime.fromtimestamp(dtdt)
            a_datetime = a_datetime_local.strftime("%Y-%m-%d %H:%M:%S")
            return a_datetime

            # elif isinstance(dtdt, unicode):
            #     # 区别：一个是strp， 一个是strf
            #     if dtdt.split(" ")[1:]:
            #         a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
            #         a_datetime = a_datetime.strftime("%Y-%m-%d %H:%M:%S")
            #     else:
            #         a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
            #         a_datetime = a_datetime.strftime("%Y-%m-%d")
            #     return a_datetime

    @staticmethod
    def str_datetime():
        return (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")


def MyGuid():
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    us = ("%.7f" % time.time())[-7:]

    res = "".join(re.findall('\d+', str(uuid.uuid4())))[:7]

    ret = date + us + res

    return ret

try:
    logDict = Config().get_content("log")
    logPath = logDict['logpath']
    logName = logDict['logname']

except Exception as e:
    logPath = None
    logName = None
my_log = Logger(filepath=logPath, filename=logName)
