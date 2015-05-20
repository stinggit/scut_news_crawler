#!/usr/bin/python
# -*- coding: utf-8 -*-
import re  
import json  
import redis
  
from scrapy.selector import Selector
try:  
    from scrapy.spider import Spider  
except:  
    from scrapy.spider import BaseSpider as Spider  
from scrapy.utils.response import get_base_url  
from scrapy.utils.url import urljoin_rfc  
from scrapy.contrib.spiders import CrawlSpider, Rule  
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle  
try:
    import cPickle as pickle
except ImportError:
    import pickle
    
from scutnews.items import *
  
class ScutSpider(CrawlSpider):
    name = "news"  
    allowed_domains = ["news.scut.edu.cn"]  
    start_urls = [  
        "http://news.scut.edu.cn/s/22/t/3/52/1d/info21021.htm"  
    ]  
    # rules = [
    #     Rule(sle(allow=("/position.php\?&start=\d{,4}#a")), follow=True, callback='parse_item')  
    # ]  
    r = redis.Redis(host = 'localhost',port = 6379,db = 1)
    def parse(self,response):
        sel = Selector(response)
        base_url = get_base_url(response)
        urls = sel.css('a')
        for url in urls:
            print url.xpath('@href').extract()[0]

        total_item = sel.css("#LIST_PAGINATION_COUNT")
        if len(count_item) > 0:
            total_count = count_item.xpath("text()").extract()[0]
            list_url_tuple = os.path.split(base_url)
            for i in total_count:
                url = list_url_tuple[0] + '/i/' + str(total_count) + "/" + list_url_tuple[1]
                print url

        if len(sel.css(".display_news_con")) > 0:
          
            info = []
            contents = sel.css(".display_news_con")
            title = contents.css(".atitle").xpath("text()").extract()[0]
            posttime = contents.css(".posttime").xpath("text()").extract()[0]
            items = posttime.split("\r\n")

            temp_submit_time = item[0].split(":")
            info['submit_time'] = temp_submit_time[1] + temp_submit_time[2]
            temp_publish_time = item[1].split(":")
            info['publish_time'] = temp_publish_time[1] + temp_publish_time[2]
            info['department'] = item[2].split(":")[1]
            info['content'] = contents.css(".entry").extract()[0]
            info['last_modified'] = response.headers['Last-Modified']

            return info
      
        # def parse_item(self, response): # 提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据  
        #     items = []  
        #     sel = Selector(response)
        #     base_url = get_base_url(response)  
        #     sites_even = sel.css('table.tablelist tr.even')
        #     for site in sites_even:  
        #         item = TencentItem()  
        #         item['name'] = site.css('.l.square a').xpath('text()').extract()  
        #         relative_url = site.css('.l.square a').xpath('@href').extract()[0]  
        #         item['detailLink'] = urljoin_rfc(base_url, relative_url)  
        #         item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()  
        #         item['workLocation'] = site.css('tr > td:nth-child(4)::text').extract()  
        #         item['recruitNumber'] = site.css('tr > td:nth-child(3)::text').extract()  
        #         item['publishTime'] = site.css('tr > td:nth-child(5)::text').extract()  
        #         items.append(item)  
        #         #print repr(item).decode("unicode-escape") + '\n'  
      
        #     sites_odd = sel.css('table.tablelist tr.odd')  
        #     for site in sites_odd:  
        #         item = TencentItem()  
        #         item['name'] = site.css('.l.square a').xpath('text()').extract()  
        #         relative_url = site.css('.l.square a').xpath('@href').extract()[0]  
        #         item['detailLink'] = urljoin_rfc(base_url, relative_url)  
        #         item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()  
        #         item['workLocation'] = site.css('tr > td:nth-child(4)::text').extract()  
        #         item['recruitNumber'] = site.css('tr > td:nth-child(3)::text').extract()  
        #         item['publishTime'] = site.css('tr > td:nth-child(5)::text').extract()  
        #         items.append(item)  
        #         #print repr(item).decode("unicode-escape") + '\n'  
      
        #     info('parsed ' + str(response))  
        #     return items  
  
  
    def _process_request(self, request):  
        info('process ' + str(request))  
        return request  

    def pagination_url(self,sel,base_url):
        

