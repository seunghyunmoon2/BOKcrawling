# # 콜금리

# In[15]:


base_url2= "https://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_CALL&page={}"


# In[16]:


page_num = 381


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



callrate.to_csv('./mod_callrate.csv')
#여기까지가 수한님꺼 수정

# %%
# 먼저읽어와야함
callrate['shift'] = callrate['RATE'].shift(periods=30, fill_value=0)

# %%
callrate

# %%

# 왜안되냐...
# def labeler(x):
#   if (callrate['RATE'] - callrate['shift']) > 0 : return 'up'
#   elif (callrate['RATE'] - callrate['shift']) == 0: return 'neutral'
#   else: return 'down'
#callrate['label'] = callrate.apply(labeler, axis=1)

# %%

# %%
conditions = [
    (callrate['RATE'] - callrate['shift']) > 0,
    (callrate['RATE'] - callrate['shift']) < 0
]

choices = ['up','down']

callrate['label'] = np.select(conditions, choices, default='neutral')

# %%
callrate

# %%
callrate['label'].value_counts()

# %%
callrate.to_csv('./labeled_callrate.csv')
