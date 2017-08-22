import scrapy
import time

class HifiklubbenSpider(scrapy.Spider):
    name = "hifiklubben"
    start_urls = [
        'https://www.hifiklubben.nl/',
    ]

    def parse(self, response):
        categories = response.css("ul.topLevel a::attr(href)").extract()
        #i = 0
        for c in categories:
            c = 'https://www.hifiklubben.nl' + c 
            yield scrapy.Request(url=c, callback=self.parse_product)
            #if(i == 5):
            #   break
            #i = i +1
    def parse_product(self, response):
        time.sleep(2) 
        for info in response.css('article.productCol'):
            yield {
                'product_name':info.css('span.itemName::text').extract_first(),
                'url': 'https://www.hifiklubben.nl' + info.css('a.linkWrapper::attr(href)').extract()[0],
                'price': info.css('span.price::text').extract_first().strip()[1:]
            }
