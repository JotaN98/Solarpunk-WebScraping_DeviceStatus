import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://console.geodnet.com/4fa3bc0fc013fbd6b89dff9ae2f216efdf3c573d.js?meteor_js_resource=true'

response = requests.get(url)

#soup = BeautifulSoup(response,'html.parser')

with open('page.html','w',encoding='utf-8') as file:
    file.write(response.text)

#for row in soup.findAll('ui mini statistic'):
#    date = row.find('value')
 #   label = row.find('label')
  #  print(date)
   # print(label)

