##
## File: hx8rc-assignment05.py
## Topic: Assignment 5
## Name: Eric Xie
## Section time: 3:30-4:45
## Grading Group: 6

import pandas as pd
import numpy as np
#### Part 1

df = pd.read_csv('fastfood2.csv')

##  1(a)
num_lunch = len(df[df['meal']=="Lunch"]) #Isolate lunch orders
print(num_lunch/len(df)) #Find proportion compared to all orders

'''
1(a).
0.5165224154435226
'''
##  1(b)
#Calculate mean on seconds when grouped by day of week
days = df['secs'].groupby(df['dayofweek']).mean()
#Print mean in order for each day
print("Mon:", days["Mon"])
print("Tues:", days["Tues"])
print("Wed:", days["Wed"])
print("Thur:", days["Thur"])
print("Fri:", days["Fri"])

'''
1(b).
Mon: 216.774747074
Tues: 215.742299693
Wed: 216.282449267
Thur: 216.605129495
Fri: 216.234940657
'''

##  1(c)
mealtypes = ['Breakfast', 'Lunch', 'Dinner'] #Iterable list of meals
for meal in mealtypes: #Perform calculations for each meal
    data = df[df['meal'] == meal]
    n = len(data)
    p_hat = len(data[data['drinkonly']=="Yes"])/n
    q_hat = 1 - p_hat
    # CI formula
    ci = [p_hat - 1.96*np.sqrt(p_hat*q_hat/n), p_hat + 1.96*np.sqrt(p_hat*q_hat/n)]
    print(ci)

'''
1(c).
Breakfast: [0.22117406656754271, 0.23613394334162327]
Lunch:     [0.12675719458238568, 0.13254281893086697]
Dinner:    [0.12730476118757109, 0.1342341232723899]
The confidence intervals for lunch and dinner overlap significantly, but neither
overlaps with breakfast, which has a significantly higher proportion of drink only 
orders. 
'''

##  1(d)
# Calculate mean on cost when grouped by meal
mean_costs = df['cost'].groupby(df['meal']).mean()
# Print mean cost for each meal in order
print(mean_costs["Breakfast"])
print(mean_costs["Lunch"])
print(mean_costs["Dinner"])

'''
1(d).
Breakfast: 292.079190751
Lunch:     372.363622324
Dinner:    502.017676004
'''

##  1(e)
daysofweek = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri'] # Iterable list of days
mealtypes = ['Breakfast', 'Lunch', 'Dinner'] # Iterable list of meals
for day in daysofweek: # For each day of week
    data = df[df['dayofweek'] == day] # Isolate orders on this day
    n = len(data) # Number of orders this day
    for meal in mealtypes: # For each meal
        p = len(data[data['meal'] == meal])/n # Proportion formula
        print(p)

'''
1(e).
Monday
Breakfast: 0.12016464987105734
Lunch:     0.5155723070819281
Dinner:    0.36426304304701446
Tuesday
Breakfast: 0.11983757551748044
Lunch:     0.516440526889175
Dinner:    0.36372189759334456
Wednesday
Breakfast: 0.11990154711673699
Lunch:     0.5144665461121157
Dinner:    0.36563190677114726
Thursday
Breakfast: 0.12245411113904954
Lunch:     0.5160673874779985
Dinner:    0.36147850138295196
Friday
Breakfast: 0.12141828474946616
Lunch:     0.5200377414709242
Dinner:    0.35854397377960967
'''

##  1(f)
# Store the mean order time for each store
stores = df.groupby(df['storenum'])['secs'].mean()
# Calculate the thresholds for high and low performance using mean
x_bar = stores.mean()
std = stores.std()
lower = x_bar - 2*std
higher = x_bar + 2*std
# Find high/low performing stores by comparing with threshold time
# reset_index() allows access to storenum column
high_performing_mean = stores[stores <= lower].reset_index()
low_performing_mean = stores[stores >= higher].reset_index()
# Print only storenums of the groups
print(high_performing_mean['storenum'].values)
print(low_performing_mean['storenum'].values)

'''
1(f).
High Performing Stores: [ 27  43  53 122 201 243 312 500 511 514 550 570 651 699 722 852 859]
Low Performing Stores: [ 30  47  59 128 149 154 155 231 233 281 318 387 392 402 422 452 474 528
614 621 657 718 723 725 726 887]
'''

##  1(g)
# Store the median order time for each store
stores = df.groupby(df['storenum'])['secs'].median()
# Calculate the thresholds for high and low performance using mean median
x_bar = stores.mean()
std = stores.std()
lower = x_bar - 2*std
higher = x_bar + 2*std
# Find high/low performing stores by comparing with threshold time
# reset_index() allows access to storenum column
high_performing_med = stores[stores <= lower].reset_index()
low_performing_med = stores[stores >= higher].reset_index()
# Cast all performance groups into sets in order to intersect them
both_high = set(high_performing_mean['storenum']).intersection(set(high_performing_med['storenum']))
both_low = set(low_performing_mean['storenum']).intersection(set(low_performing_med['storenum']))
# Print only storenums
print(high_performing_med['storenum'].values)
print(low_performing_med['storenum'].values)
# Sort intersection before printing
print(sorted(both_high))
print(sorted(both_low))

'''
1(g).
High Performing Stores: [ 27 243 312 722]
Low Performing Stores: [ 14  59 130 149 161 173 200 233 240 242 267 290 304 
318 320 357 365 402 438 448 452 478 517 528 531 546 568 611 640 657 702 718 
723 725 726 755 796 875 887]
Both High Performing: [27, 243, 312, 722]
Both Low Performing: [59, 149, 233, 318, 402, 452, 528, 657, 718, 723, 725, 726, 887]
'''

#### Part 2

df = pd.read_csv('fastfood3.csv')

##  2(a)
max = df['satisfaction'].max() # Max of satisfaction col
min = df['satisfaction'].min() # Min of satisfaction col
n = len(df) # Total orders
print(len(df[df['satisfaction'] == max])*100/n) # Percentage formula
print(len(df[df['satisfaction'] == min])*100/n)

'''
2(a).
Highest: 0.1296266751754946%
Lowest: 0.004985641352903638%
'''

##  2(b)
# Calculate mean satisfaction value when data grouped by day of week
mean_sat = df['satisfaction'].groupby(df['dayofweek']).mean()
print(mean_sat)

'''
2(b).
Mon     6.132017
Tues    6.142121
Wed     6.141752
Thur    6.118582
Fri     6.116154
'''

##  2(c)
meals = ['Breakfast', 'Lunch', 'Dinner'] # Iterable list of meals
for meal in meals: # For each meal
    data = df[df['meal'] == meal] # Isolate orders of that meal only
    n = len(data)
    p_hat = len(data[data['satisfaction'] >= 7])/n
    q_hat = 1-p_hat
    # CI formula
    ci = [p_hat - 1.96*np.sqrt(p_hat*q_hat/n), p_hat + 1.96*np.sqrt(p_hat*q_hat/n)]
    print(ci)

'''
2(c).
Breakfast: [0.54399335890671141, 0.56170441153094353]
Lunch:     [0.35876723189754983, 0.3670488720386676]
Dinner:    [0.43303525024777823, 0.44323272127268798]
'''

##  2(d)
fast = df[df['secs'] <= 180] # Isolate 'fast' orders
n = len(fast)
p_hat = len(fast[fast['satisfaction'] >= 7]) / n # Calculate proportion
q_hat = 1 - p_hat
# CI Formula
ci = [p_hat - 1.96 * np.sqrt(p_hat * q_hat / n), p_hat + 1.96 * np.sqrt(p_hat * q_hat / n)]
print(ci)

slow = df[df['secs'] >= 360] # Isolate 'slow' orders
n = len(slow)
p_hat = len(slow[slow['satisfaction'] >= 7]) / n # Calculate proportion
q_hat = 1 - p_hat
# CI Formula
ci = [p_hat - 1.96 * np.sqrt(p_hat * q_hat / n), p_hat + 1.96 * np.sqrt(p_hat * q_hat / n)]
print(ci)

'''
2(d).
Faster than 180: [0.53217460518638282, 0.54038739287204096]
Slower than 360: [0.1024361195473813, 0.11139622888772485]
'''

##  2(e)
for i in range(len(df)): # Iterate through every order
    # Extract values from the order to calculate predicted satisfaction
    secs = df.loc[i,'secs']
    cost = df.loc[i, 'cost']
    m = 1 if df.loc[i,'meal'] == 'Breakfast' else 0
    # Calculate using formula and apply to new column
    df.loc[i,'predsatis'] = 4 + 0.002*cost - 0.005*secs + m
print(df['predsatis'].mean()) # Find mean value of predsatis column

'''
2(e).
3.858512513959867
'''

##  2(f)
# Placeholder max and min difference using the first order
max_diff = np.abs(df.loc[0, 'predsatis'] - df.loc[0, 'satisfaction'])
min_diff = np.abs(df.loc[0, 'predsatis'] - df.loc[0, 'satisfaction'])
# Accumulate total difference for mean calculation
total_diff = 0
for i in range(len(df)): # Iterate through every order
    diff = np.abs(df.loc[i, 'predsatis'] - df.loc[i, 'satisfaction']) # Find diff
    total_diff += diff # Add diff to total
    # Replace max and min if new max/min is found
    max_diff = diff if diff > max_diff else max_diff
    min_diff = diff if diff < min_diff else min_diff
print(max_diff)
print(min_diff)
print(total_diff/len(df))

'''
2(f).
Max Difference: 4.896
Min Difference: 0.0
Mean Difference: 2.27289870174
'''