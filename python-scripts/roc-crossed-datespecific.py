# Rate of Change code

# Load the necessary packages and modules
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import yfinance
import pandas as pd
import requests
import csv
from collections import deque
import os.path
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("-checkemas", "--checkemas", help="Ema Check.", type=bool, default=True)
parser.add_argument("-date", "--date", help="ops for date.", type=str, default="")
args = parser.parse_args()

n=65
stockinddict = {}
stockcalculated = {}
stocksector={}
finalstocks=[]
with open('Stocks_List.csv') as file_obj:
  reader_obj = csv.reader(file_obj)
  next(reader_obj)
  for row in reader_obj:
      if(row[5] == 'Common Stock' and row[10]!=""):
          stocksector[row[0]] = row[10]
          if(row[10] in stockinddict):
              count = stockinddict[row[10]]
              count = count + 1;
              stockinddict[row[10]] = count
          else:
              stockinddict[row[10]] = 1

with open('NSE_LIST_OF_SYMBOLS.csv') as file_obj: 
  reader_obj = csv.reader(file_obj) 
  next(reader_obj)
  for row in reader_obj:
    if(os.path.isfile("files/"+row[0]+".csv") and args.checkemas==True):
      df = pd.read_csv("files/"+row[0]+".csv", delimiter='\t')
      dfvalues = df[df['date']==args.date]
      if(len(dfvalues['volume'])>0 and float(dfvalues['volume'].item())>(float(dfvalues['10VOLEMA'].item())*1.25) and float(dfvalues['adjusted_close'].item())>(float(dfvalues['20EMA'].item())) and row[0] in stocksector and row[0] not in finalstocks):
        FACTOR = float(dfvalues['close'].item())/float(dfvalues['adjusted_close'].item())
        OPENWITHFACTOR = float(dfvalues['open'].item())/FACTOR
        CLOSEWITHFACTOR = float(dfvalues['adjusted_close'].item())
        if(CLOSEWITHFACTOR-OPENWITHFACTOR > float(dfvalues['ATR14'].item())*1.3):
           if(stocksector[row[0]] in stockcalculated):
               #print(row[0])
               countstock = stockcalculated[stocksector[row[0]]]
               #print(countstock)
               countstock = countstock + 1;
               stockcalculated[stocksector[row[0]]] = countstock;
           else:
               stockcalculated[stocksector[row[0]]] = 1;
           finalstocks.append(row[0])
           print("with emas "+row[0]);
           #break


f = open('result.csv', 'w')
w = csv.writer(f, delimiter = ',')
header=[]
header.append("Secror")
header.append("Total stocks in Sector")
header.append("Total stocks satisfying")
header.append("% stocks")
w.writerow(header)
for key, value in stockinddict.items():
    data = []
    if(key in stockcalculated):
     calculatedvalue = (stockcalculated[key]/stockinddict[key])*100
    else:
        calculatedvalue = 0
    print("Sector name: " + key + "Total stocks "+ str(stockinddict[key])  +" Percentage: " + str(calculatedvalue))
    data.append(key)
    data.append(str(stockinddict[key]))
    if(key in stockcalculated):
     data.append(str(stockcalculated[key]))
    else:
     data.append(0)
    data.append(str(calculatedvalue)+"%")
    w.writerow(data);
#print(stockcalculated)
f.close()


f1 = open('stocksector.csv', 'w')
w1 = csv.writer(f1, delimiter = ',')
for key in finalstocks:
  data1=[]
  data1.append(key)
  data1.append(stocksector[key])
  w1.writerow(data1)
f1.close()
