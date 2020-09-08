# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import JsonLinesItemExporter


class NaverCrawlerPipeline:
    def process_item(self, item, spider):

        dirName = "crawled"
        if not os.path.exists(dirName):
            os.makedirs(dirName)

        #date = item["date"]
        #filename = "naver_news_final.json"
        filename = "final.json"

        filpath = os.path.join(dirName, filename)

        mode = "wb"

        if os.path.exists(filpath):
            mode = "ab"

        with open(filpath, mode) as f:
            exporter = JsonLinesItemExporter(f, encoding="utf-8")
            exporter.export_item(item)
            return item
