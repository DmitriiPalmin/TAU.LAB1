import math as m
import numpy as n
import main

from math import sqrt as s

rr = s(4)

print(rr)

main.print_hi(m.pi)




# переменные, туда-сюда

value = 10.1

age =  21

age2 = float (age)

str2 = "Я люблю МЭИ"

str1 = " по субботам"

sum1 = value + float(age)

s = list()

s1 = [1, 2]

s1.append(3)

s1[1] = 14

s3 = tuple()
s3 = (1, 3)

d = dict()

d = {1 : 'Vasya'}
d = {2 : 'Semen'}

a = d.get(2)

# множество
s = set()

s.add(2)
s.add(13)
s.add(7)

# for i in range (2, 10, 2):
#     print(i)

for j in s1:
    print (j)

# for letter in 'лучший':
#     if letter == 'и':
#         letter = 'а'
#     elif letter == 'й':
#         letter = 'я'
#     print(letter)
x = 45
# def y_ot_x(f):
#     print('in method')
#     return f*2
# value = y_ot_x(x)
#
# def func(*args):
#     # for argument in args:
#         print(args)

val0 = 10
q = 3
# func(1, 'a0', True)

def newfunc():
    val1 = val0
    return val1

print(newfunc())


print (val0)
print (str1 + str2 + " " + str(value) + " раз")