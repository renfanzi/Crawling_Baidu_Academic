#!/usr/bin/env python
# -*- coding:utf-8 -*-


from controllers.CreateHandlers import MyTestHandler, CreateProjectHandler

urls = list()

testUrls = [(r'/index', MyTestHandler), ]

createUrls = [
    (r'/CreateProject', CreateProjectHandler),
]

urls += testUrls + createUrls
