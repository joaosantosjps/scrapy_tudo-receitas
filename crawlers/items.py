# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlersItem(scrapy.Item):
    url = scrapy.Field()
    titulo = scrapy.Field()
    autor = scrapy.Field()
    dificuldade = scrapy.Field()
    quantidade = scrapy.Field()
    tempo = scrapy.Field()
    categoria = scrapy.Field()
    description = scrapy.Field()
    ingredinets = scrapy.Field()
    preparation = scrapy.Field()

    def keys(self):
        return [
            "url",
            "autor",
            "categoria",
            "titulo",
            "dificuldade",
            "tempo",
            "quantidade",
            "description",
            "ingredinets",
            "preparation",
        ]