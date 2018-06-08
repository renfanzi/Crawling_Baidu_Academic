#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import os
import logging.handlers


class Logger(logging.Logger):
    """
    # my_log = Logger()
    #
    # # 输出日志
    # # myLog.info("日志模块消息!")
    # # myLog.debug("日志模块调试消息!")
    # my_log.error("日志模块错误消息!")
    """

    def __init__(self, filepath=None, filename="myProject.log"):
        super(Logger, self).__init__(self)
        # 日志文件名

        if not filepath:
            filepath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        else:
            if not os.path.exists(filepath):
                os.makedirs(filepath)
        if filepath[-1] == '/':
            filepathname = filepath + filename
        else:
            filepathname = filepath + '/' + filename
        self.filename = filepathname

        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        # fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 5)
        fh = logging.handlers.WatchedFileHandler(self.filename)
        fh.suffix = "%Y%m%d-%H%M.log"
        fh.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] - %(filename)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - [%(message)s]')
        fh.setFormatter(formatter)

        # 给logger添加handler
        self.addHandler(fh)
