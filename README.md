# Datagg
Datagg（Data aggregation) is designed to crawl and store data. The data will be input of model training and material of article. 


运行环境:
机器centos 7
python 2.7
scrapy 1.3.2
redis  3.2.8
mongodb

安装:
1.安装scrapy(建议安装pip)

1下载get-pip.py文件,执行python  get-pip.py
检查是否安装成功pip --version
2安装openssl  
3安装lxml
4安装scrapy  使用pip install  scrapy
验证是否成功  scrapy


2安装python需要模块 
redis模块  pip install redis
mongodb模块 pip install pymongo
requests模块  pip install requests

测试 输入python 在命令行输入 import redis,pymongo不出错就安装成功了

使用:
1.开启redis-server redis.conf
2.开启mongodb 
3.切换到tutorial目录下执行 scrapy crawl sinaSpider运行 此时爬虫会进入到阻塞状态 没有任务
4.启动redis-cli -h redis服务器ip    连接redis server 
执行lpush  sinaSpider:start_urls  http://www.toutiao.com/api/pc/feed/
此时爬虫就会自动启动 

注意事项:
注意配置代码中出现的redis,mongodb的ip地址端口号  