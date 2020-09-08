import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        ["scrapy", "crawl", "naver", "-a", "start=2020-03-10", "-a", "end=2020-03-10",]
    )
except SystemExit:
    pass
