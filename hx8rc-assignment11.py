##
## File: hx8rc-assignment11.py
## Topic: Assignment 11
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
df['Date'] = pd.to_datetime(df['Date'], yearfirst=True) # Convert date column to datetime objects
unique_dates = pd.Series(df['Date'].unique()) # Get all unique dates that we have records for
# Mask unique dates according to specified date range
in_range = unique_dates[(datetime.datetime(2005, 1, 2) <= unique_dates) & (unique_dates <= datetime.datetime(2014, 12, 31))]
print(in_range.groupby(in_range.dt.year).count()) # Group by year and count dates per year

'''
1.
2005    252
2006    251
2007    251
2008    253
2009    252
2010    252
2011    252
2012    250
2013    252
2014    252
'''

## 2.
missing = pd.DataFrame() # Prepare df to hold missing records
for ticker in df.groupby('Ticker').groups: # Iterate through unique tickers
    data = df[df['Ticker'] == ticker] # Get records for ticker
    # Find the first and last day this stock appears
    start = data['Date'].min()
    end = data['Date'].max()
    # Get all the dates that the market was open within that interval
    all_dates = unique_dates[(start <= unique_dates) & (unique_dates <= end)]
    # Remove the dates that we have records for to get only missing dates
    missing_recs = all_dates[~all_dates.isin(data['Date'])].reset_index()
    # Build series with just the ticker symbol to serve as the ticker column
    ticker_series = pd.Series([ticker for x in range(len(missing_recs))])
    # Build df with the missing records for this ticker
    newdf = pd.DataFrame({'Date': missing_recs[0], 'Ticker': ticker_series})
    missing = pd.concat([missing, newdf]) # Append missing for this stock to the main missing df
# Mask missing records by specified interval
missing_in_range = missing[(datetime.datetime(2005, 1, 2) <= missing['Date']) & (missing['Date'] <= datetime.datetime(2014, 12, 31))]
print(len(missing_in_range)) # Print length of missing records

'''
2.
9459
'''

## 3.
# Mask records within specified interval
in_range = df[(datetime.datetime(2005, 1, 2) <= df['Date']) & (df['Date'] <= datetime.datetime(2014, 12, 31))]
# Build an empty series indexed by a list of unique tickers
tickers_with_records = pd.Series(index=in_range['Ticker'].drop_duplicates())
# Group the missing records by ticker and count their frequency
missing_by_ticker = missing_in_range.groupby('Ticker')['Ticker'].count()
# Align all tickers with the counts of missing records, filling in 0 for tickers that aren't in the missing records
missing_by_ticker = tickers_with_records.align(missing_by_ticker, fill_value=0)[1]
# Sort the missing records per ticker and convert to integers
missing_by_ticker = missing_by_ticker.sort_values(ascending=False).astype(int)
# Find the border values for ties
top_thresh = missing_by_ticker[9]
bot_thresh = missing_by_ticker[-10]
# Mask the top and bottom 10 using the border values
print('Top 10 Stocks Missing: \n',missing_by_ticker[missing_by_ticker >= top_thresh])
print('Bottom 10 Stocks Missing: \n',missing_by_ticker[missing_by_ticker <= bot_thresh])

'''
3.
Top 10 Stocks Missing: 
PDCO    45
SO      44
FLR     44
STJ     44
GE      43
RF      43
PPG     43
SWN     42
LVLT    42
HOT     42
QCOM    42
BBT     42
GAS     42
LB      42

Bottom 10 Stocks Missing: 
FB      0
ADT     0
GM      0
LYB     0
NAVI    0
NLSN    0
NWSA    0
TRIP    0
XYL     0
ZTS     0
'''

## 4.
# Group all records in the specified range by ticker and count frequency to get total days market was open
counts_by_ticker = in_range.groupby('Ticker')['Date'].count()
# Divide missing record count per ticker by total days open to find proportion
props_by_ticker = missing_by_ticker/(counts_by_ticker+missing_by_ticker)
props_by_ticker = props_by_ticker.sort_values(ascending=False) # Sort
# Find the border values for ties
top_thresh = props_by_ticker[9]
bot_thresh = props_by_ticker[-10]
# Find top and bottom 10 by masking with the border values, then using their indices to find
# the corresponding rows in the missing records frequency table
top_prop_counts = missing_by_ticker.loc[props_by_ticker[props_by_ticker >= top_thresh].index]
bot_prop_counts = missing_by_ticker.loc[props_by_ticker[props_by_ticker <= bot_thresh].index]
print('Top 10 Stocks Missing: \n',top_prop_counts)
print('Bottom 10 Stocks Missing: \n',bot_prop_counts)

'''
4.
Top 10 Stocks Missing: 
SO      44
PDCO    45
QCOM    42
STJ     44
FLR     44
RF      43
GE      43
PPG     43
GGP     41
LVLT    42
LB      42
SWN     42
HOT     42
GAS     42
BBT     42

Bottom 10 Stocks Missing: 
FB      0
GM      0
ADT     0
LYB     0
NAVI    0
NLSN    0
NWSA    0
TRIP    0
XYL     0
ZTS     0
'''

## 5.
# Group the missing records by date and count frequency per date, then sort
missing_by_date = missing_in_range.groupby('Date')['Ticker'].count().sort_values(ascending=False)
# Find the border values for ties
top_thresh = missing_by_date[9]
# Find the top 10 dates by masking with the border value
print(missing_by_date.index[missing_by_date >= top_thresh])

'''
5.
['2012-04-23', '2005-12-15', '2007-06-25', '2005-05-05',
 '2013-01-30', '2006-12-04', '2005-02-28', '2005-07-14',
 '2011-03-08', '2013-09-23']
'''

## 6.
price_types = ['Open', 'High', 'Low', 'Close','Volume'] # The 5 metrics to calculate for each date
newlines = [] # List to store new records to add
last_ticker = "" # Keeps track of the last ticker processed
for index, row in missing.iterrows(): # Loop through all missing records
    d2 = row['Date'] # Date to be interpolated
    if row['Ticker'] != last_ticker: # If this is our first time encountering this ticker
        data = df[df['Ticker'] == row['Ticker']] # Find all records for this ticker
    # Otherwise, data is still usable from the last iteration
    # Find records before and after missing date
    earlier = data[data['Date'] < d2]
    later = data[data['Date'] > d2]
    # The minimum later date is d3, the maximum earlier date is d1
    d1 = earlier.loc[earlier['Date'].idxmax()]
    d3 = later.loc[later['Date'].idxmin()]
    # Calculate time differences because they're the same for each metric to be calculated
    a = (d3['Date']-d2).days #
    b = (d2-d1['Date']).days
    c = (d3['Date']-d1['Date']).days
    # Set up the new record to add with the ticker and date that it's for
    dict = {'Ticker': row['Ticker'], 'Date': d2}
    for type in price_types: # Loop through the 5 things to interpolate
        dict[type] = (a*d1[type]+b*d3[type])/c # Interpolation formula, save in dictionary
    newlines.append(dict) # Add dictionary to list of new records to add
    last_ticker = row['Ticker'] # Update the last ticker encountered
df = pd.concat([df, pd.DataFrame(newlines)]) # Concat the original df and all the new interpolated rows
in_range = df[(df['Date'].dt.year>=2007) & (df['Date'].dt.year<=2013)] # Get records in date range

## 6a.
# Calculate the weighted prices for each of Open, High, Low, and Close
in_range['OpenW'] = in_range['Open']*in_range['Volume']
in_range['HighW'] = in_range['High']*in_range['Volume']
in_range['LowW'] = in_range['Low']*in_range['Volume']
in_range['CloseW'] = in_range['Close']*in_range['Volume']
# Group by date and sum the columns relevant to the formula
by_date = in_range.groupby('Date')['OpenW','HighW','LowW','CloseW','Volume'].sum()
pyindex = pd.DataFrame() # Initialize a df to store the python index
# For each of Open, High, Low, and Close, divide the numerator Series by denominator
pyindex['Open'] = by_date['OpenW']/by_date['Volume']
pyindex['High'] = by_date['HighW']/by_date['Volume']
pyindex['Low'] = by_date['LowW']/by_date['Volume']
pyindex['Close'] = by_date['CloseW']/by_date['Volume']
# Mask the python index by Oct 2010
print(pyindex[(pyindex.index.year == 2010) & (pyindex.index.month==10)])

'''
6a.
                 Open       High        Low      Close
Date                                                  
2010-10-01  39.169581  39.434530  38.461729  38.847595
2010-10-04  36.510926  36.970777  36.037449  36.470644
2010-10-05  36.821391  37.397876  36.469230  37.105123
2010-10-06  39.893535  40.348672  38.636233  39.300411
2010-10-07  38.711915  38.958309  38.004147  38.474292
2010-10-08  33.890921  34.354389  33.540042  34.078250
2010-10-11  36.729402  37.154667  36.305414  36.646461
2010-10-12  36.442557  37.035612  36.078277  36.841441
2010-10-13  36.963579  37.470745  36.601837  37.025214
2010-10-14  32.105693  32.370234  31.580260  31.928302
2010-10-15  31.384209  31.578964  30.617056  31.063536
2010-10-18  34.031321  34.490335  33.683067  34.226742
2010-10-19  33.253679  33.645777  32.673050  33.010323
2010-10-20  33.199450  33.880878  32.823187  33.527427
2010-10-21  40.940366  41.605321  40.194412  40.919451
2010-10-22  40.189095  40.802296  39.830970  40.410532
2010-10-25  35.343950  35.672289  34.925287  35.151389
2010-10-26  37.290510  38.299406  37.040847  37.953417
2010-10-27  39.112723  39.718565  38.627671  39.289454
2010-10-28  38.538390  38.825426  37.787602  38.267811
2010-10-29  39.347623  39.811310  38.935350  39.458878
'''

## 6b.
# Mask pyindex values between 2008-2012
in_range = pyindex[(pyindex.index.year>=2008) & (pyindex.index.year<=2012)]
# Group the pyindex values by their year-month, and calculate the mean values for each group
in_range.groupby(in_range.index.strftime('%Y-%m')).mean()

'''
6b.
             Open       High        Low      Close
2008-01  43.879383  44.892409  42.818134  43.879455
2008-02  44.312511  45.094670  43.430333  44.231277
2008-03  43.931635  44.795459  43.048824  43.933829
2008-04  44.443226  45.155724  43.795947  44.503364
2008-05  46.223506  46.903393  45.527736  46.240284
2008-06  43.551863  44.206226  42.731014  43.351498
2008-07  40.355927  41.309069  39.296554  40.294039
2008-08  41.288243  42.040213  40.513061  41.308876
2008-09  40.180907  41.356652  38.654772  39.998303
2008-10  31.236292  32.628599  29.519426  30.985339
2008-11  27.219452  28.183572  25.990354  27.058088
2008-12  26.335239  27.183410  25.544060  26.413611
2009-01  25.409133  26.069218  24.567002  25.308607
2009-02  21.604370  22.229320  20.907962  21.537163
2009-03  21.135608  21.857057  20.461184  21.201853
2009-04  23.071624  23.851243  22.531289  23.285297
2009-05  24.395802  25.015676  23.782373  24.428134
2009-06  26.374804  26.816666  25.879218  26.354770
2009-07  26.714240  27.212668  26.268579  26.811794
2009-08  28.961602  29.516990  28.487846  29.062931
2009-09  30.872073  31.393763  30.383100  30.899522
2009-10  32.438632  32.937909  31.901634  32.393257
2009-11  32.019869  32.471559  31.640013  32.113337
2009-12  32.763814  33.119627  32.400190  32.742729
2010-01  32.705986  33.121490  32.155696  32.608962
2010-02  33.132899  33.590305  32.712490  33.230161
2010-03  34.026824  34.439033  33.705850  34.099288
2010-04  36.493883  36.989883  35.956138  36.493005
2010-05  34.991162  35.602147  34.217451  34.919117
2010-06  34.969566  35.442337  34.399057  34.854441
2010-07  33.607538  34.101586  33.069073  33.652820
2010-08  35.069629  35.561742  34.632379  35.129022
2010-09  36.286588  36.778156  35.907844  36.384822
2010-10  36.660515  37.134589  36.135863  36.666509
2010-11  37.720691  38.234390  37.284057  37.807793
2010-12  39.662716  40.081944  39.251770  39.684723
2011-01  39.626213  40.106999  39.128459  39.667586
2011-02  42.111608  42.680693  41.621860  42.212864
2011-03  42.638494  43.186795  42.078523  42.651902
2011-04  42.867418  43.353457  42.320513  42.860279
2011-05  42.486394  42.965594  41.996559  42.498843
2011-06  39.442939  39.915710  38.998463  39.428882
2011-07  42.172371  42.731904  41.674772  42.201682
2011-08  34.352679  35.003856  33.486768  34.211051
2011-09  37.009378  37.650239  36.107664  36.725012
2011-10  34.838146  35.551106  34.138827  34.922552
2011-11  34.096725  34.566951  33.503721  34.019407
2011-12  33.602081  34.031428  33.111160  33.537572
2012-01  36.615057  37.266753  36.128494  36.824483
2012-02  37.729617  38.218533  37.302312  37.801535
2012-03  36.854072  37.273991  36.465473  36.917044
2012-04  38.646941  39.105297  38.166190  38.629491
2012-05  36.616235  37.099327  36.010804  36.460415
2012-06  35.507085  35.974332  35.038382  35.539954
2012-07  37.884296  38.400811  37.362617  37.910984
2012-08  37.160381  37.574388  36.803358  37.204773
2012-09  37.713443  38.147519  37.328751  37.760984
2012-10  38.252714  38.763395  37.739419  38.242168
2012-11  36.931831  37.411101  36.523875  36.988903
2012-12  37.350130  37.825887  36.975137  37.443758
'''