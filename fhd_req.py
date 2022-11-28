# Запрос данных о плане ФХД с сервера bus.gov.ru

#%% import modules

import urllib.request 
import json
import csv
# import time
import pandas as pd
# import certifi

#%% Certificate workaround (unsafe!)
import ssl

from pandas.core.indexes.base import Index
ssl._create_default_https_context = ssl._create_unverified_context


# %% request url
baseurl ='https://kpak.app.gmu.dks.lanit.ru/public-rest/api/epbs/fap?'
s_type = 'inn='
testinn = '2437000076'
# jsn = urllib.request.urlopen(baseurl + s_type + testinn)
jsn = urllib.request.urlopen('https://kpak.app.gmu.dks.lanit.ru/public-rest/api/epbs/fap?inn=2437000076')
parsed_string = json.loads(jsn)

# %%
with open('files\sochi.json', encoding='utf-8') as f:
  data = json.load(f)
#%%
otch = {
    'Name':data['content'][1]['common']['fullClientName'],
    'FinYear':data['content'][1]['common']['financialYear'],
    'TotalRev':data['content'][0]['planPaymentIndexesMain'][0]['total'],
    'SobsRev':data['content'][0]['planPaymentIndexesMain'][0]['serviceTotal'],
    'CapGrant':data['content'][0]['planPaymentIndexesMain'][0]['capitalInvestment']
}
print(otch)
# %%
indic = data['content'][0]['planPaymentIndexes']
otch2 = {'park':data['content'][1]['common']['fullClientName'],
          'data':{}
}

for i in indic:
  otch2['data'][i['name']] =  float(i['total'])
  
# %%
df = pd.DataFrame.from_dict(otch2)
# %%
to = {'name': 'testname',
      'data': {
        'p1':0,
        'p2':1
      }
}
# %%


df2 = pd.DataFrame.from_dict(to)
# %%
df3 = pd.json_normalize(indic)
df3['Comp'] = data['content'][1]['common']['fullClientName']
# %%
df4 = pd.DataFrame()
for i in data['content']:
  obj = pd.json_normalize(i['planPaymentIndexes'])
  N = i['common']['fullClientName']
  Y = i['common']['financialYear']
  obj['year'] = Y
  obj['company'] = N
  df4.append(obj, ignore_index=True)
  print(obj)
# %%
