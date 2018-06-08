# Website Name

__Crawling_Baidu_Academic__  
爬虫： 爬取百度学术
 
This websit based on Python Tornado, but i don't use tornado  
  
## api:  
1. core/SelectDetail.py  
```buildoutcfg
    xueshu_search_academic(pn, search_content)
```


### 表结构


1. 文章表
```buildoutcfg
	1. 文章ID  article_id
	2. 学术标题  academic_title
	3. 学术链接  article_url  
	4. 学术内容  article_contents
	5. 被引用量  reference_quantity
	6. 被引用文章链接  reference_url
	8. 发表刊物  publications
	9. 刊物链接  publications_url
	11. 时间 create_time
	12. md5 article_md5
```

2. 作者表：
```buildoutcfg
	1. 文章ID  article_id
	2. 作者ID  author_id
	3. 作者  author
	4. 作者链接  author_url
	5. 作者机构  author_mechanism
	6. 作者可能机构 【石家庄铁路学院， 北京农业大学，...】author_maybe_mechanism

```

3. 标签表：
```buildoutcfg
	1. 文章ID  article_id
	2. 标签ＩＤ  tag_id
	3. 标签  tag
	4. 标签链接  tag_url
```



4. 来源表：
```buildoutcfg
	1. 文章id
	2. 来源id
	3. 来源名字
	4. 来源是否免费 1: 免费 0： 付费
	5. 来源url
```


