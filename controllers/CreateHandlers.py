#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from controllers.HomeHandlers import BaseHandler, initializeBaseRequestHandler
from common.Base import result, MyGuid, my_datetime, Config, my_log


class MyTestHandler(BaseHandler):
    # executor = ThreadPoolExecutor(2)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.asynchronous_get()

    def _get(self):
        user = self.get_argument('user', None)
        print("get", user)
        ret = json.dumps(result(status=2000, value="hello world!"))
        return ret

    def post(self, *args, **kwargs):
        self.asynchronous_post()

    def _post(self):
        user = self.get_argument('user', None)
        print("post", user)
        ret = json.dumps(result(status=2000, value="hello world!"))
        return ret


class CreateProjectHandler(initializeBaseRequestHandler):
    def post(self, *args, **kwargs):
        self.asynchronous_post()

    def _post(self):
        if self.verifyFlag == 1 and self.status == 0:
            return json.dumps(result(status=2000, value="hello world!"))
        else:
            return self.noLogin()

    def noLogin(self):
        return json.dumps(result(status=4005))
