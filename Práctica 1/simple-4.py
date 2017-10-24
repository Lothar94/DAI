#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def fibonacci(n):
    f = [0, 1]
    for i in range(2,n+1):
        f.append(f[i-1] + f[i-2])
    return f

def nesimefibonacci(n):
    return fibonacci(n)[n]


if len(sys.argv) == 2:
    try:
        file_to_read = open(sys.argv[1], "r")
        file_to_write = open("output", "w")

        n = int(file_to_read.read())
        file_to_write.write(str(nesimefibonacci(n)))

        file_to_read.close()
        file_to_write.close()
    except IOError:
        print("Error, El archivo introducido no existe")
else:
    print("No se han pasado el número correcto de argumentos (1)")
