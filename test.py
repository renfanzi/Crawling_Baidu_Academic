#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys


# 明天可以把这个封装出来

class a():
    def __init__(self):
        pass

    def a1(self):
        print("This is A1")


class b(a):
    def __init__(self):
        super(b, self).__init__()
    def b1(self):
        print("This is B1")

class c(a):
    def __init__(self):
        super(c, self).__init__()

class d(b, c):
    def __init__(self):
        super(c, self).__init__()
        super(b, self).__init__()

if __name__ == '__main__':
    dd = d()
    dd.a1()
    dd.b1()


    def comp(y):
        c = y > 11

        return c


    ret1 = map(comp, [1, 2, 4, 11, 22, 33])

    for i in ret1:
        print(i)

    ret2 =filter(comp,[1,2,4,11, 22, 33])

    for i in ret2:

        print(i)
