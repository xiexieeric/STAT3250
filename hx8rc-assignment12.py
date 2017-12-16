##
## File: hx8rc-assignment12.py
## Topic: Assignment 12
## Name: Eric Xie
## Section time: 3:30-4:45
## Grading Group: 6
##

import numpy as np
import matplotlib.pyplot as plt

def toDollar(num): # Define a function that converts rounds a number to 2 decimals
    return "%.2f" % np.round(num,2)

## 1.
# Set initial balance and interest rate
B = 50000
u = 0.076
for i in range(26): # Iterate from ages 40 to 65
    x = B * np.exp(i*u) # Calculate balance using Pe^rt
    print(40+i,'\t'+ toDollar(x)) # Print balance for each year

'''
1.
40 	50000.00
41 	53948.13
42 	58208.01
43 	62804.27
44 	67763.45
45 	73114.23
46 	78887.52
47 	85116.68
48 	91837.71
49 	99089.45
50 	106913.81
51 	115356.00
52 	124464.81
53 	134292.87
54 	144896.98
55 	156338.42
56 	168683.30
57 	182002.97
58 	196374.39
59 	211880.62
60 	228611.26
61 	246662.99
62 	266140.14
63 	287155.25
64 	309829.77
65 	334294.72
'''

## 2.
bal_list = [] # List to hold trials
for x in range(100000): # Experiment 100000 times
    B = 50000 # Set initial balance
    for i in range(26): # Iterate from age 40 to 65
        if i != 0: # Don't compound interest on the first year
            B = B*np.exp(np.random.normal(0.076, 0.167)) # Lognormal formula
    bal_list.append(B) # Add balance at age 65 to list

## 2a.
x_bar = np.mean(bal_list) # Calculate mean balance at 65
print(toDollar(x_bar)) # Convert to dollar format

'''
2a.
472119.48
'''

## 2b.
print(toDollar(np.median(bal_list))) # Find median balance at age 65

'''
2b.
332788.24
'''

## 2c.
bal_list.sort() # Sort the list of balances
ci = [bal_list[2500], bal_list[97499]] # Use 2.5 and 97.5 percentiles as the CI bounds
print(ci)

'''
2c.
[64588.943462381125, 1706040.7590449501]
'''

## 2d.
succ = len([x for x in bal_list if x > 300000]) # Add all values over 300000 to new list and count
print(succ/100000) # Proportion formula

'''
2d.
0.54923
'''

## 2e.
plt.hist(bal_list, bins=100, range=[0,2000000]) # Plot histogram

## 3.
# Set up initial balance and interest rate
B = 50000
u = 0.076
for i in range(26): # Iterate through age 40 to 65
    if i != 0: # Only accumulate interest and deposit after 40
        B = B*np.exp(u) + 3000 # Add interest and deposit 3000
    print(40+i,'\t'+toDollar(B)) # Print balance at this age

'''
3.
40 	50000.00
41 	56948.13
42 	64444.90
43 	72533.63
44 	81261.08
45 	90677.66
46 	100837.80
47 	111800.22
48 	123628.25
49 	136390.25
50 	150159.98
51 	165017.00
52 	181047.16
53 	198343.11
54 	217004.80
55 	237140.05
56 	258865.24
57 	282305.91
58 	307597.51
59 	334886.20
60 	364329.68
61 	396098.09
62 	430375.01
63 	467358.53
64 	507262.36
65 	550317.10
'''

## 4.
bal_list = [] # New list to hold 100000 trials
for x in range(100000): # Simulate 100000 trials
    B = 50000 # Initial balance
    for i in range(26): # Iterate from age 40 to 65
        if i != 0: # Only accumulate interest and deposit after age 40
            # Accumulate interest using formula and add 3000 deposit
            B = B*np.exp(np.random.normal(0.076, 0.167)) + 3000
    bal_list.append(B) # Add balance at age 65 to list

## 4a.
x_bar = np.mean(bal_list) # Calculate mean balance at 65
print(toDollar(x_bar)) # Convert to dollar format

'''
4a.
746403.67
'''

## 4b.
print(toDollar(np.median(bal_list))) # Find median balance at 65

'''
4b.
564061.10
'''

## 4c.
bal_list.sort() # Sort the list of balances
ci = [bal_list[2500], bal_list[97499]] # Use 2.5 and 97.5 percentiles as the CI bounds
print(ci)

'''
4c.
[149379.45184674452, 2418123.1073136209]
'''

## 4d.
succ = len([x for x in bal_list if x > 300000]) # Add all values over 300000 to new list and count
print(succ/100000) # Find proportion

'''
4d.
0.81608
'''

## 4e.
plt.hist(bal_list, bins=100, range=[0, 3000000]) # Plot histogram

## 5.
# Set initial balance, interest rate, and deposit amount
B = 50000
u = 0.076
d = 3000
for i in range(26): # Iterate through ages 40 to 65
    if i != 0: # Don't accumulate interest or deposit at age 40
        B = B*np.exp(u) + d # Interest formula and add deposit
        d = d*np.exp(0.03) # Increase next year's deposit with inflation
    print(40+i,'\t'+toDollar(B)) # Print the balance at the beginning of this year

'''
5.
40 	50000.00
41 	56948.13
42 	64536.26
43 	72817.72
44 	81850.12
45 	91695.71
46 	102421.74
47 	114100.87
48 	126811.61
49 	140638.73
50 	155673.82
51 	172015.80
52 	189771.51
53 	209056.35
54 	229994.92
55 	252721.79
56 	277382.29
57 	304133.33
58 	333144.36
59 	364598.32
60 	398692.74
61 	435640.90
62 	475673.06
63 	519037.80
64 	566003.51
65 	616859.91
'''

## 6.
bal_list = [] # New list to hold 100000 trials
for x in range(100000): # Run 100000 experiments
    # Set initial balance and deposit
    B = 50000
    d = 3000
    for i in range(26): # Iterate through ages 40 to 65
        if i != 0: # Don't accumulate interest or deposit at age 40
            # Accumulate interest according to formula and make deposit
            B = B*np.exp(np.random.normal(0.076, 0.167)) + d
            d = d * np.exp(0.03) # Increase deposit for next year according to inflation
    bal_list.append(B) # Add balance at age 65 to list

## 6a.
x_bar = np.mean(bal_list) # Calculate mean balance at age 65
print(toDollar(x_bar)) # Convert to dollar format

'''
6a.
820613.51
'''

## 6b.
print(toDollar(np.median(bal_list))) # Find median balance at age 65

'''
6b.
635010.44
'''

## 6c.
bal_list.sort() # Sort the list of balances
ci = [bal_list[2500], bal_list[97499]] # Use 2.5 and 97.5 percentiles as the CI bounds
print(ci)

'''
6c.
[187302.03267350385, 2562623.4579916834]
'''

## 6d.
succ = len([x for x in bal_list if x > 300000]) # Add all values over 300000 to new list and count
print(succ/100000) # Proportion formula

'''
6d.
0.87592
'''

## 6e.
plt.hist(bal_list, bins=100, range=[0, 3000000]) # Plot histogram

## 7.
# Set initial balance, interest rate, and deposit amount
B = 50000
u = 0.076
d = 3000
for i in range(61): # Iterate from age 40 to 100
    if i != 0: # Only add interest, deposit, or withdraw after age 40
        if i > 25: # If age 66 or above
            u = 0.035 # Set new interest rate
            B = B * np.exp(u) - 25000 # Collect interest and withdraw
        else: # If between 41 and 65
            B = B*np.exp(u) + d # Collect interest and make deposit
            d = d*np.exp(0.03) # Increase deposit for inflation
    print(40+i,'\t'+toDollar(B)) # Print balance for the year

'''
7.
40 	50000.00
41 	56948.13
42 	64536.26
43 	72817.72
44 	81850.12
45 	91695.71
46 	102421.74
47 	114100.87
48 	126811.61
49 	140638.73
50 	155673.82
51 	172015.80
52 	189771.51
53 	209056.35
54 	229994.92
55 	252721.79
56 	277382.29
57 	304133.33
58 	333144.36
59 	364598.32
60 	398692.74
61 	435640.90
62 	475673.06
63 	519037.80
64 	566003.51
65 	616859.91
66 	613832.28
67 	610696.80
68 	607449.64
69 	604086.82
70 	600604.22
71 	596997.57
72 	593262.45
73 	589394.28
74 	585388.34
75 	581239.70
76 	576943.29
77 	572493.84
78 	567885.90
79 	563113.83
80 	558171.78
81 	553053.70
82 	547753.31
83 	542264.13
84 	536579.42
85 	530692.22
86 	524595.32
87 	518281.25
88 	511742.28
89 	504970.39
90 	497957.29
91 	490694.38
92 	483172.78
93 	475383.25
94 	467316.26
95 	458961.93
96 	450310.02
97 	441349.93
98 	432070.69
99 	422460.92
100 412508.86
'''

## 8.
bal_list = [] # New list to hold 100000 trials
for i in range(100000): # Simulate 1000000 times
    # Set initial balance and deposit
    B = 50000
    d = 3000
    for i in range(61): # Iterate from age 40 to 100
        if i != 0: # Only collect interest, deposit, or withdraw after 40
            if i > 25: # If 66 or older
                u = 0.035 # Set new mean interest rate
                # Collect interest according to formula and withdraw
                B = B * np.exp(np.random.normal(0.035, 0.051)) - 25000
            else: # If between age 41 and 65
                # Collect interest and make deposit
                B = B*np.exp(np.random.normal(0.076, 0.167)) + d
                d = d*np.exp(0.03) # Increase deposit for inflation
    bal_list.append(B) # Add balance at age 100 to list

## 8a.
x_bar = np.mean(bal_list) # Calculate mean balance at age 100
print(toDollar(x_bar)) # Convert to dollar format

'''
8a.
1190464.98
'''

## 8b.
print(toDollar(np.median(bal_list))) # Find median balance at age 100

'''
8b.
447066.31
'''

## 8c.
bal_list.sort() # Sort the list of balances
ci = [bal_list[2500], bal_list[97499]] # Use 2.5 and 97.5 percentiles as the CI bounds
print(ci)

'''
8c.
[-1102422.0834796175, 7912964.9883558862]
'''

## 8d.
succ = len([x for x in bal_list if x > 0]) # Add all values over 0 to new list and count
print(succ/100000) # Proportion formula

'''
4d.
0.63477
'''

## 8e.
plt.hist(bal_list, bins=100, range=[-1500000, 7000000]) # Plot histogram