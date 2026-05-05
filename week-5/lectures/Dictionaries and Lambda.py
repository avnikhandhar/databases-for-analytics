#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on ???

@author: fitsstudiouser
"""

 extensions = {111:'Alex', 222: 'Jane'}

 extensions[222]

extensions[333] = 'Mike'
extensions['Default'] = 'Operator'

extensions[333] = 'Mike2'
extensions[333]

extensions[555]

if 555 in extensions:
    extensions[555]

extensions[555] = 'dummy'

extensions.pop(555)

extensions.keys()
for key in extensions.keys():
    print(key)

for value in extensions.values():
    print (value)

extensions.items()

for (key, value) in extensions.items():
    print (key, '-->', value)

def timesTwo(x):
    return x*2

def mySquare(x):
    return x*x

def applyFunc(myFunc, value):
    return myFunc(value)

applyFunc(timesTwo, 10)
applyFunc(mySquare, 10)

lambda x: x*x  # This is a nameless square function

applyFunc( lambda x: x*x, 10)

mySquare2 = lambda x: x*x

applyFunc( mySquare2, 10)


