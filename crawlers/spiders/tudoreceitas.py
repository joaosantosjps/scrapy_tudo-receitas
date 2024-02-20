import scrapy
from crawlers.items import CrawlersItem
import json


class TudoreceitasSpider(scrapy.Spider):
    name = "tudoreceitas"
    custom_settings = {
        "LOG_LEVEL": "DEBUG"
    }
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
                callback=self.parse_url_products, 
                meta={
                    "category": category,
                    "page": page,
                    "url": url
                },
                dont_filter=True
            )

    def parse_url_products(self, response):
        meta = response.meta
        category = meta["category"]
        for block_product in response.xpath('//div[@class="resultado link"]'): 
            url_products = block_product.xpath('a[@class="titulo titulo--resultado"]/@href').extract_first()
            
            yield scrapy.Request(
                url=url_products,
                method="GET",
                callback=self.parse_preparation_method,
                meta=meta
            )
        
        next_page = response.xpath('//a[@class="next ga"]').extract_first()
        page = meta["page"]
        url = meta["url"]
        if next_page:
            page += 1
            
            yield from self.request_category(url=url, category=category, page=page)

    def parse_preparation_method(self, response):
        meta = response.meta
        category = meta["category"]
        difficulty = response.xpath('//span[@class="property dificultad"]/text()').extract_first()

        for json_method in response.xpath('/html/body/script[@type="application/ld+json"]'):
            method = json_method.xpath('text()').extract_first()
            data = json.loads(method) 

            if isinstance(data, list) and data[0]["@type"] == "Recipe":
                name_products = data[0].get("name")
                name_author = data[0].get("author", {}).get("name")
                portion = data[0].get("recipeYield")
                time = data[0].get("totalTime")
                time = time.replace("PT", "")
                description = data[0].get('description')
                ingredinets = data[0].get("recipeIngredient")

                for preparation_method in data[0]["recipeInstructions"]:
                    preparation = preparation_method["text"]

                yield CrawlersItem(
                    url=response.url,
                    titulo=name_products,
                    autor=name_author,
                    dificuldade=difficulty,
                    quantidade=portion,
                    tempo=time,
                    categoria=category,
                    description=description,
                    ingredinets=ingredinets,
                    preparation=preparation              
                )
