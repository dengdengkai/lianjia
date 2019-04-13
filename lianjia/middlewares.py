# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import base64
import random

from lianjia.proxys import PROXIES
from lianjia.spiders.agents import USERAGENT_AGENTS


class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USERAGENT_AGENTS)
        print useragent
        #request.headers.setdefault("User-Agent", useragent)
        request.headers['User-Agent'] = useragent
class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        #print proxy
        if proxy['user_passwd'] is None:
            # 如果没有代理账户验证使用方式
            request.meta['proxy'] = "http://" + proxy['ip_port']
        else:
            # 账户验证，账户和密码需要转码
            base64_userpasswd=base64.b64encode(proxy['user_passwd'])
            #print base64_userpasswd
            # 对账户密码进行base64编码转换
            request.meta['proxy'] = "http://" + proxy['ip_port']
            # 对应到代理服务器的信令格式里
            request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd

