#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import pymongo
import json
def process_item():
    # 创建redis数据库连接
    rediscli = redis.Redis(host="127.0.0.1", port=6379, db="0")
    # 创建MongoDB数据库连接
    mongocli = pymongo.MongoClient(host="127.0.0.1", port=27017)
    # 创建MongoDB数据库名称
    dbname = mongocli["lianjia_ds"]
    # 创建mongoDB数据库youyuan的名称
    sheetname = dbname["lj_info"]
    offset = 0
    while True:

        # redis 数据库表名 和数据
        source, data = rediscli.blpop("lj_distribute:items")
        offset += 1
        # 将json对象转换成Python对象
        data = json.loads(data)
        # 将数据插入到sheetname里
        sheetname.insert(data)
        print offset

		    
if __name__ == "__main__":
    process_item()


