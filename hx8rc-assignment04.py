##
## File: hx8rc-assignment04.py
## Topic: Assignment 4
## Name: Eric Xie
## Section time: 3:30-4:45
## Grading Group: 6

#import Pandas and Numpy for later use
import pandas as pd
import numpy as np
#### Part 1

ff = pd.read_csv('fastfood1.csv',index_col=0) # Reads the csv into ff, with the storenums as indices
ff = ff.iloc[:,0] # Extracts the first column of ff into a series
ff = ff.sort_index() # Sort by ascending storenum

##  1(a)
print(ff.mean()) # Finds the mean order time

"""
1(a).
216.32710792916401
"""

##  1(b)
maxVal = ff.max() # Find largest order time in series
minVal = ff.min() # Find lowest order time in series
print(maxVal)
print(minVal)
print(ff.loc[ff.values == maxVal].size) # Select orders in ff that took longest time, then finds the size of that list
print(ff.loc[ff.values == minVal].size) # Select orders in ff that took shortest time, then finds the size of that list

"""
1(b).
max time: 600
min time: 30
number of orders taking max time: 23
number of orders taking min time: 123
"""

##  1(c)
print(ff[777].mean()) # Selects orders with index 777, which corresponds to orders from storenum 777, and finds mean

"""
1(c).
198.51908396946564
"""

##  1(d)
print(ff[321].size) # Selects orders from store 321 via their index, and returns the size of that list

"""
1(d).
97
"""

##  1(e)
print(ff.loc[700:750].mean()) # Select all orders by storenums 700-750, and finds the mean order time

"""
1(e).
215.89245446660885
"""

##  1(f)
data = ff.loc[500:600] # Save all the orders from stores 500-600 as a series called data
orders = data.loc[data.values > 200] # Save orders that took longer than 200 secs
n = data.size # Total number of orders from stores 500-600
p_hat = orders.size/n # Proportion of orders over 200 secs
q_hat = 1 - p_hat # Complement of p_hat
ci = [p_hat - 1.96*np.sqrt(p_hat*q_hat/n), p_hat + 1.96*np.sqrt(p_hat*q_hat/n)] # CI formula
print(ci)

"""
1(f).
[0.3683886862227696, 0.38620552814459169]
"""

##  1(g)
unique_stores = ff.index.unique() # Find the unique indices in the data, which correspond to unique storenums
print(unique_stores.size)

"""
1(g).
892
"""

##  1(h)
store_id_lowest = unique_stores[0] # keep track of the storenum with the lowest mean order time
store_id_highest = unique_stores[0] # do the same for the highest mean order time
lowest = ff.loc[store_id_lowest].mean() # keep track of the actual lowest mean time
highest = ff.loc[store_id_highest].mean() # do the same for the actual highest mean time
for i in unique_stores: # Iterate through all unique stores
    x_bar = ff.loc[i].mean() # calculate mean order time for that store
    #update the highest and lowest mean if necessary, and keep track of the corresponding storenums
    if x_bar > highest:
        highest = x_bar
        store_id_highest = i
        print(i)
    if x_bar < lowest:
        lowest = x_bar
        store_id_lowest = i
print(store_id_lowest)
print(store_id_highest)

"""
1(h).
Store with lowest mean order time: 243
Store with highest mean order time: 657
"""

##  1(i)
ctarray = [] # List to hold the number of orders for stores
for i in unique_stores: # Iterate through each unique store
    order = ff.loc[i].size # Select orders by the storenum and find its length
    ctarray.append(order) # Add the number of orders for this store to the list
print(np.median(ctarray)) # Numpy calculates the median number of orders

"""
1(i).
112.0
"""
#%%

#### Part 2

df = pd.read_csv('samplegrades.csv', index_col=0) # Read in grades data, using Student ID as the index
##  2(a)
print(df['CourseAve'].mean()) # Select just the Course Averages and find their mean
print(df['CourseAve'].std(ddof=1)) # Select just the Course Averages and find their sample std dev
print(df['Write'].mean()) # Select just the SAT Writing scores and find their mean
print(df['Write'].std(ddof=1)) # Select just the SAT Writing scores and find their sample std dev

"""
2(i).
Course Average Mean: 80.40115017667841
Course Average Std Dev: 10.666467372530862
SAT Writing Mean: 666.7234042553191
SAT Writing Std Dev: 94.45561725052345
"""

##  2(b)
females = df[df['Gender'] == 'F'] # Save all rows for which the Gender column is F as females
print(females['Final'].mean()) # Find the Final exam scores for females and average them

"""
2(b).
71.35179153094462
"""

##  2(c)
males = df[(df['Gender'] == 'M') & (df['Sect'] == 'TR930')] # Save all rows for which Gender is M and Section is TR930
print(males['Final'].mean()) # Find the average Final exam score for these males in section TR930

"""
2(c).
68.1534090909091
"""

##  2(d)
first_years = df[df['Year'] == 1]['HW'].mean() # For all rows where the Year is 1, find the average HW score
fourth_years = df[df['Year'] == 4]['HW'].mean() # For all rows where the Year is 4, find the average HW score
print(first_years)
print(fourth_years)

"""
2(d).
Mean HW Score for 1st Years: 189.24376811594198
Mean HW Score for 4th Years: 192.95172413793102
"""

##  2(e)
second_years = df[df['Year'] == 2] # Save all rows where the Year is 2 into second_years
in_section = second_years[second_years['Sect'] == 'MW200'].size # Out of the second_years, find those in Section MW200
print(in_section/second_years.size) # Finds proportion of 2nd yrs in the section

"""
2(e).
0.321428571429
"""

##  2(f)
df = df.sort_values('CourseAve') # Sort all rows by their Course Average values, such that lowest averages are first
# Get the last 20 rows, corresponding to the highest 20 course averages, and calculate the average of their scores
print(df.iloc[-20:].loc[:,'CourseAve'].mean())


"""
2(f).
95.21865
"""

##  2(g)
section = df[df['Sect'] == 'MW200'].sort_values('Final') # Sort all students in MW200 by their final exam scores
print(section[:10]['Final']) # Select the first 10 of those students, which have the lowest final scores

"""
2(g).
CRAMQ     0.0
ISCWI    27.5
HBTSX    35.0
BEYTQ    40.0
ZMERR    45.0
HYXDY    45.0
CBDIH    45.0
WQHKF    45.0
VLSJZ    50.0
EFTKY    50.0
"""

##  2(h)
cutoff_apde = df.quantile(0.8)['APDE'] # Find score that represents the 80th percentile of APDE
top_apde = df[df['APDE'] >= cutoff_apde] # Find students that are above 80th percentil
cutoff_avg = df.quantile(0.8)["CourseAve"] # Find score that represents 80th precentile of Course Average
# Count students who are both top 20th percentile in both, and divide by number of top 20th percentile APDE.
print(len(top_apde[top_apde['CourseAve'] >= cutoff_avg])*100/len(top_apde))

"""
2(h).
16.9811320754717
"""
