#!/usr/bin/env python
# -*- coding:utf-8 -*-

from importlib import import_module


def include(module):
    res = import_module(module)
    urls = getattr(res, 'urls', res)
    return urls


def url_wrapper(urls):
    wrapper_list = []
    for url in urls:
        path, handles = url
        if isinstance(handles, (tuple, list)):
            for handle in handles:
                pattern, handle_class = handle
                wrap = ('{0}{1}'.format(path, pattern), handle_class)
                wrapper_list.append(wrap)
        else:
            wrapper_list.append((path, handles))
    return wrapper_list
