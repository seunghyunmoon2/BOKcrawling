import datetime
import pandas as pd
import re

import scrapy
from naver_crawler.items import NaverCrawlerItem
from datetime import timedelta, date, datetime
from pandas.tseries.offsets import MonthEnd

date_pattern = re.compile(r"ds=(\d{4}.\d{2}.\d{2})")
page_pattern = re.compile(r"&start=(\d+)&")


class NaverSpider(scrapy.Spider):
    name = "navernewsfinal"
    crawled_url = []
    #startdate = str(date.today()) #   1990-01-01
    #enddate = str(date.today())   #   2010-01-01  
    #date.today() -> datetime.date(2020, 9, 2)  str() ->  '2020-09-02'

    #startdates = pd.date_range(start='2010-01-01', end='2020-08-31', freq='MS')
    #enddates = startdates + MonthEnd(1)

    startdate = '2010-01-01'
    enddate = '2020-08-01'

    def __init__(self, start="", end="", exportdir=".", exporttype="json"):
        self.end_date = (
            datetime.strptime(self.enddate, "%Y-%m-%d")
            if end == ""
            else datetime.strptime(end, "%Y-%m-%d")
        )
        self.start_date = (
            datetime.strptime(self.startdate, "%Y-%m-%d")
            if start == ""
            else datetime.strptime(start, "%Y-%m-%d")
        )

    def start_requests(self):

        urls = []
        for cur_date in pd.date_range(self.start_date, self.end_date, freq = 'MS'):
            month_start_date, month_end_date = cur_date.strftime("%Y.%m.%d"), (cur_date + MonthEnd(1)).strftime("%Y.%m.%d")
            url = "https://search.naver.com/search.naver?&where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_pge&sort=1&photo=0&field=0&reporter_article=&pd=3&ds={0}&de={1}&docid=&nso=so:dd,p:,a:all&mynews=1&start=1&refresh_start=0".format(
                month_start_date, month_end_date
            )

            urls.append(url)
        
        for url in urls:
            yield scrapy.Request(url=url, 
                                cookies={"news_office_checked": "1001,1018,2227"},
                                callback=self.parse_list)
    
    def get_num(self, num_str):
        num = 0
        for i in range(len(num_str)):
            num += int(num_str[i])
        return num

    def parse_list(self, response):
        self.logger.critical(response.url)
        if response.url not in self.crawled_url:
            self.crawled_url.append(response.url)
            articles = response.xpath("//dd[@class='txt_inline']")

            for article in articles:
                media = (
                    article.xpath("./span[@class='_sp_each_source']/text()")
                    .get()
                    .strip()
                )

                if media in ["연합뉴스", "이데일리"]:
                    page_url = article.xpath("./a/@href").get()
                else:
                    page_url = article.xpath("../dt/a/@href").get()

                cur_date = re.findall(r"ds=(\d{4}.\d{2}.\d{2})", response.url)[0]

                yield scrapy.Request(
                    page_url,
                    callback=self.parse_page,
                    meta={"media": media
                        ,"date": response.css('dd.txt_inline::text')[1].get().strip()[:-1]},
                )

        # cur_page = re.findall(r"&start=(\d+)&", response.url)[0]

        # if self.get_num(cur_page) == int(response.css("div.paging strong::text").get()):
        #     next_page = int(cur_page) + 10
        #     url = re.sub(r"&start=(\d+)&", "&start={}&".format(next_page), response.url)

        #     yield scrapy.Request(
        #         url,
        #         cookies={"news_office_checked": "1001,1018,2227"},
        #         callback=self.parse_list,
        #     )
        next_page = response.css('div.paging a::attr(href)')[-1].get()
        
        if next_page is not None:

            yield response.follow(
                next_page, 
                cookies={"news_office_checked": "1001,1018,2227"}, 
                callback=self.parse_list)

    def parse_page(self, response):
        item = NaverCrawlerItem()
        item["media"] = response.meta["media"]
        item["date"] = response.meta["date"]
        item["url"] = response.url
        if item["media"] in ["연합뉴스", "이데일리"]:
            item["content"] = response.xpath(
                "//div[@id='articleBodyContents']//text()"
            ).getall()
        else:
            item["content"] = response.xpath(
                "//div[@id='article-view-content-div']//text()"
            ).getall()

        yield item

