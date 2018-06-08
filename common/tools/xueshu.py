#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests, re, os, sys
from bs4 import BeautifulSoup
from urllib.parse import unquote

'''
    html内文章封装后获取每个文章的主体内容公共类
'''


def article_body_soup(content):
    soup = BeautifulSoup(content, "html.parser")

    result = soup.findAll(name='div', attrs={"class": "result sc_default_result xpath-log"})
    data = []

    for num in range(len(result)):
        sub_article = result[num]

        # -----<学术标题>----- #
        academic_title = "".join(
            list(sub_article.find(name='a', attrs={"data-click": "{'button_tp':'title'}"}).stripped_strings))

        # -----<学术主要内容>----- #
        academic_contents = sub_article.find(name='div', attrs={"class": "c_abstract"}).stripped_strings
        academic_content = list(academic_contents)[0]

        # -----<学术链接>----- #
        academic_href = sub_article.find(name='a', attrs={"data-click": "{'button_tp':'title'}"}).get("href")

        # -----<学术发表刊物>----- #
        try:
            academic_publish_school_content = sub_article.find(name='div', attrs={"class": "sc_info"}).findAll("span")[1]
        except:
            academic_publish_school_content = ""

        # -----<论文来源： 知网啊， 等>----- #
        source_articles = sub_article.find(name="div", attrs={"class": "sc_allversion"})
        source_articles_li = []
        if source_articles:

            source_articles_span = source_articles.findAll(name="span", attrs={"class": "v_item_span"})
            # print(s1)
            for i in range(len(source_articles_span)):
                # 如果不是【】， 证明这个是免费的
                sub_source_articles_dict = {}
                source_articles_i = source_articles_span[i].findAll(name="i",
                                                                    attrs={"class": "c-icon c-icon-free v_freeicon"})
                if source_articles_i:
                    # 证明是免费的
                    sub_source_articles_dict["free"] = 1
                else:
                    sub_source_articles_dict["free"] = 0

                source_articles_a = source_articles_span[i].find(name="a", attrs={"class": "v_source"})
                sub_source_articles_dict["name"] = source_articles_a.get("title")
                sub_source_articles_dict["url"] = source_articles_a.get("href").strip()

                source_articles_li.append(sub_source_articles_dict)

        try:
            academic_publish_school = [academic_publish_school_content.find("a").get("title")]
            academic_publish_school_href = academic_publish_school_content.find("a").get("href").strip()
        except Exception:
            try:
                academic_publish_school = [i for i in academic_publish_school_content.stripped_strings]
            except:
                academic_publish_school = []
            academic_publish_school_href = ""
        # if academic_publish_school_content.find("a"):
        #     academic_publish_school = academic_publish_school_content.find("a").string.strip()
        #     academic_publish_school_href = academic_publish_school_content.find("a").get("href").strip()
        # else:
        #     academic_publish_school = academic_publish_school_content.string.strip()
        #     academic_publish_school_href = ""

        # -----<作者>----- #
        academic_author = [i.string for i in
                           sub_article.findAll(name='a', attrs={"data-click": "{'button_tp':'author'}"})]

        # -----<作者连接>----- #
        academic_author_href = [i.get("href").strip() for i in
                                sub_article.findAll(name='a', attrs={"data-click": "{'button_tp':'author'}"})]

        if sub_article.find(name='a', attrs={"data-click": "{'button_tp':'sc_cited'}"}):
            # -----<被引量>----- #
            academic_count = sub_article.find(name='a', attrs={"data-click": "{'button_tp':'sc_cited'}"}).string.strip()

            # -----<被引用文章链接>----- #
            academic_count_href = sub_article.find(name='a', attrs={"data-click": "{'button_tp':'sc_cited'}"}).get(
                "href").strip()
        else:
            academic_count = 0
            academic_count_href = ''

        # -----<标签>----- #
        academic_label = [i.string for i in
                          sub_article.findAll(name='a', attrs={"data-click": "{'button_tp':'sc_search'}"})]

        # -----<标签链接>----- #
        academic_label_href = [i.get("href").strip() for i in
                               sub_article.findAll(name='a', attrs={"data-click": "{'button_tp':'sc_search'}"})]

        sub_data = {}
        sub_data["academic_title"] = academic_title
        sub_data["academic_content"] = academic_content
        sub_data["academic_href"] = academic_href
        sub_data["academic_author"] = academic_author
        sub_data["academic_author_href"] = academic_author_href
        sub_data["academic_count"] = academic_count
        sub_data["academic_count_href"] = academic_count_href
        sub_data["academic_label"] = academic_label
        sub_data["academic_label_href"] = academic_label_href
        sub_data["academic_publish_school"] = academic_publish_school
        sub_data["academic_publish_school_href"] = academic_publish_school_href
        sub_data["academic_article_source"] = source_articles_li

        # print("# ======================================>>>")
        # print("\n\n")
        # print("学术标题:", academic_title)
        # print("学术主要内容:", academic_content)
        # print("学术链接:", academic_href)
        # print("作者:", academic_author)
        # print("作者连接:", academic_author_href)
        # print("被引量:", academic_count)
        # print("被引用文章链接:", academic_count_href)
        # print("标签:", academic_label)
        # print("标签链接:", academic_label_href)
        # print("发表刊物地方:", academic_publish_school)
        # print("发表刊物链接:", academic_publish_school_href)
        # print("来源:", source_articles_li)
        # print("\n\n")
        # print("# ======================================>>>")

        data.append(sub_data)
    return data


'''
    通过输入关键词或人名得到的论文文章
'''


def search_academic(research, pn=0):
    '''

    :param research: 搜索的内容
    :return:
    '''
    '''
        wd: search content
        pn： page num 0 其实表示1， 10表示第2页，hh【0， 10， 20， 30， 40， 50... 100, 110】
        :param research:
        :return:
    '''
    pn = pn - 1
    url = "http://xueshu.baidu.com/s?wd={}&pn={}0&tn=SE_baiduxueshu_c1gjeupa&cl=3&ie=utf-8&bs=deep+speech+2%3A+End-to-End+Speech&f=8&rsv_bp=1&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_spt=3".format(
        research, pn)
    # url = "http://xueshu.baidu.com/s?wd={}&pn=0&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&filter=sc_year%3D%7B2010%2C2019%7D&sc_hit=1".format(
    #     research)

    content = requests.get(url).text
    return article_body_soup(content)


'''
    通过搜索到的论文文章内部的被引用量：--》 得到引用文章
'''


def citing_article(url):
    '''
    查看每个文章的引用文章
        URL = "http://xueshu.baidu.com/s?wd=refpaperuri:(ea3049d2c71d9e127ca0fdc7ccb62fbd)&sc_f_para=sc_cita={水果采摘机器人通用夹持机构设计,            13\r\n    }&sort=sc_cited&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8"
        ret = citing_article(URL)
    :param url:
    :return:
    '''

    content = requests.get(url).text
    return article_body_soup(content)


'''
    通过输入人名得到不同地区的人名
'''


def search_user(research=None, url=None):
    '''
    有两种用法：
        1. search_user("周昌")
            url = "http://xueshu.baidu.com" + "/s?wd=author%3A%28%E9%83%AD%E4%B8%87%E5%AD%A6%29%20&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_hilight%3Dperson"
            这上面的url是通常search_academic函数得到的每个文章的作者的链接
        2. sear_user(url)

    wd: search content
    pn： page num 0 其实表示1， 10表示第2页，hh【0， 10， 20， 30， 40， 50... 100, 110】
    :param research:
    :return:
    '''
    if not url:
        url = "http://xueshu.baidu.com/s?wd={}&tn=SE_baiduxueshu_c1gjeupa&cl=3&ie=utf-8&bs=deep+speech+2%3A+End-to-End+Speech&f=8&rsv_bp=1&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_spt=3".format(
            research)
    else:
        if not url[:23] == "http://xueshu.baidu.com":
            url = "http://xueshu.baidu.com" + url

    # url = "http://xueshu.baidu.com/s?wd={}&pn=0&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&filter=sc_year%3D%7B2010%2C2019%7D&sc_hit=1".format(
    #     research)
    li = []
    content = requests.get(url).text

    soup = BeautifulSoup(content, "html.parser")

    # -----> 获取多个人物的span标签 <-----#
    # 由于有一种情况会跳转到单独的学者页， 属于特殊情况：http://xueshu.baidu.com/scholarID/CN-BT734MAJ
    # 　所以用了ｆｌａｇ这种方式
    flag = 1
    if not url:
        result = soup.find(name="div", attrs={"class": "c-border"}).findAll(name="span",
                                                                            attrs={
                                                                                "class": "op-scholar-authorcard-info"})
    else:
        try:
            result = soup.find(name="div", attrs={"class": "op-scholar-authorcard-wr"}).findAll(name="span", attrs={
                "class": "op-scholar-authorcard-info"})
        except:
            flag = 0
            result = []


    if not result:
        if flag:
            # 这种是只有一个人的情况下， 但是是那种为您找到1个学者那种
            result = soup.find(name="span", attrs={"class": "op-scholar-authorcard-intro"})
            description = result.find(name="span", attrs={"class": "c-gap-left-large"}).string
            username = str(result.find('a').string)
            href = str(result.find('a').get("href"))

            # -----> 分割url的目的（1. 需要后面这段加密后的数字标识， 2. 请求需要， 3. 想让用户跳转连接的时候调到我自己的URL） <-----#
            URI = "".join(str(href).split("http://xueshu.baidu.com"))
            li.append({
                "username": username,
                "href": href,
                "uri": URI,
                "description": description,
                "scholarid": URI.split('/')[-1]
            })
        else:
            if "usercenter/data/author?cmd=authoruri" in url:
                url = unquote(url)
                info_li = url.split("author:(")[-1].split(")")
                li.append(
                    {
                        "username": info_li[0],
                        "href": "",
                        "uri": "",
                        "description": info_li[1] if len(info_li) == 2 else "",
                        "scholarid": ''
                    }
                )

    else:

        for i in range(len(result)):
            description = str(result[i].find('p').string)
            username = str(result[i].find('a').string)
            href = str(result[i].find('a').get("href"))

            # -----> 分割url的目的（1. 需要后面这段加密后的数字标识， 2. 请求需要， 3. 想让用户跳转连接的时候调到我自己的URL） <-----#
            URI = "".join(str(href).split("http://xueshu.baidu.com"))
            li.append({
                "username": username,
                "href": href,
                "uri": URI,
                "description": description,
                "scholarid": URI.split('/')[-1]
            })



    # print(li)
    return li


'''
    输入scholarid， 得到每个学者相关联的合作学者， 以及合作次数
'''


def relationship(scholarid):
    '''
        scholarid = "5eb681821d8c17a3fdf9c1f696daaa39"
        ret1 = relationship(scholarid)
    :param scholarid:
    :return:
    '''
    # -----> 如果用ret.text会出现乱码， 所以这个地方用了二进制的形式，然后转成字符串 <----- #

    ret = requests.post("http://xueshu.baidu.com/usercenter/data/author",
                        data={"cmd": "show_co_affiliate", "entity_id": scholarid})
    soup = BeautifulSoup(str(ret.content, encoding='utf-8'), "html.parser")

    li = []

    result = soup.findAll(name="a", attrs={"class": "co_relmap_person"})

    search_user = soup.find(name="div", attrs={"class": "co_relmap_mainauthor"}).find('h3').string


    # -----<得到合作学者的每个人的名称和scholarid以及合作次数>----- #
    for sub_a in result:
        # -----<人物的地址链接>----- #
        href = sub_a.get("href")

        # -----<机构>----- #
        affiliate = sub_a.find(name="div", attrs={"class": "co_person_name"}).get("affiliate")

        # -----<用户名>----- #
        username = sub_a.find(name="div", attrs={"class": "co_person_name"}).string

        # -----<合作次数>----- #
        paper_count = sub_a.find(name="div", attrs={"class": "co_person_name"}).get("paper-count")
        li.append({
            "href": href,
            "affiliate": affiliate,
            "username": username,
            "paper_count": paper_count,
            # 注意， 这个的scholarid是CN-×××××形式， 经过编码的
            "scholarid": href.split('/')[-1]
        })

    return {"data_count": len(li), "data": li, "search_user": search_user, "scholarid": scholarid}




if __name__ == '__main__':
    pass
    # user_li = search_user("郭万学")
    # print(user_li)
    # url = "/s?wd=author%3A%28%E9%83%AD%E4%B8%87%E5%AD%A6%29%20&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_hilight%3Dperson"
    # url = "http://xueshu.baidu.com" + "/s?wd=author%3A%28%E5%91%A8%E6%B0%B8%E6%98%8C%29%20&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_hilight%3Dperson"
    # url = "http://xueshu.baidu.com" + "/s?wd=author%3A%28%E9%83%AD%E4%B8%87%E5%AD%A6%29%20&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_hilight%3Dperson"
    # url = "http://xueshu.baidu.com/usercenter/data/author?cmd=authoruri&amp;wd=authoruri%3A%28af7d460de49db4e2%29%20author%3A%28%E5%BC%A0%E4%B8%87%E5%B2%B1%29%20%E7%AC%AC%E4%B8%80%E5%86%9B%E5%8C%BB%E5%A4%A7%E5%AD%A6%E5%8D%97%E6%96%B9%E5%8C%BB%E9%99%A2"
    # search_user(url=url)
    # search_academic("医")
