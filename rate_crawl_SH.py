#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import datetime
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML


# In[2]:


display(HTML("<style>.container { width:90% !important; }</style>"))


# # 한국은행 기준금리

# In[3]:


base_url= "https://www.bok.or.kr/portal/singl/baseRate/list.do?dataSeCd=01&menuNo=200643"
resp = requests.get(base_url, 'html.parser')
soup= BeautifulSoup(resp.text, 'lxml')


# In[4]:


dict_list= []

for i in range(45):
    dict_list.append({
        'DATE': pd.to_datetime(datetime.datetime.strptime(soup.find_all('td')[3*i].text + soup.find_all('td')[3*i+1].text, '%Y%m월 %d일')),
        'RATE': float(soup.find_all('td')[3*i+2].text)
    })


# In[5]:


pd_result= pd.DataFrame(dict_list)

# 원하는 전체 date range
idx= pd.date_range(pd_result.DATE.min(), pd_result.DATE.max())
idx= pd.Series(idx)


# In[25]:


# 없는 행에 Nan을 넣어 병합한 후 Nan값을 이전 값으로 메꾸기
baserate= pd.concat([pd.DataFrame({'DATE': idx[~idx.isin(pd_result.DATE)], 'RATE': np.nan}),pd_result]).sort_values('DATE').reset_index(drop=True).ffill(axis=0)


# In[29]:


baserate


# In[26]:


baserate.to_csv('./baserate.csv')


# # 콜금리

# In[15]:


base_url2= "https://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_CALL&page={}"


# In[16]:


page_num= 377


# In[17]:


soup_list2= []

for i in range(1,page_num+1):
    soup_list2.append(BeautifulSoup(requests.get(base_url2.format(i), 'html.parser').text,'lxml').find_all('td'))


# In[18]:


result_list2= []

for lists in soup_list2:
    for i in range(len(lists)//4):
        result_list2.append({
            'DATE': lists[4*i].text.strip(),
            'RATE': float(lists[4*i+1].text)
        })


# In[19]:


pd_result2= pd.DataFrame(result_list2)
pd_result2.DATE= pd_result2.DATE.astype('datetime64')


# In[20]:


# 원하는 전체 date range
idx2= pd.date_range(pd_result2.DATE.min(), pd_result2.DATE.max())
idx2= pd.Series(idx2)


# In[27]:


# 없는 행에 Nan을 넣어 병합한 후 Nan값을 이전 값으로 메꾸기
callrate= pd.concat([pd.DataFrame({'DATE': idx2[~idx2.isin(pd_result2.DATE)], 'RATE': np.nan}),pd_result2]).sort_values('DATE').reset_index(drop=True).ffill(axis=0)[1:]


# In[30]:


callrate


# In[28]:


callrate.to_csv('./callrate.csv')

