import scrapy


class TudoreceitasSpider(scrapy.Spider):
    name = "tudoreceitas"
    allowed_domains = ["tudoreceitas.com"]
    start_urls = ["https://tudoreceitas.com"]

    def parse(self, response):
        for url in response.xpath('//a[@class="titulo"]/@href').extract():
            yield scrapy.Request(
                url=url,
                method="GET",
                callback=self.parse_categories
                
            )

    def parse_categories(self, response):
        for block_product in response.xpath('//div[@class="resultado link"]'): 
            url_products = block_product.xpath('a[@class="titulo titulo--resultado"]/@href').extract_first()
            name_products = block_product.xpath('a[@class="titulo titulo--resultado"]/text()').extract_first()
            
            yield {
                "url": url_products,
                "titulo": name_products               
            }

            