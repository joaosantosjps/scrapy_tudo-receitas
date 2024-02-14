# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlersItem(scrapy.Item):
    url = scrapy.Field()
    titulo = scrapy.Field()
    dificuldade = scrapy.Field()
    quantidade = scrapy.Field()
    tempo = scrapy.Field()
    categoria = scrapy.Field()

    def keys(self):
        return [
            "categoria",
            "titulo",
            "url",
            "dificuldade",
            "quantidade",
            "tempo",
        ]