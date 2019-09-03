# cd E:\untitled\cnblogs\cnblogSpider到此运行，scrapy crawl cnblogs
import os
import sys
sys.path.append("E:\\untitled") #解决from cnblogs.cnblogSpider.cnblogSpider.items import CnblogspiderItem 会报错无法找到模块cnblogs
import scrapy
from cnblogs.cnblogSpider.cnblogSpider.items import CnblogspiderItem
from scrapy.selector import Selector
class CnblogsSpider(scrapy.Spider): #继承scrapy.Spider
    name ="cnblogs" #爬虫名称 ,注意空格也会被当作名称
    allowed_domains =["cnblogs.com"] #允许的域名
    start_urls={
        # 'https://www.cnblogs.com/qiyeboy/p/9062667.html'
        'https://www.cnblogs.com/qiyeboy/'
    }
    def parse(self,response):
      #解析
        papers = response.xpath(".//*[@class='day']")
        for paper in papers:
            url =paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title=paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            time =paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content=paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            # print(url,title,time,content)
            item=CnblogspiderItem(url=url,title=title,time=time,content=content)
            request= scrapy.Request(url=url,callback=self.pares_body)
            request.meta['item'] =item  #将item暂存
            yield request
        next_page=Selector(response).re(u'<a href="(\S*)">下一页</a>')
        if next_page:
            yield scrapy.Request(url=next_page[0],callback=self.parse)
    def pares_body(self,response):
        item= response.meta['item']
        body=response.xpath(".//*[@class='postBody']")
        item['image_urls']=body.xpath('.//img//@src').extract() #提取图片链接
        yield item


if __name__ == '__main__':
    run=CnblogsSpider()