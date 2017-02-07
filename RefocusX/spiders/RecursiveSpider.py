from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from RefocusX.items import RefocusxItem

class RecursiveSpider(CrawlSpider) :
    name = "rxspider"
    allowed_domains = ["epicurious.com"]
    start_urls=["http://www.epicurious.com/"]

    rules = (
        Rule(SgmlLinkExtractor(allow=("/recipes/food/views/.*" ,)), callback='parse_item', follow =True),
        )
    
    def parse_item(self,response) :
        sel = Selector(response)
        item = RefocusxItem()
        item['url'] = response.request.url
        item['ingredients'] = sel.xpath('/html/body/div[2]/div[1]/div[3]/div/div[1]/div[5]/div[1]/div[2]/ol/li/ul/li/text()').extract()                                        
        item['recipe'] = sel.xpath('.//*[@class="preparation-groups"]/li/ol/li/text()').extract()
        return item


