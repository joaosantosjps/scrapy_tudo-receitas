# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import csv
from crawlers.items import CrawlersItem


class CrawlersPipeline:
    def open_spider(self, spider):
        filename = f"{spider.name}.csv"
        self.headers = CrawlersItem().keys()

        if "data" not in os.listdir("crawlers/"):
            os.mkdir("crawlers/data/")
        
        self.file = csv.DictWriter(
            open(f"crawlers/data/{filename}", "w", newline="", encoding="utf-8"),
            fieldnames=self.headers,
            delimiter=";",
        )
        self.file.writeheader()

    def process_item(self, item, spider):
        for header in self.headers:
            item[header] = self.string_process(item[header])
        self.save_to_csv(item=item)
        
        return item
   
    def save_to_csv(self, item):
        self.file.writerow(dict(item))

    def string_process(self, itens):
        if itens and isinstance(itens, str):
            return itens.strip()
        elif itens and isinstance(itens, list):
            return ",".join(itens)
        else:
            return itens
