# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from datetime import datetime


import urllib
import os
from lxml import etree 
from pymongo  import MongoClient
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import sys
import threading
import requests
request_headers = {
    'Host':"www.toutiao.com",\
    'Referer': 'http://www.toutiao.com/news_hot/',\
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',\
    'Cookie':'__tasessionId=ejkwg0dlu1487757674976; CNZZDATA1259612802=292894742-1487753192-%7C1487753192; tt_webid=56080438353; uuid="w:bdfa4db788204f5c815b1e772735ea29"; _ga=GA1.2.1732663361.1487757676; _gat=1'}
class ExamplePipeline(object):
    lock=threading.Lock()
    MONGODB_SERVER='192.168.163.128'
    MONGODB_PORT=27017
    MONGODB_DB='test'
    
    def __init__(self):
        print "-----------mongo init------------------------"
        try:
            client=MongoClient(self.MONGODB_SERVER,int(self.MONGODB_PORT))
            print client
            self.db=client['news']
        except:
            print "mongodb error"
    @classmethod
    def from_crawl(cls,crawler):
        cls.MONGODB_SERVER='192.168.163.128'
        cls.MONGODB_PORT=27017
        cls.MONGODB_DB='test'
        pipe=cls()
        pipe.crawler=crawler
        return pipe
	
    		
    def process_item(self, item, spider):
        print "hahahahahaha"
        reload(sys)
        sys.setdefaultencoding( "utf-8" )
        if not os.path.exists("/news"):
            os.mkdir("/news")
        os.chdir('/news')
        tag_url=item['chinese_tag']
        if not os.path.exists("/news/"+tag_url):
	      os.mkdir("/news/"+tag_url)
        os.chdir("/news/"+tag_url)
        title=item['title']
        pos=item["source_url"].find('/')
        item['file_path']='/home/ren/photo'+item["source_url"][pos:-1]
        if not os.path.exists('/home/ren/photo/group'):
            os.mkdir('/home/ren/photo/group')
        if not os.path.exists("/news/"+tag_url+"/"+title):
            with open("/news/"+tag_url+"/"+title,"w") as f:
                try:
                    ExamplePipeline.lock.acquire()
                    f.write(("[tag_url]\n").decode('utf-8'))
                    f.write((item['tag_url']+"\n").decode('utf-8'))
                    f.write(("[chinese_tag]\n").decode('utf-8'))
                    f.write((item['chinese_tag']+"\n").decode('utf-8'))
                    f.write(("[title]\n").decode('utf-8'))
                    f.write((item['title']+"\n").decode('utf-8'))
                    f.write(("[abstract]\n").decode('utf-8'))
                    f.write((item['abstract']+"\n").decode('utf-8'))
                    f.write(("[source_url]\n").decode('utf-8'))
                    f.write((item['source_url']+"\n").decode('utf-8'))
                    f.write(("[file_path]\n").decode('utf-8'))
                    f.write((item['file_path']+"\n").decode('utf-8'))
                    f.flush()
                    f.close()
                except:
                    pass
                finally:
                    ExamplePipeline.lock.release()
        
        news_detail={
		"tag_url":item['tag_url'].decode('utf-8'),\
		"chinese_tag":item['chinese_tag'].decode('utf-8'),\
		"title":item['title'].decode('utf-8'),\
		"abstract":item['abstract'].decode('utf-8'),\
		"source_url":item['source_url'].decode('utf-8'),\
		"file_path":item['file_path'].decode('utf-8'),\
		}
        ret=self.db['test'].insert(news_detail)
        print ret
        r=requests.get("http://"+item['source_url'],headers=request_headers)
        r.encoding='utf-8'
        html=r.text
        title_list=Selector(text=html).xpath('//h1[@class="article-title"]/text()').extract()
        if len(title_list)!=0:		
            os.chdir('/home/ren/photo/group')
            if item['file_path']!=None and item['source_url']!=None:
                filename=item['file_path']
                if item['file_path'][-1] =='/':
                    filename=item['file_path'][0:-1]
                if not os.path.exists(filename):
                    with open(filename,'w') as fi:		
                        try:
                            ExamplePipeline.lock.acquire()	
                            fi.write('[article-title]\n'.decode('utf-8'))
                            for i in title_list:
                                fi.write(i.encode('utf-8'))	
#fi.write((str(Selector(text=html).xpath('//h1[@class="article-title"]/text()').extract()).decode('utf-8')))
                                fi.write('\n'.decode('utf-8'))
#content
                            content_list=Selector(text=html).xpath('.//*[@id="article-main"]/div[2]//p/text()').extract()
                            fi.write('[content]\n'.decode('utf-8'))
                            for i in content_list:
                                fi.write(i.encode('utf-8'))
                            fi.write('\n')
#picture 
                            fi.write('[picture]\n'.decode('utf-8')) 
                            pic_list=Selector(text=html).xpath('.//*[@id="article-main"]/div[2]//img/@src').extract()
                            print len(pic_list)

                            for i in range(0,len(pic_list)):
                                fi.write(pic_list[i].encode('utf-8'))
                                print pic_list[i].encode('utf-8')
                                fi.write('\n'.decode('utf-8'))
                            fi.write('\n')
                            fi.flush()
                            fi.close()
                            if len(pic_list)>0:
                                for i in range(0,len(pic_list)):
                                    j=len(str(pic_list[i].encode('utf-8')))-1
                                    while j>0:
                                        if str(pic_list[i].encode('utf-8'))[j]=='/':
                                            break
                                        else:
                                            j-=1
                            pic_location="/home/ren/photo/photos/"+str(pic_list[i].encode('utf-8'))[j+1:-1]
                            with open(pic_location,"wr") as f:
                                f.write(urllib.urlopen(pic_list[i].encode('utf-8')).read())
                                f.flush()
                                f.close()
								
                        except:
                            pass
                        finally:
                            ExamplePipeline.lock.release()
        elif len(Selector(text=html).xpath('/html/body/header/h1/text()').extract())!=0:
            os.chdir('/home/ren/photo/group')

            if item['file_path']!=None and item['source_url']!=None:
                filename=item['file_path']
                if item['file_path'][-1] =='/':
                    filename=item['file_path'][0:-1]
                if not os.path.exists(filename):
                    with open(filename,'w') as fi:
						#title
                        try:
                            ExamplePipeline.lock.acquire()	
                            fi.write('[article-title]\n'.decode('utf-8'))
                            for i in title_list:
	                          fi.write(i.encode('utf-8'))
                            fi.write('\n'.decode('utf-8'))
                            fi.write('[origin]\n'.decode('utf-8'))
                            origin=Selector(text=html).xpath('.//*[@id="source"]/text()').extract()
                            for i in origin:
                                fi.write(i.encode('utf-8'))
                            fi.write('[date]\n'.decode('utf-8'))
                            date=Selector(text=html).xpath('/html/body/header/div/time/text()').extract()
                            for i in date:
                                fi.write(i.encode('utf-8'))					
                            content_list=Selector(text=html).xpath('/html/body/article//p/text()').extract()
                            fi.write('[content]\n'.decode('utf-8'))
                            for i in content_list:
                                fi.write(i.encode('utf-8'))
                            fi.write('\n')
                            fi.write('[picture]\n'.decode('utf-8')) 
                            pic_list=Selector(text=html).xpath('/html/body/article/p[15]//img/@src').extract()
                            print len(pic_list)

                            for i in range(0,len(pic_list)):
                                fi.write(pic_list[i].encode('utf-8'))
	                        print pic_list[i].encode('utf-8')
	                        fi.write('\n'.decode('utf-8'))
                            fi.write('\n')
                            fi.flush()
                            fi.close()
                            if len(pic_list)>0:
                                for i in range(0,len(pic_list)):
                                    j=len(str(pic_list[i].encode('utf-8')))-1
                                    while j>0:
                                        if str(pic_list[i].encode('utf-8'))[j]=='/':
                                            break
                                        else:
                                            j-=1
                            pic_location="/home/ren/photo/photos/"+str(pic_list[i].encode('utf-8'))[j+1:-1]
                            with open(pic_location,"wr") as f:
                                f.write(urllib.urlopen(pic_list[i].encode('utf-8')).read())
                            f.flush()
                            f.close()
                        except:
                            pass
                        finally:
                            ExamplePipeline.lock.release()
        else:
            if str(item['media_url'])=="1":
                f=open("/home/ren/photo/temp","a+")
                f.write(item['media_url']+'\n')
                f.flush()
                f.close()
                return
        return item
		
			
