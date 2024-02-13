# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CrawlersPipeline:
    def process_item(self, item, spider):
        item["Titulo"] = self.string_process(item["Titulo"])
        item ["Dificuldade"] = self.string_process(item["Dificuldade"])
        item["Quantidade"] = self.string_process(item["Quantidade"])
        item["Tempo"] = self.string_process(item["Tempo"])
        item["Categoria"] = self.string_process(item["Categoria"])
        return item
    
    def string_process(self, string):
        if string:
            return string.strip()
        return None
