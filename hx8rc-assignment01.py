##
## File: hx8rc-assignment01.py
## Topic: Assignment 1
## Name: Eric Xie
## Section time: 3:30-4:45
## Grading Group: 6


mylist01 = [2,5,4,9,10,-3,5,5,3,-8,0,2,3,8,8,-2,-4,0,6]
mylist02 = [-7,-3,8,-5,-5,-2,4,6,7,5,9,10,2,13,-12,-4,1]

## A1.

print(str(2**521 - 1)[-4:])

"""
A1.
7151
"""

## A2. 

print(mylist01[6] * mylist01[12] * mylist02[3])

"""
A2. 
-75
"""

## A3. 

mylist03 = mylist02[4:9]
print(mylist03)

"""
A3. 
[-5, -2, 4, 6, 7]
"""

## A4. 

mylist04 = mylist01+mylist02
print(sorted(mylist04)[7:19])

"""
A4. 
[-3, -3, -2, -2, 0, 0, 1, 2, 2, 2, 3, 3]
"""

## A5. 

count = 0
for i in mylist04:
	if i == 8:
		count=count+1
print(count)

"""
A5. 
3
"""

## A6. 

mylist05 = [x for x in mylist01 if x != 3]
print(mylist05)

"""
A6.
[2, 5, 4, 9, 10, -3, 5, 5, -8, 0, 2, 8, 8, -2, -4, 0, 6]
"""

## A7. 

print(mylist02[-1::-3])

"""
A7. 
[1, 13, 9, 6, -5, -3]
"""

## A8. 

print(mylist04[2::5])

"""
A8.
[4, 5, 3, 0, -5, 7, 13]
"""
#%%

mylist01 = [2,5,4,9,10,-3,5,5,3,-8,0,2,3,8,8,-2,-4,0,6]
mylist02 = [-7,-3,8,-5,-5,-2,4,6,7,5,9,10,2,13,-12,-4,1]

## B1. 

sum = 0
for i in mylist01:
	sum += i**3
print(sum)

"""
B1. 
2867
"""

## B2. 

mylist03 = []
for i in range(0,15):
	mylist03.append(mylist01[i] * mylist02[i])
print(mylist03)

"""
B2. 
[-14, -15, 32, -45, -50, 6, 20, 30, 21, -40, 0, 20, 6, 104, -96]
"""

## B3. 

sum = 0
for i in mylist02:
	sum += i
print(sum/len(mylist02))

"""
B3. 
1.588235294117647
"""

#%%

mylist01 = [2,5,4,9,10,-3,5,5,3,-8,0,2,3,8,8,-2,-4,0,6]
mylist02 = [-7,-3,8,-5,-5,-2,4,6,7,5,9,10,2,13,-12,-4,1]
mylist03 = [2,-5,6,7,-2,-3,0,3,0,2,8,7,9,2,0,-2,5,5,6]
biglist = mylist01 + mylist02 + mylist03

## C1. 

print(len([x for x in biglist if x > 4]))

"""
C1. 
23
"""

## C2. 

print(len([x for x in biglist if x>= -1 and x<=3]))

"""
C2. 
15
"""

## C3. 

mylist04 = [x for x in biglist if x % 3 != 0]
print(mylist04)

"""
C3.
[2, 5, 4, 10, 5, 5, -8, 2, 8, 8, -2, -4, -7, 8, -5, -5, -2, 4, 7, 5, 10, 2, 13, -4, 1, 2, -5, 7, -2, 2, 8, 7, 2, -2, 5, 5]
"""

#%%









