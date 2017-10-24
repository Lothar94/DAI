#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def exercise2():
    naturalnumber = int(input("Introduce un número natural: "))

    allNumbers = range(0, naturalnumber)
    checked = []
    primes = []

    for i in allNumbers:
        checked.append(False)

    for i in range(2, int(math.sqrt(naturalnumber))):
        if not checked[i]:
            for j in range(i, int(naturalnumber/i)):
                checked[i*j] = True

    for i in allNumbers:
        if not checked[i]:
            primes.append(i)

    primes.append(naturalnumber)

    return primes

exercise2()
