##
## File: hx8rc-assignment10.py
## Topic: Assignment 10
## Name: Eric Xie
## Section time: 3:30-4:45
## Grading Group: 6
##

import pandas as pd
import glob
import datetime

df = pd.DataFrame() # Instantiate a dataframe to hold all records
filelist = glob.glob('Stocks/*.csv') # Get list of all csv files in Stocks folder
for filename in filelist: # Iterate through all filenames
    newdf = pd.read_csv(filename) # Read the csv as a df
    newdf['Ticker'] = pd.Series([filename[7:-4] for x in range(len(newdf))]) # Add stock ticker as a column
    df = pd.concat([df, newdf]) # Concat df for this file to overall df

## 1.
print('Open:', df['Open'].mean()) # Calculate mean open price
print('High:', df['High'].mean()) # Calculate mean high price
print('Low:', df['Low'].mean()) # Calculate mean low price
print('Close:', df['Close'].mean()) # Calculate mean close price

'''
1.
Open: 50.86385220906213
High: 51.459411725747884
Low: 50.25336771426483
Close: 50.876481580135426
'''

## 2.
# Group by ticker name, and calculate the mean Close price for each stock and sort them
by_close = df.groupby('Ticker')['Close'].mean().sort_values()
print("Top 5 Close:\n", by_close[-5:]) # Splice out the top 5 stocks
print("Bottom 5 Close:\n", by_close[:5]) # Splice out the bottom 5 stocks

'''
2.
Top 5 Close:
GS      139.146781
BLK     164.069088
AMZN    185.140534
AZO     235.951950
CME     253.956017

Bottom 5 Close:
FTR      8.969515
F       11.174158
XRX     11.291864
ETFC    12.808103
HBAN    13.697483
'''

## 3.
df['Volatility'] = df['High'] - df['Low'] # Calculate volatility for each record and store in new column
by_volatility = df.groupby('Ticker')['Volatility'].mean().sort_values() # Find mean volatility for each stock and sort
print("Top 5 Volatility:\n", by_volatility[-5:]) # Splice out the top 5 stocks
print("Bottom 5 Volatility:\n", by_volatility[:5]) # Splice out the bottom 5 stocks

'''
3.
Top 5 Volatility:
ICE     4.056189
AZO     4.330294
BLK     4.470693
AMZN    4.691407
CME     7.697287

Bottom 5 Volatility:
FTR     0.205275
XRX     0.308743
F       0.323567
HBAN    0.343893
NI      0.363250
'''

## 4.
# Calculate Relative Volatility and store in new column
df['Rel_Volatility'] = df['Volatility']/(0.5 * (df['Open']+df['Close']))
# Group by stock and calculate mean Relative Volatility for each, and sort those values
by_rel_volatility = df.groupby('Ticker')['Rel_Volatility'].mean().sort_values()
print("Top 5 Relative Volatility:\n", by_rel_volatility[-5:]) # Splice out the top 5 stocks
print("Bottom 5 Relative Volatility:\n", by_rel_volatility[:5]) # Splice out the bottom 5 stocks

'''
4.
Top 5 Relative Volatility:
ETFC    0.045381
REGN    0.048172
EQIX    0.051295
LVLT    0.054870
AAL     0.055533

Bottom 5 Relative Volatility:
GIS    0.013966
PG     0.014192
K      0.014992
CL     0.015521
WEC    0.015761
'''

# 5.
feb_2010 = df[df['Date'].str[:7] == '2010-02'] # Extract only records in Feb 2010
print(feb_2010.groupby('Date')['Open','High','Low','Close','Volume'].mean()) # Average all the required columns

'''
5.
                 Open       High        Low      Close        Volume
Date                                                                
2010-02-01  42.267199  42.935162  41.912471  42.704181  7.200101e+06
2010-02-02  42.573926  43.308290  42.178253  43.083780  7.996646e+06
2010-02-03  43.074528  43.519709  42.596412  42.996122  7.173997e+06
2010-02-04  42.869744  43.069415  41.666130  41.799597  9.732287e+06
2010-02-05  41.487291  41.987255  40.569602  41.628338  1.075256e+07
2010-02-08  41.954153  42.400403  41.349668  41.565881  7.132838e+06
2010-02-09  41.371208  41.952746  40.934578  41.500219  7.972704e+06
2010-02-10  41.783087  42.167315  41.212389  41.722352  6.744782e+06
2010-02-11  41.814452  42.595182  41.417809  42.391167  7.037806e+06
2010-02-12  41.403247  41.989561  41.018028  41.823831  7.246792e+06
2010-02-16  42.663708  43.217454  42.331781  43.075126  6.649753e+06
2010-02-17  43.571721  43.954541  43.134688  43.627508  6.623697e+06
2010-02-18  43.396970  43.983284  43.125218  43.769598  6.460454e+06
2010-02-19  43.390687  44.013586  43.154311  43.704347  6.660305e+06
2010-02-22  44.004548  44.280432  43.455306  43.785487  6.427562e+06
2010-02-23  43.152945  43.468508  42.491308  42.754581  7.270832e+06
2010-02-24  43.480865  44.004945  43.167400  43.755306  6.697727e+06
2010-02-25  43.201386  43.893284  42.772043  43.771350  7.895413e+06
2010-02-26  43.703560  44.084712  43.281258  43.767877  7.223996e+06
'''

## 6.
records_2012 = df[df['Date'].str[:4] == '2012'] # Extract all records from 2012
by_date = records_2012.groupby('Date')['Rel_Volatility'].mean() # Calculate average Relative Volatility for each day
print('Max:', by_date.idxmax()) # Print date of the highest mean Relative Volatility
print('Min:', by_date.idxmin()) # Print date of the lowest mean Relative Volatility

'''
6.
Max: 2012-06-21
Min: 2012-12-24
'''

## 7.
df['Date'] = pd.to_datetime(df['Date'], yearfirst=True) # Convert Date column to datetime objects
df['DayOfWeek'] = df['Date'].dt.strftime('%A') # Extract day of week from datetime and save as new column
# Extract records within the specified date range
within_range = df[(datetime.datetime(2008, 1, 1) <= df['Date']) & (df['Date'] <= datetime.datetime(2013, 12, 31))]
# Group by day of week and calculate avg Relative Volatility for each day
by_day = within_range.groupby('DayOfWeek')['Rel_Volatility'].mean()
print(by_day)

'''
7.
DayOfWeek
Friday       0.029041
Monday       0.028542
Thursday     0.031066
Tuesday      0.029436
Wednesday    0.029766
'''

## 8.
# Extract records in Oct 2010
oct2010 = df[df['Date'].dt.strftime('%Y-%m') == '2010-10']
# Calculate the weighted prices for each of Open, High, Low, and Close
oct2010['OpenW'] = oct2010['Open']*oct2010['Volume']
oct2010['HighW'] = oct2010['High']*oct2010['Volume']
oct2010['LowW'] = oct2010['Low']*oct2010['Volume']
oct2010['CloseW'] = oct2010['Close']*oct2010['Volume']
# Group by date and sum the columns relevant to the formula
by_date = oct2010.groupby('Date')['OpenW','HighW','LowW','CloseW','Volume'].sum()
pyindex = pd.DataFrame() # Initialize a df to store the python index
# For each of Open, High, Low, and Close, divide the numerator Series by denominator
pyindex['Open'] = by_date['OpenW']/by_date['Volume']
pyindex['High'] = by_date['HighW']/by_date['Volume']
pyindex['Low'] = by_date['LowW']/by_date['Volume']
pyindex['Close'] = by_date['CloseW']/by_date['Volume']
print(pyindex)

'''
8.
                 Open       High        Low      Close
Date                                                  
2010-10-01  39.272779  39.540464  38.574467  38.961689
2010-10-04  36.513664  36.973598  36.039906  36.473198
2010-10-05  36.868819  37.448798  36.515236  37.154517
2010-10-06  40.069422  40.526281  38.790438  39.453984
2010-10-07  38.738979  38.982299  38.023149  38.494185
2010-10-08  33.953131  34.418515  33.601610  34.141493
2010-10-11  36.415035  36.840357  35.996804  36.331342
2010-10-12  36.550699  37.148552  36.185750  36.956121
2010-10-13  36.769845  37.277431  36.410377  36.830507
2010-10-14  31.929174  32.188759  31.399433  31.746258
2010-10-15  31.379396  31.574286  30.611508  31.058207
2010-10-18  34.735203  35.208943  34.389509  34.947873
2010-10-19  33.418144  33.812511  32.833834  33.171654
2010-10-20  33.225863  33.908320  32.849706  33.555329
2010-10-21  40.968005  41.634092  40.219655  40.945613
2010-10-22  40.206448  40.821101  39.843407  40.424731
2010-10-25  35.196479  35.525335  34.779042  35.002647
2010-10-26  37.425957  38.443149  37.176602  38.095958
2010-10-27  40.800620  41.430831  40.293345  40.981265
2010-10-28  38.377249  38.645428  37.617353  38.085284
2010-10-29  40.159713  40.638799  39.741861  40.279059
'''


