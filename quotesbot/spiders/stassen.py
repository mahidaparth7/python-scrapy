import scrapy
import time

class StassenSpider(scrapy.Spider):
	name = "stassen"
	start_urls = [
		'http://www.stassen.nl/producten',
	]

	def parse(self, response):
	    categories = response.css("div.nav-holder a::attr(href)").extract()
	    for c in categories:
		c = 'http://www.stassen.nl' + c
		yield scrapy.Request(url=c, callback=self.parse_product)
		
	def parse_product(self, response):
	    time.sleep(2)
	    next_page_url = 'http://www.stassen.nl' + response.css('.link_volgende::attr(href)').extract()[0].encode('utf8')
	    
	    for info in response.css('div.item'):
                url = info.css('strong.title a::attr(href)').extract()[0]
                if(url[0] != '/'):
                    url = '/' + url
                url = 'http://www.stassen.nl' + url
	    	yield {
        		'product_name': info.css('strong.title a::text').extract_first(),
    			'url': url,
                        'price': info.css('strong.price::text').extract_first()[1:]
		}
	    if next_page_url is not None:
		yield scrapy.Request(url=next_page_url, callback=self.parse_product)
