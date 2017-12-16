##
## File: hx8rc-assignment06.py
## Topic: Assignment 6
## Name: Eric Xie
## Section time: 3:30-4:45
## Grading Group: 6
##

lines = open('timing_log.txt').read().splitlines()

#
# 1.
count = 0 # Initialize a count
for line in lines: # Go through each entry
    if line.count('hardcopy') > 0: # If the line is a PDF request
        count += 1 # Increment count
print(count)

'''
1.
138
'''

# 2.
n = len(lines) # Find the total number of entries
count = 0 # Initialize a count
for line in lines: # Go through each entry
    if line.count('STAT2120') > 0: # If the line contains 'STAT 2120'
        count += 1 # Increment count
print(count*100/n) # Find percentage

'''
2.
52.49243925331108%
'''

# 3.
count = 0 # Initialize a count
for line in lines: # Go through each entry
    if line.count('admin') == 0: # Skips admin entries
        elements = line.split() # Split by space
        element = elements[8].split('/') # Go to the webwork element and split by '/'
        if len(element) == 3 and len(element[2]) > 1: # Matches the specified template as-is
            count += 1 # Increment count
        if len(element) == 4 and element[3] == ']': # Matches the template if there is an extra trailing '/'
            count += 1 # Increment count
print(count*100/n) # Calculate percentage

'''
3.
3.790801960579831%
'''

# 4.
count = 0 # Initialize a count
for line in lines: # Go through each entry
    elements = line.split() # Split by space
    element = elements[8].split('/') # Find webwork element and split by /
    if len(element) > 3 and element[3] == 'instructor': # Only increment if instructor is in 3rd position
        count += 1
print(count)

'''
4.
295
'''

# 5.
dict = {} # Maps hours to their frequency
for line in lines: # Go through each entry
    elements = line.split() # Split by space
    element = elements[3].split(':') # Find time element
    hour = element[0] # Save the hour
    if hour not in dict: # Add the hour to the dict if not present
        dict[hour] = 1 # Set frequency to 1
    else: # If dict already has the hour
        dict[hour] = dict[hour] + 1 # Increment frequency
most = max(dict.values()) # Find the highest freq
least = min(dict.values()) # Find lowest freq
most_key = "" # Placeholder for highest freq hour
least_key = "" # Placeholder for lowest freq hour
for key in dict: # Go through all hours
    if dict[key] == most: # Sets highest freq hour if it matches the highest freq
        most_key = key
    if dict[key] == least: # Sets lowest freq hour if it matches the lowest freq
        least_key = key
print(most_key)
print(least_key)

'''
5.
Most: 22
Least: 06
'''

# 6.
count = 0 # Initialize a count
classes = set() # Create a set for the unique classes
for line in lines: # Go through each entry
    element = line.split()[8] # Find the webwork element
    if element.count('admin') == 0: # Skip admin entries
        element = element.split('/') # Split by '/'
        if len(element) > 2: # Only splits with 3+ pieces have class names
            if len(element) == 3: # If exactly 3 pieces
                classes.add(element[2][:-1]) # Trim the trailing ']' and add to set
            else: # Else, add the classname directly to set
                classes.add(element[2])
print(len(classes)) # Find number of unique classnames

'''
6.
40
'''

# 7.
dict = {} # Maps classes both to their number of entries and total runtime
for line in lines: # Go through each entry
    if line.count('admin') == 0: # Skip admin entries
        element = line.split()[8] # Find webwork element
        element = element.split('/') # Split by '/'
        if len(element) > 2: # Only splits with 3+ pieces contain classnames
            s = "" # To hold the classname
            if len(element) == 3: # If exactly 3 pieces
                s = element[2][:-1] # Classname needs to trim trailing ']'
            else: # Else, classname is just the 2nd element
                s = element[2]
        element = line.split()[11] # Find the runtime element
        if s != '': # Only consider the line if the classname isn't empty
            if s not in dict: # If the class is not in the dict
                dict[s] = [1, float(element)] # The class starts with freq=1 and runtime=this line's runtime
            else: # If the class is already in the dict
                dict[s][0] += 1 # Increment the class frequency
                dict[s][1] += float(element) # Add this entry's runtime to the total runtime

asList = list(dict.items()) # Cast the dictionary as a list of tuples containing the classname and usage data
byEntries = sorted(asList, key = lambda x: x[1][0], reverse=True) # Sort the list by the frequency data
byTime = sorted(asList, key = lambda x: x[1][1], reverse=True) # Sort the list by the runtime data

#    (a) Based on the number of entries in the log file
# Find the top 3 highest frequency classes
print(byEntries[0][0])
print(byEntries[1][0])
print(byEntries[2][0])

'''
7(a).
1. Spring11-STAT2120
2. Spring12-STAT2120
3. Spring11-APMA2130-Fulgham
'''

#    (b) Based on the total "runTime" required.
# Find the top 3 highest runtime classes
print(byTime[0][0])
print(byTime[1][0])
print(byTime[2][0])

'''
7(b).
1. Spring11-STAT2120
2. Spring11-APMA2130-Fulgham
3. Spring12-APMA2130
'''

# 8.
# Sort the list by dividing total runtime by frequency
byAvgTime = sorted(asList, key = lambda x: x[1][1]/x[1][0], reverse=True)
# Find the top 3 highest average runtime classes
# First prints the name, then the calculated avg runtime
print(byAvgTime[0][0], byAvgTime[0][1][1]/byAvgTime[0][1][0])
print(byAvgTime[1][0], byAvgTime[1][1][1]/byAvgTime[1][1][0])
print(byAvgTime[2][0], byAvgTime[2][1][1]/byAvgTime[2][1][0])

'''
8.
1. APMA2120-Devel 0.5334690265486726
2. apma2130-devel 0.3876734693877551
3. Spring12-APMA2130 0.34805043149946097
'''

# 9.
dict = {} # Maps problems to their frequency
for line in lines: # Go through each line
    element = line.split()[8] # Find webwork element
    parts = element.split('/') # Split by '/'
    # Only consider elements with all the necessary pieces and whose 4th element is a digit
    if len(parts) > 5 and parts[4].isdigit():
        if element not in dict: # If the problem is not in the dict
            dict[element] = 1 # Add it to the dict with freq = 1
        else: # Else, increment its frequency
            dict[element] += 1

x = sum(dict.values()) # Sum the frequencies of all problems
print(x*100/n) # Find percentage

'''
9.
78.5079257482532
'''

# 10. 
asList = list(dict.items()) # Cast the dict as a list of tuples containing the problem name and frequency
byEntries = sorted(asList, key = lambda x: x[1], reverse=True) # Sort the list by the frequency
print(byEntries[0][0]) # Find the most frequent problem

'''
10.
[/webwork2/Spring11-STAT2120/Webwork09/22/]
'''
#%%
