from scrapy.spiders import CrawlSpider, Rule

from tutorial.items import *
import sys
import logging
import datetime
import requests
import re
from lxml import etree

from scrapy.selector import Selector
from scrapy.http import Request


from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest, HtmlResponse
import scrapy
from tutorial.scrapy_redis.spiders import *
import time
from datetime import datetime
import re
import json
import time
import random
import urllib
import requests
import os

reload(sys)
sys.setdefaultencoding('utf8')
request_headers = {
        'Host':"www.toutiao.com",\
        'Referer': 'http://www.toutiao.com/news_hot/',\
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',\
        'Cookie':'__tasessionId=ejkwg0dlu1487757674976; CNZZDATA1259612802=292894742-1487753192-%7C1487753192; tt_webid=56080438353; uuid="w:bdfa4db788204f5c815b1e772735ea29"; _ga=GA1.2.1732663361.1487757676; _gat=1'}

#from dmoz.items import ExampleItem
class sinaSpider(RedisCrawlSpider):
    name = 'sinaSpider'
    redis_key='sinaSpider:start_urls'
    allowed_domains = ['www.toutiao.com']
    #start_urls = ['http://www.toutiao.com/api/pc/feed/']   
    def parse(self, response):
        text=response.body.decode('utf-8')
        data=json.loads(text)
        d=data['data']
        print len(d)
        if len(d)==0:
	      return
        for i in range(0,len(d)):
            if d[i]['tag_url']!='video' and d[i].has_key('chinese_tag'):
                item=ExampleItem()
                #print d[i]['tag_url']
                #print d[i]['chinese_tag']
                #print d[i]['title']
                if d[i].has_key('abstract'):
                    print d[i]['abstract']
                    item['abstract']=d[i]['abstract']
                else:
                    item['abstract']='None'
                    print d[i]['source_url']
                if d[i].has_key('media_url'):
                    item['media_url']=d[i]['media_url']
                    item['has_media_url']=1
                else:
                    item['has_media_url']=0
                item['tag_url']=d[i]['tag_url']
                item['chinese_tag']=d[i]['chinese_tag']
                item['tag_url']=d[i]['tag_url']
                item['title']=d[i]['title']

                item['source_url']='www.toutiao.com'+d[i]['source_url']
                yield item
                time.sleep(1)
            else:
                continue
        t=data['next']["max_behot_time"]
        #print str(t)
	print "----------------------------------"
        query_data = {\
		'category':"news_hot",\
		'utm_source': 'toutiao',\
		'widen': '1',\
		'max_behot_time': str(t),\
		'max_behot_time_tmp': str(t),\
		   'tadrequire': "true",\
		'as':'A185480A2E58133',\
		'cp':'58AE48B133938E1'}
        query_url = 'http://www.toutiao.com/api/pc/feed/' + '?' + urllib.urlencode(query_data)
        yield Request(query_url,headers=request_headers,callback=self.parse)
	
