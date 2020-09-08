import pandas as pd

test = pd.read_json(r'./naver_crawler_moon/crawled/final.json', lines=True)

print(test.head())

#print(test.at[1,'content'])