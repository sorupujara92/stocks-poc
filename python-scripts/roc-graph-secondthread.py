# Rate of Change code

# Load the necessary packages and modules
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import yfinance
import pandas as pd
import requests
import csv
import collections
import pandas_ta as ta
from ta.volatility import AverageTrueRange
import os.path

yfinance.pdr_override()


# Rate of Change (ROC)
def calc_ROC(data,niftydf,n):
 N = data['adjusted_close'].shift(0)
 D = data['adjusted_close'].shift(n)
 FACTOR = data['close'].shift(0)/N
 #stockroc = data['Rate of Change'].shift(0)
 #print(data)
 #print(niftydf)
 niftyroc = niftydf['Rate of Change'].shift(0)
 try:
  arrATR = AverageTrueRange(high=data['high']/FACTOR,low=data['low']/FACTOR,close=data['adjusted_close'],window=14).average_true_range()
 except Exception:
  print("exception")
  arrATR=""
  pass
 #print(N)
 #DICTF = float(mydictframe.shift(0))
 #print(DICTF)
 #RC = float(mydict[data['date']])
 #print(calc)
 #print(data['date'][1])
 #print(float(mydict[data['date'][1]]))
 #print(calc/RC)
 ROC = pd.Series(N/D,name='Rate of Change')
 data = data.join(ROC)
 EMA = ta.ema(data["adjusted_close"], length=20, fillna="")
 #RSSTOCK = pd.Series((N/D)/niftyroc,name="StockRS")
 VOLUME = ta.ema(data["volume"], length=20, fillna="")
 EMACSV = pd.Series(EMA,name='20EMA')
 VOLUMECSV = pd.Series(VOLUME,name='20VOLEMA')
 ATRCSV = pd.Series(arrATR,name="ATR14")
 data = data.join(EMACSV)
 data = data.join(VOLUMECSV)
 data = data.join(ATRCSV)
 #data = data.join(RSSTOCK)
 #RS = pd.Series((N/D)/DICTF,name='RS')
 #data = data.join(RS)
 return data 

mydict = {}
#dictloop=0
with open('files/nifty.csv', mode='r') as infile:
    for line in infile:
        #dictloop = dictloop + 1;
        #if(dictloop==1):
        #    continue;
        data_line = line.rstrip().split('\t')
        if(len(data_line) > 7):
         mydict[data_line[0]] = data_line[7];
        else:
         mydict[data_line[0]] = 1    
#mydictframe = pd.DataFrame(mydict.values())
#print(mydictframe)
# Retrieve the NIFTY data from Yahoo finance:
n = 65
niftydf = pd.read_csv("files/nifty.csv",delimiter="\t")

niftyloop=0
with open('NSE_LIST_OF_SYMBOLS.csv') as file_obj: 
  reader_obj = csv.reader(file_obj) 
  next(reader_obj)
  for row in reader_obj:
    if(row[5]!='Common Stock'):
        continue;
    niftyloop = niftyloop+1
    if(niftyloop > 1000):
      if(os.path.isfile("files/"+row[0]+".csv")):
          continue
      api_key = 'YOUR API KEY'
      api_url= f'https://eodhd.com/api/eod/'+row[0]+'.NSE?from=2022-01-01&api_token=""&fmt=json'
      #api_url = f'https://eodhistoricaldata.com/api/technical/'+row[0]+'.NSE?order=a&fmt=json&from="2023-01-01"&function=splitadjusted&api_token='
      print(api_url)
      #niftydf = pd.read_csv("files/nifty.csv",delimiter="\t")
      #niftydfvalue = pd.DataFrame(niftydf)
      #print(niftydf)
      #print(niftydfvalue)
      raw_df = requests.get(api_url).json()
      stock_data = pd.DataFrame(raw_df)
      #n = 100
      #print(stock_data)
      STOCK_ROC = calc_ROC(stock_data,niftydf,n)
      #ROC = STOCK_ROC['Rate of Change']
      filename = "files/"+row[0]+".csv"
      STOCK_ROC.to_csv(filename, sep='\t')
      with open("files/"+row[0]+".csv", mode='r') as infile:
        rscalc = collections.OrderedDict()
        for line in infile:
            data_line = line.rstrip().split('\t')
            if(data_line[1] in mydict and len(data_line) > 8 and data_line[8]!=""):
              rscalc[data_line[1]] = float(data_line[8])/float(mydict[data_line[1]])
              pd.DataFrame.from_dict(data=rscalc, orient='index').to_csv("files/"+row[0]+"_rs.csv", header=False)

#data = pdr.get_data_yahoo("^NSEI", start="2015-06-01", end="2016-01-01") 

#print(data)
#data = pd.DataFrame(data)

# Compute the 5-period Rate of Change for NIFTY
#n = 100
#NIFTY_ROC = ROC(data,n)
#ROC = NIFTY_ROC['Rate of Change']
#print(ROC)
#filename = "university_records.csv"
#NIFTY_ROC.to_csv(filename, sep='\t')
 
# writing to csv file


# Plotting the Price Series chart and the Ease Of Movement below
#fig = plt.figure(figsize=(7,5))
#ax = fig.add_subplot(2, 1, 1)
#ax.set_xticklabels([])
#plt.plot(data['close'],lw=1)
#plt.title('NSE Price Chart')
#plt.ylabel('Close Price')
#plt.grid(True)
#bx = fig.add_subplot(2, 1, 2)
#plt.plot(ROC,'k',lw=0.75,linestyle='-',label='ROC')
#plt.legend(loc=2,prop={'size':9})
#plt.ylabel('ROC values')
#plt.grid(True)
#plt.setp(plt.gca().get_xticklabels(), rotation=30)
