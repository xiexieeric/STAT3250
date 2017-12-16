##
## File: hx8rc-assignment07.py
## Topic: Assignment 7
## Name: Eric Xie
## Section time: 3:30-4:45
## Grading Group: 6
##

import numpy as np
import pandas as pd

lines = pd.Series(open('pizza_requests.txt').read().splitlines()) # Read each line into a pandas series
n = len(lines[lines.str.contains('"giver_username_if_known"')]) # Use one attribute to count total requests

## 1.
success = lines[lines.str.contains('"requester_received_pizza", true')] # All requests that were successful
print(len(success) / n) # Proportion formula

'''
1.
0.24634103332745547
'''

## 2.
# Save all the account ages as a series of floats
ages = lines[lines.str.contains('"requester_account_age_in_days_at_request"')].str.split(', ').str[1].astype(float)
med = ages.median() # Find median of account ages
print(med)

'''
2.
155.6475925925926
'''

## 3.
greater = ages[ages > med] # Isolate account ages older than median
lesser = ages[ages <= med] # Isolate account ages younger than median
# Go down 13 lines from the age to find the success value
greater_succ = lines[greater.index + 13]
lesser_succ = lines[lesser.index + 13]
n1 = len(greater) # Number of acct ages older than median
n2 = len(lesser) # Number of acct ages younger than median
p1 = len(greater_succ[greater_succ.str.contains('true')]) / n1 # Proportion of older accounts that were successful
q1 = 1 - p1 # Complement
p2 = len(lesser_succ[lesser_succ.str.contains('true')]) / n2 # Proportion of younger accounts that were successful
q2 = 1 - p2 # Complement
ci = [p1-p2-1.96*np.sqrt(p1*q1/n1+p2*q2/n2), p1-p2+1.96*np.sqrt(p1*q1/n1+p2*q2/n2)] # CI formula
print(ci)

'''
3.
[0.021770947082183623, 0.066570682209140045]
'''

## 4.
req_texts = lines[lines.str.contains('"request_text"')].str.lower() # Isolate request texts in lowercase form
# Find all request texts that contained either of the keywords
contains_key = req_texts[(req_texts.str.contains('student')) | (req_texts.str.contains('children'))]
print(len(contains_key)*100/n) # Percentage formula

'''
4.
9.222359372244753%
'''

## 5.
req_titles = lines[lines.str.contains('"request_title"')].str.lower() # Isolate request titles in lowercase form
contains_key = req_titles[req_titles.str.contains('canada')] # Find all titles that contain Canada
print(len(contains_key))

'''
5.
103
'''

## 6.
# For each success line, go up 23 lines to find the username line, save as series
uname_by_succ = lines[success.index - 23]
n = len(success) # Number of successful requests
p = len(uname_by_succ[uname_by_succ.str.contains('N/A')]) / n # Proportion of successful that were anonymous
q = 1 - p # Complement
ci = [p - 1.96*np.sqrt(p*q/n), p + 1.96*np.sqrt(p*q/n)] # CI formula
print(ci)

'''
6.
[0.68996720497778263, 0.73737710425629033]
'''

## 7.
# Save the indices of the line immediately preceding lists of subreddits
subreddits_start = lines[lines.str.contains('"requester_subreddits_at_request"')].index
# Save the indices of the line immediately following lists of subreddits
subreddits_end = lines[lines.str.contains('requester_upvotes_minus_downvotes_at_request')].index
# Subtract those two series element-wise to find the length of each list of subreddits
# Subtract 2 to account for brackets and the ending line
num_subs = subreddits_end-subreddits_start-2
print(num_subs.max()) # Find max number of subreddits

'''
7.
235
'''

## 8.
# Identify lines containing subreddits by the fact that they
#  don't contain commas, don't contain '%', but do contain quotes
all_subs = lines[lines.str.startswith('  "')]
all_subs = all_subs.str.strip().str.strip('"') # Remove quotes and trailing spaces
freq = all_subs.value_counts() # pandas.Series function that creates frequency table, descending order
for i in range(10): # For the top ten most common subreddits
    print(freq.index[i]+", "+str(freq[i])) # Print name and freq

with open('hx8rc-assignment07-subreddits.txt', "w") as outfile: # Prepare file for writing
    for i in range(len(freq)): # Iterate through all subreddits in freq table
        outfile.write(freq.index[i] + ", " + str(freq[i])+"\n") # Write name and freq to file
outfile.close() # Close file

freq.to_csv('test.txt')
'''
8.
AskReddit, 3241
pics, 2734
funny, 2704
IAmA, 2138
WTF, 2133
gaming, 2079
Random_Acts_Of_Pizza, 1978
videos, 1620
todayilearned, 1556
AdviceAnimals, 1452
'''