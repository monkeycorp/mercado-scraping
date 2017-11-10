#Import item field
import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from mercado.items import MercadoItem

class MercadoSpider(CrawlSpider):
	name = 'mercado'
	item_count = 0
	allowed_domain = ['www.mercadolibre.com.mx']
	start_url = ['https://listado.mercadolibre.com.mx/consolas-videojuegos#D[A:consolas-videojuegos,B:5]']

	rules = {
		# Para cada item
		Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="pagination__next"]/a'))),
		Rule(LinkExtractor(allow =(), restrict_xpaths = ('//h2[contains(@class,"item__title")]/a')),
							callback = 'parse_item', follow = False)
	}

	def parse_item(self, response):
		product = MercadoItem()

		#get info product
		product['titulo'] = response.xpath('normalize-space(//h1[@class="item-title__primary"]/text())').extract_firts()
		#Maximo de productos 
		self.item_count += 1
		if self.item_count > 20:
			raise CloseSpider('item_exceeded')
		yield product
