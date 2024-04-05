# Rate of Change code

# Load the necessary packages and modules
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import yfinance
import pandas as pd
import requests
import csv
from collections import deque
import json

import os.path
n=250
import csv
f = open('test_2.csv', 'w')
writer = csv.writer(f, delimiter=",") 
count = 0;
with open('NSE_LIST_OF_SYMBOLS.csv') as file_obj: 
  reader_obj = csv.reader(file_obj) 
  #print("11") 
  next(reader_obj)
  for row in reader_obj:
    count = count + 1;
    if(count<1500):
        continue;
    api_key = 'YOUR API KEY'
    api_url= f'https://eodhd.com/api/fundamentals/'+row[0]+'.NSE?api_token=""&fmt=xlsx'
    raw_df = requests.get(api_url).json()
    #stock_data = pd.DataFrame(raw_df)
    #print(api_url)
    #print(raw_df.keys())
    if 'General' in raw_df:
      if 'Sector' in raw_df['General']:
        element = []
        element.insert(len(element),raw_df['General']['Sector']);
        element.insert(len(element),raw_df['General']['Industry']);
        element.insert(len(element),raw_df['General']['GicSector']);
        element.insert(len(element),raw_df['General']['GicGroup']);
        element.insert(len(element),raw_df['General']['GicIndustry']);
        element.insert(len(element),raw_df['General']['GicSubIndustry']); 
        #row.extend([raw_df['General']['Sector']]) 
        #row.extend(raw_df['General']['Industry'])
        #row.extend(raw_df['General']['GicSector'])
        #row.extend(raw_df['General']['GicGroup'])
        #row.extend(raw_df['General']['GicIndustry'])
        #row.extend(raw_df['General']['GicSubIndustry'])
        print(element)
        row.extend(element)
  #write.writerow("111")
    print(row)
    writer.writerow(row)
    f.flush()
f.close()
#f.close()
   


    #json_dict = json.loads(raw_df)
    #print(json_dict) 
    #print(row[0])
    #if(os.path.isfile("files/"+row[0]+"_rs.csv")):
      #with open("files/"+row[0]+"_rs.csv", mode='r') as infile:
         #print(infile)
  
