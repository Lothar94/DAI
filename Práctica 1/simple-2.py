#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import time

def bubbleSort(input_list):
    n = len(input_list)
    for i in range(1,n):
        for j in range(0,n-i):
            if input_list[j] > input_list[j+1]:
                aux = input_list[j]
                input_list[j] = input_list[j+1]
                input_list[j+1] = aux

def selectionSort(input_list):
    n = len(input_list)
    for i in range(0,n-1):
        minimum = i
        for j in range(i+1,n):
            if input_list[j] < input_list[minimum]:
                minimum = j
        aux = input_list[i]
        input_list[i] = input_list[minimum]
        input_list[minimum] = aux

def randomTest(n,t,a,b):
    for i in range(n):
        l = []
        for j in range(t):
            l.append(randint(a,b))
        print(l)
        init = time.time()
        bubbleSort(list(l))
        end = time.time()
        total = end - init
        print("bubbleSort: "+str(total))
        init = time.time()
        selectionSort(list(l))
        end = time.time()
        total = end - init
        print("selectionSort: "+str(total))

randomTest(3,10,1,9)
