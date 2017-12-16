##
## File: assignment02.py (STAT 3250)
## Topic: Assignment 2
## Name: Eric Xie
## Section time: 3:30-4:45
## Grading Group: 6


import numpy as np 
#### Assignment 2, Part A
##
## A1. 

x = np.random.uniform(low=0,high=20,size=10000)
count = 0
for i in x:
	if i>=5 and i<=12:
		count += 1
print(count/100)

"""
A1.
35.09
"""

## A2. 

ctarray = np.zeros(500)
for i in range(500):
	x = np.random.uniform(low=0,high=20,size=10000)
	ct = 0
	for val in x:
		if val>=5 and val<=12:
			ct += 1
	ctarray[i] = ct/100
print(np.mean(ctarray))

"""
A2.
34.9824
"""

## A3. 

ct = 1
s = np.random.choice(x, size=1)
while s >= 4:
	ct += 1
	s = np.random.choice(x, size=1)
print(ct)

"""
A3.
10
"""

## A4. 

ctarray = np.zeros(1000)
for i in range(1000):
	ct = 1
	s = np.random.choice(x, size=1)
	while s >= 4:
		ct += 1
		s = np.random.choice(x, size=1)
	ctarray[i] = ct
print(np.mean(ctarray))

"""
A4.
5.012
"""

## A5. 

ct = 1
encountered = 0
s = np.random.choice(x, size=1)
if s > 12:
	encountered += 1
while encountered < 3:
	ct += 1
	s = np.random.choice(x, size=1)
	if s > 12:
		encountered += 1
print(ct)

"""
A5. 
9
"""

## A6. 

ctarray = np.zeros(1000)
for i in range(1000):
	ct = 1
	encountered = 0
	s = np.random.choice(x, size=1)
	if s > 12:
		encountered += 1
	while encountered < 3:
		ct += 1
		s = np.random.choice(x, size=1)
		if s > 12:
			encountered += 1
	ctarray[i] = ct
print(np.mean(ctarray))	

"""
A6.
7.544
"""
#%%

p1 = np.random.normal(40,12,size=500000)

#  a) 
#
#   i) 

ct = 0
for i in range(10000):
	s = np.random.choice(p1, size=10)
	xbar = np.mean(s)
	sigma = 12
	n = 10
	ci = [xbar - 1.96*sigma/np.sqrt(n), xbar + 1.96*sigma/np.sqrt(n)]
	if ci[0] <= 40 and ci[1] >= 40:
		ct += 1
print(ct/10000)

"""
Bai.
0.9158
"""

#   ii) 

ct = 0
for i in range(10000):
	s = np.random.choice(p1, size=20)
	xbar = np.mean(s)
	sigma = 12
	n = 20
	ci = [xbar - 1.96*sigma/np.sqrt(n), xbar + 1.96*sigma/np.sqrt(n)]
	if ci[0] <= 40 and ci[1] >= 40:
		ct += 1
print(ct/10000)

"""
Baii.
0.9376
"""

#   iii) 
ct = 0
for i in range(10000):
	s = np.random.choice(p1, size=30)
	xbar = np.mean(s)
	sigma = 12
	n = 30
	ci = [xbar - 1.96*sigma/np.sqrt(n), xbar + 1.96*sigma/np.sqrt(n)]
	if ci[0] <= 40 and ci[1] >= 40:
		ct += 1
print(ct/10000)

"""
Baiii.
0.9425
"""
#
#  b) 
#
ct = 0
for i in range(10000):
	s = np.random.choice(p1, size=10)
	xbar = np.mean(s)
	sigma = np.std(s, ddof=1)
	n = 10
	ci = [xbar - 1.96*sigma/np.sqrt(n), xbar + 1.96*sigma/np.sqrt(n)]
	if ci[0] <= 40 and ci[1] >= 40:
		ct += 1
print(ct/10000)

"""
Bbi.
0.9158
"""

#   ii) 
ct = 0
for i in range(10000):
	s = np.random.choice(p1, size=20)
	xbar = np.mean(s)
	sigma = np.std(s, ddof=1)
	n = 20
	ci = [xbar - 1.96*sigma/np.sqrt(n), xbar + 1.96*sigma/np.sqrt(n)]
	if ci[0] <= 40 and ci[1] >= 40:
		ct += 1
print(ct/10000)

"""
Bbii.
0.9376
"""

#   iii) Repeat part i) using samples of size 30.
ct = 0
for i in range(10000):
	s = np.random.choice(p1, size=30)
	xbar = np.mean(s)
	sigma = np.std(s, ddof=1)
	n = 30
	ci = [xbar - 1.96*sigma/np.sqrt(n), xbar + 1.96*sigma/np.sqrt(n)]
	if ci[0] <= 40 and ci[1] >= 40:
		ct += 1
print(ct/10000)

"""
Bbiii.
0.9425
"""
#  c)

ct = 0
for i in range(10000):
	s = np.random.choice(p1, size=10)
	xbar = np.mean(s)
	sigma = np.std(s, ddof=1)
	n = 10
	t = 2.262
	ci = [xbar - t*sigma/np.sqrt(n), xbar + t*sigma/np.sqrt(n)]
	if ci[0] <= 40 and ci[1] >= 40:
		ct += 1
print(ct/10000)

"""
Bci.
0.9446
"""

#   ii) 
ct = 0
for i in range(10000):
	s = np.random.choice(p1, size=20)
	xbar = np.mean(s)
	sigma = np.std(s, ddof=1)
	n = 20
	t = 2.093
	ci = [xbar - t*sigma/np.sqrt(n), xbar + t*sigma/np.sqrt(n)]
	if ci[0] <= 40 and ci[1] >= 40:
		ct += 1
print(ct/10000)

"""
Bcii.
0.952
"""

#   iii) 
ct = 0
for i in range(10000):
	s = np.random.choice(p1, size=30)
	xbar = np.mean(s)
	sigma = np.std(s, ddof=1)
	n = 30
	t = 2.045
	ci = [xbar - t*sigma/np.sqrt(n), xbar + t*sigma/np.sqrt(n)]
	if ci[0] <= 40 and ci[1] >= 40:
		ct += 1
print(ct/10000)

"""
Bciii.
0.9522
"""









