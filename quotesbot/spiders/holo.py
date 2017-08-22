import scrapy
import time

class HoboSpider(scrapy.Spider):
	name = "hobo"
	start_urls = [
		'https://www.hobo.nl/hi-fi.html',
                'https://www.hobo.nl/streaming.html',
                'https://www.hobo.nl/home-cinema-beeld.html',
                'https://www.hobo.nl/luidsprekers.html',
                'https://www.hobo.nl/hoofdtelefoons.html',
                'https://www.hobo.nl/kabels.html',
                'https://www.hobo.nl/accessoires.html'
                
	]

	def parse(self, response):
	    time.sleep(2)
	    next_page_url = response.css('a.next::attr(href)').extract()[0].encode('utf8')
	    
	    for info in response.css('li.item'):
	    	yield {
        		'product_name': info.css('p.brand-name::text').extract_first() + ' ' + info.css('h2.product-name::text').extract_first(),
    			'url': response.css('a.product-image::attr(href)').extract()[0],
                        'price': info.css('span.price::text').extract_first().strip()[2:]
		}

	    if next_page_url is not None:
                yield scrapy.Request(url= next_page_url, callback=self.parse)
	    
