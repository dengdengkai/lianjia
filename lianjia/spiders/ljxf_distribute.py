# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lianjia.items import LianjiaItem
import sys
from scrapy_redis.spiders import RedisSpider
reload(sys)
sys.setdefaultencoding('utf-8')

#class LjxfSpider(scrapy.Spider):
class LjxfSpider(RedisSpider):
    name = 'lj_distribute'
    #allowed_domains = ['cd.fang.lianjia.com/loupan']

    #start_urls = [url + str(start) + end]
    redis_key = "ljspider:start_urls"
    url = "https://cd.fang.lianjia.com/loupan/jinjiang-qingyang-wuhou-gaoxin7-chenghua-jinniu-tianfuxinqu-gaoxinxi1-shuangliu-wenjiang-pidou-longquanyi-xindou/pg"
#rediskey:https://cd.fang.lianjia.com/loupan/
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(LjxfSpider, self).__init__(*args, **kwargs)
    def parse(self, response):
        for i in range(1, 101):
            start = i
            url = self.url + str(start) + '/'
            print url
            yield scrapy.Request(url=url, callback=self.parse_first)

    def parse_first(self, response):
        # 此处不转码 。extract（）
        houses = response.xpath("//ul[@class='resblock-list-wrapper']/li/div[@class='resblock-desc-wrapper']")
        # 初始化一个空列表用于存储每一页的楼盘（每一页10个）
        items = []
        for each in houses:
            item = LianjiaItem()
            # 楼盘名称
            item['name'] = each.xpath("div[@class='resblock-name']/a/text()").extract_first("null")
            # 楼盘类型
            item['type'] = each.xpath("div[@class='resblock-name']/span[@class='resblock-type']/text()").extract_first()
            # 楼盘价格
            item['price'] = each.xpath("div[@class='resblock-price']//span[@class='number']/text()").extract_first()
            # 楼盘状态
            item['status'] = each.xpath("div[@class='resblock-name']/span[@class='sale-status']/text()").extract_first()
            # 楼盘区域位置
            item['area'] = each.xpath("div[@class='resblock-location']/span[1]/text()").extract_first()
            # 评分等链接源
            grade_url = 'https://cd.fang.lianjia.com/' + each.xpath("div[@class='resblock-name']/a/@href").extract_first()
            item['grade_url'] = grade_url
            items.append(item)
        for item in items:
            yield scrapy.Request(url=item['grade_url'], meta={'meta_1': item}, callback=self.second_parse, dont_filter=True)


    def second_parse(self, response):
        item = response.meta['meta_1']
        item['detail_address'] = response.xpath('//div[@class="mod-banner"]//p[contains(@class,"where")]/span/@title').extract_first()
        item['newest_made_time'] = response.xpath('//div[@class="mod-banner"]//p[contains(@class,"when")]/span[2]/text()').extract_first()
        # 交房时间
        item['given_time'] = response.xpath('//div[contains(@class,"loupan")]/ul/li[3]/p/span[2]/text()').extract_first()
        # 开发商
        item['developers'] = response.xpath('//div[contains(@class,"loupan")]/p[4]/span[2]/text()').extract_first()
        # 综合评分
        item['general_grade'] = response.xpath('//span[@class="score"]/text()').extract_first()
        scores = response.xpath('//div[@class="item"]//i/text()').extract()
        # 周边配套评分
        if len(scores) > 0:
            item['around_grade'] = scores[0]
            # 交通方便评分
            item['traffic_grade'] = scores[1]
            # 绿化环境评分
            item['green_grade'] = scores[2]
        else:
            item['around_grade'] = "null"
            item['traffic_grade'] = "null"
            # 绿化环境评分
            item['green_grade'] = "null"
        yield item



