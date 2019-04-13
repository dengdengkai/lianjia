# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # 14个字段
    # 楼盘名称
    name = scrapy.Field()
    # 楼盘类型
    type = scrapy.Field()
    # 楼盘状态
    status = scrapy.Field()
    # 每平方米的价格
    price = scrapy.Field()
    # 位于成都市哪个区域
    area = scrapy.Field()

    #  评分等链接源
    grade_url = scrapy.Field()
    # 详细地址
    detail_address = scrapy.Field()
    # 最新开盘
    newest_made_time = scrapy.Field()
    # 交房时间
    given_time = scrapy.Field()
    # 开发商
    developers = scrapy.Field()

    # 综合评分
    general_grade = scrapy.Field()
    # 周边配套评分
    around_grade = scrapy.Field()
    # 交通方便评分
    traffic_grade = scrapy.Field()
    # 绿化环境评分
    green_grade = scrapy.Field()
    # 爬虫名称
    spider_name = scrapy.Field()





