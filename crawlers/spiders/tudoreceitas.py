import scrapy


class TudoreceitasSpider(scrapy.Spider):
    name = "tudoreceitas"
    allowed_domains = ["tudoreceitas.com"]
    start_urls = ["https://tudoreceitas.com"]

    def parse(self, response):
        for category_all in response.xpath('//a[@class="titulo"]'):
            url = category_all.xpath("@href").extract_first()
            category = category_all.xpath("text()").extract_first()
            
            yield from self.request_category(url=url, category=category)
            
    def request_category(self, url, category, page=1):
           
           yield scrapy.Request(
                url=str(url)+str(page),
                method="GET",
                callback=self.parse_categories, 
                meta={
                    "category": category,
                    "page": page,
                    "url": url
                },
                dont_filter=True
            )



    def parse_categories(self, response):
        meta = response.meta
        category = meta["category"]
        for block_product in response.xpath('//div[@class="resultado link"]'): 
            url_products = block_product.xpath('a[@class="titulo titulo--resultado"]/@href').extract_first()
            name_products = block_product.xpath('a[@class="titulo titulo--resultado"]/text()').extract_first()
            difficulty = block_product.xpath('div[@class="info_snippet"]/span/text()').extract_first()
            portion = block_product.xpath('div[@class="properties"]/span[@class="property comensales"]/text()').extract_first()
            time = block_product.xpath('div[@class="properties"]/span[@class="property duracion"]/text()').extract_first()

            yield {
                "Url": url_products,
                "Titulo": name_products,   
                "Dificuldade": difficulty,
                "Quantidade": portion,
                "Tempo": time,
                "Categoria": category
            }
        next_page = response.xpath('//a[@class="next ga"]').extract_first()
        page = meta["page"]
        url = meta["url"]
        if next_page:
            page += 1
            
            yield from self.request_category(url=url, category=category, page=page)


        
    

            