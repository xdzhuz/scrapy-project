# scrapy-project

## 文件说明

* items.py: 定义抓取的数据的属性

* pipelines.py: 将抓取到的数据保存到数据库

* spiders文件夹下文件: 抓取数据

## 运行说明

authorinfo: 抓取新浪股吧的作者信息, 运行: `scrapy crawl authorinfo`

guba: 爬取新浪股吧, 运行: `scrapy crawl guba`

hexunguba: 爬取和讯股吧, 运行: `scrapy crawl hexun`

sinablog: 爬取新浪博客, 运行: `scrapy crawl sinablog`

sinablogcontent: 爬取新浪博客内容, 运行: `scrapy crawl sinablogcontent`

hexuncontent: 爬取和讯股吧内容, 运行: `scrapy crawl hexuncontent`


