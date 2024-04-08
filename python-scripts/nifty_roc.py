
# Rate of Change code

# Load the necessary packages and modules
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import yfinance
import pandas as pd
yfinance.pdr_override()
# Rate of Change (ROC)
def ROC(data,n):
 N = data['Adj Close'].shift(0)
 D = data['Adj Close'].shift(n)
 ROC = pd.Series(N/D,name='Rate of Change')
 data = data.join(ROC)
 return data

# Retrieve the NIFTY data from Yahoo finance:
data = pdr.get_data_yahoo("^NSEI", start="2021-06-01", end="2024-04-10")
data = pd.DataFrame(data)

# Compute the 5-period Rate of Change for NIFTY
n = 65
NIFTY_ROC = ROC(data,n)
ROC = NIFTY_ROC['Rate of Change']
filename = "files/nifty.csv"
NIFTY_ROC.to_csv(filename, sep='\t')
# Plotting the Price Series chart and the Ease Of Movement below
fig = plt.figure(figsize=(7,5))
ax = fig.add_subplot(2, 1, 1)
ax.set_xticklabels([])
plt.plot(data['Adj Close'],lw=1)
plt.title('NSE Price Chart')
plt.ylabel('Close Price')
plt.grid(True)
bx = fig.add_subplot(2, 1, 2)
plt.plot(ROC,'k',lw=0.75,linestyle='-',label='ROC')
plt.legend(loc=2,prop={'size':9})
plt.ylabel('ROC values')
plt.grid(True)
plt.setp(plt.gca().get_xticklabels(), rotation=30)
