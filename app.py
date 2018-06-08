#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import os
from tornado.httpserver import HTTPServer
from tornado.options import define, options
from controllers.HomeHandlers import My404, write_error
from common.util.IncludeUrl import url_wrapper, include
from common.Base import Config

ServerPort = Config().get_content("server")

define("port", default=ServerPort["serverport"], type=int)
# define("port", default=8005, type=int)
_ROOT_PATH = os.path.dirname(__file__)
ROOT_JOIN = lambda sub_dir: os.path.join(_ROOT_PATH, sub_dir)

router = url_wrapper([
    (r'', include('urls')),
])

settings = dict(
    template_path=ROOT_JOIN('views'),
    static_path=ROOT_JOIN('static'),
    # cookie_secret=Env.COOKIE_SEC,
    default_handler_class=None,
)

tornado.web.RequestHandler.write_error = write_error
application = tornado.web.Application(router, **settings)

if __name__ == "__main__":
    server = HTTPServer(application, max_buffer_size=504857600)
    server.bind(options.port, address="0.0.0.0")
    server.start(10)  # Forks multiple sub-process
    tornado.ioloop.IOLoop.current().start()
