#!/usr/bin/env python
# -*- coding:utf-8 -*-


def my_4_quartiles(li):
    # 求4分位数
    # 第一步：将n个变量值从小到大排列，X(j)表示此数列中第j个数。
    # 第二步：计算指数，设(n+1)P%=j+g，j为整数部分，g为小数部分。
    # 第三步：1)当g=0时：P百分位数=X(j);
    # 2)当g≠0时：P百分位数=g*X(j+1)+（1-g）*X(j)=X(j)+g*[X(j+1)-X(j)]。
    if isinstance(li, list):
        import math
        li = sorted(li)
        P1 = 0.25
        P2 = 0.5
        P3 = 0.75
        a1 = float((len(li) + 1) * P1)
        a2 = float((len(li) + 1) * P2)
        a3 = float((len(li) + 1) * P3)
        j1 = math.floor(a1)
        j2 = math.floor(a2)
        j3 = math.floor(a3)
        g1 = float(a1) - float(j1)
        g2 = float(a2) - float(j2)
        g3 = float(a3) - float(j3)
        try:
            P_value1 = g1 * li[int(j1)] + (1 - g1) * li[int(j1) - 1]
        except Exception as e1:
            P_value1 = "NaN"
        try:
            P_value2 = g2 * li[int(j2)] + (1 - g2) * li[int(j2) - 1]
        except Exception as e2:
            P_value2 = "NaN"
        try:
            P_value3 = g3 * li[int(j3)] + (1 - g3) * li[int(j3) - 1]
        except Exception as e3:
            P_value3 = "NaN"
        return (P_value1, P_value2, P_value3)
    else:
        raise IndexError



def myNQuartiles(li, p):
    # 求4分位数
    # 第一步：将n个变量值从小到大排列，X(j)表示此数列中第j个数。
    # 第二步：计算指数，设(n+1)P%=j+g，j为整数部分，g为小数部分。
    # 第三步：1)当g=0时：P百分位数=X(j);
    # 2)当g≠0时：P百分位数=g*X(j+1)+（1-g）*X(j)=X(j)+g*[X(j+1)-X(j)]。
    if isinstance(li, list):
        import math
        li = sorted(li)
        P1 = p

        a1 = float((len(li) + 1) * P1)

        j1 = math.floor(a1)

        g1 = float(a1) - float(j1)

        try:
            P_value1 = g1 * li[int(j1)] + (1 - g1) * li[int(j1) - 1]
        except Exception as e1:
            P_value1 = "NaN"

        return P_value1
    else:
        raise IndexError