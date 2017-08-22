import scrapy
import time

class WifimediaSpider(scrapy.Spider):
    name = "wikimedia"
    start_urls = [
        'https://www.wifimedia.eu/nl/',
    ]

    def parse(self, response):
        categories = response.css("a.subsubitemlink::attr(href)").extract()
        for c in categories:
            yield scrapy.Request(url=c, callback=self.parse_product)
            #break	
    def parse_product(self, response):
        time.sleep(2) 
        for info in response.css('div.productborder'):
            brand  = info.css('div.product-title a strong::text').extract_first()
            product_name = info.css('div.product-title a span::text').extract_first()
            yield {
                'product_name': brand + ' '+ product_name,
                'url': info.css('div.product-title a::attr(href)').extract()[0],
                'price': info.css('div.product-price .price::text').extract_first()[1:]
            }
            #break