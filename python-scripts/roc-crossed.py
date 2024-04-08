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
n=65
stockinddict = {}
stockcalculated = {}
stocksector={}
finalstocks=[]
with open('Stocks_List.csv') as file_obj:
  reader_obj = csv.reader(file_obj)
  next(reader_obj)
  for row in reader_obj:
      if(row[5] == 'Common Stock' and row[8]!=""):
          stocksector[row[0]] = row[8]
          if(row[8] in stockinddict):
              count = stockinddict[row[8]]
              count = count + 1;
              stockinddict[row[8]] = count
          else:
              stockinddict[row[8]] = 1


with open('NSE_LIST_OF_SYMBOLS.csv') as file_obj: 
  reader_obj = csv.reader(file_obj) 
  next(reader_obj)
  for row in reader_obj:
    if(os.path.isfile("files/"+row[0]+".csv")):
      with open("files/"+row[0]+".csv", mode='r') as infile:
          q = deque(infile, n) 
          high = 0
          loop = 0;
          for i in q:
              #print(i)
              data_line = i.rstrip().split(",")[12]
              if(loop<n-4):
                if(float(data_line)>float(high)):
                    high = data_line
              else:
                #if(row[0] == "HDFCLIFE"):
                #  print(data_line)
                #  print(loop)

                if(data_line>high and row[0] in stocksector):
                    if(stocksector[row[0]] in stockcalculated):
                        #print(row[0])
                        countstock = stockcalculated[stocksector[row[0]]]
                        #print(countstock)
                        countstock = countstock + 1;
                        stockcalculated[stocksector[row[0]]] = countstock;
                    else:
                        stockcalculated[stocksector[row[0]]] = 1;
                    finalstocks.append(row[0])    
                    print(row[0]);
                    break
              loop = loop+1;
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
     print(key)
     print(stockinddict)
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
