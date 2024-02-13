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
            difficulty = block_product.xpath('div[@class="info_snippet"]/span/text()').extract_first()
            portion = block_product.xpath('div[@class="properties"]/span[@class="property comensales"]/text()').extract_first()
            time = block_product.xpath('div[@class="properties"]/span[@class="property duracion"]/text()').extract_first()
        for category_all in response.xpath('//div[@class="titulo titulo--search"]'):
            category = category_all.xpath('h1/text()').extract_first()

            yield {
                "Url": url_products,
                "Titulo": name_products,   
                "Dificuldade": difficulty,
                "Quantidade": portion,
                "Tempo": time,
                "Categoria": category
            }

            