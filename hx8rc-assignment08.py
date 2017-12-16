##
## File: hx8rc-assignment08.py
## Topic: Assignment 8
## Name: Eric Xie
## Section time: 3:30-4:45
## Grading Group: 6
##

## The focus of this assignment is dates.  Not the fruit, but the time
## and date that data is put into a file.

## 1. The questions below require the data frame 'reviews.txt' that
##    is described in the README_assign08.txt file.  You can use the
##    code below to read in the data as a dataframe.

import pandas as pd # load pandas as pd
reviews = pd.read_csv('reviews.txt', 
                        sep='\t',
                        header=None,
                        names=['Reviewer','Movie','Rating','Date'])

##  (a) Find the date and time of the oldest review, and the 
##      most recent review.  Give the result in the form
##      matching "2016-10-18 17:50:43".  (Times UTC)
time_col = reviews['Date'] # Pull out the date column
oldest_rev = pd.to_datetime(time_col.min(), unit='s') # Get the smallest value and covert to a datetime object
newest_rev = pd.to_datetime(time_col.max(), unit='s') # Get the largest value and covert to a datetime object
format = "%Y-%m-%d %H:%M:%S" # Format specified by the question
print(oldest_rev.strftime(format))
print(newest_rev.strftime(format))

'''
1(a).
oldest: 1997-09-20 03:05:10
newest: 1998-04-22 23:10:38
'''

##  (b) Determine the median date and time for the reviews.
##      Give the result in the form "Tuesday October 18 2016 17:50:43"
##      (Times UTC)
median_rev = pd.to_datetime(time_col.median(), unit='s') # Get the median secs value and convert to datetime object
format = "%A %B %d %Y %H:%M:%S" # Format specified by question
print(median_rev.strftime(format))

'''
1(b).
Monday December 22 1997 21:42:24
'''

##  (c) Find the average rating for each month of the year.
reviews['Date'] = pd.to_datetime(reviews['Date'], unit='s') # Switch the 'Date' column from seconds to datetime objects
by_month = reviews.groupby(reviews['Date'].dt.strftime('%B'))['Rating'] # Group review ratings by their month
print(by_month.mean()) # Calculate mean rating of each month

'''
1(c).
January      3.397730
February     3.455009
March        3.548831
April        3.574848
September    3.540125
October      3.591421
November     3.559842
December     3.580388
'''

##  (d) Determine which day of the week produced the most reviews.
by_day = reviews['Date'].dt.strftime('%A').value_counts() # Group just the date col by day-of-week and count frequencies
# Look through indices (days of week) for the one that gives the max frequency
print(by_day.index[by_day == by_day.max()].values[0])

'''
1(d).
Wednesday
'''

##  (e) Determine the date and time of the first review for the 5 reviewers
##      who had the most reviews.
# Group reviews by their reviewer id, and count how many belong to each id by arbitrarily selecting a column to count
# Sort from most reviews to least
by_user = reviews.groupby(reviews['Reviewer'])['Date'].count().sort_values(ascending=False)
# Find the reviewer id's with the 5 highest number of reviews, and get all reviews by them
dates_top5 = reviews[reviews['Reviewer'].isin(by_user.index[:5])]
earliest_dates = dates_top5.groupby(dates_top5['Reviewer'])['Date'].min()
# Group those reviews by reviewer and find the earliest date for each reviewer
print(earliest_dates)

'''
1(e).
Reviewer
13    1997-12-07 17:11:23
276   1997-09-20 20:12:17
405   1998-01-23 08:37:15
450   1997-12-15 19:53:37
655   1998-02-14 02:52:00
'''

## 2. The questions below require the file 'pizza_requests.txt' seen 
##    previously.  All questions refer to the date and time given in 
##    the variable "unix_timestamp_of_request_utc" for each request.

lines = pd.Series(open('pizza_requests.txt').read().splitlines()) # Read all the lines of file into a Series
# Extract all the lines containing utc timestamps into a Series of floats
times_flt = lines[lines.str.contains('unix_timestamp_of_request_utc')].str.split(', ').str[1].astype(float)
times = pd.to_datetime(times_flt, unit='s') # Create a Series of datetimes from the Series of floats

##  (a) Find the date and time of the oldest request, and the 
##      most recent request.  Give the result in the form
##      matching "2016-10-18 17:50:43".  (Times UTC)
print(times.min().strftime('%Y-%m-%d %H:%M:%S')) # Print the oldest time with specified format
print(times.max().strftime('%Y-%m-%d %H:%M:%S')) # Print the newest time with specified format

'''
2(a).
2011-02-14 22:28:57
2013-10-12 01:30:36
'''

##  (b) Determine the median date and time for the requests.
##      Give the result in the form "Tuesday October 18 2016 17:50:43"
##      (Times UTC)
# Use the times in float format to find the median, convert to datetime, and print with specified format
print(pd.to_datetime(times_flt.median(), unit='s').strftime('%A %B %d %Y %H:%M:%S'))

'''
2(b).
Friday July 20 2012 17:54:08
'''

##  (c) Determine the number of requests for each hour of the day.  Report
##      the 5 one-hour periods with the most requests, and the number of
##      requests for each.
# Count the number of lines for each hour, and sort them from most requests to least
by_hour = times.groupby(times.dt.strftime('%H')).count().sort_values(ascending=False)
print(by_hour[:5]) # Print the 5 hours with most requests via slicing

'''
2(c).
00    508
22    497
23    491
21    464
01    441
'''

##  (d) Find the hour of the day that resulted in the highest proportion
##      of successful pizza requests.
# Generate a Series containing the success status of every request, either true/false
successful = lines[lines.str.contains('requester_received_pizza')].str.split(', ').str[1].str.strip()
# Build a DF with 1 column containing timestamps and 1 column containing the successfulness of that request
times_success = pd.DataFrame({'time': times.values, 'success': successful.values})
# Group by successfulness and then by hour, counting the frequency of each hour for true/false
by_hour = times_success.groupby([times_success['success'], times_success['time'].dt.strftime('%H')]).count()
# Calculates the proportion of success for each hour by element-wise Series arithmetic
prop_by_hour = by_hour['time']['true']/(by_hour['time']['true']+by_hour['time']['false'])
print(prop_by_hour.idxmax()) # Find the index (hour) with the highest proportion 

'''
2(d).
13
'''

##  (e) Repeat (d), this time finding the hour with the lowest success rate.
print(prop_by_hour.idxmin()) # Find the index (hour) with the highest proportion

'''
2(e).
08
'''
