#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------
#   Ejercicio 1
#-----------------------------------------------------------

from random import randint
import math

def exercise1():
    rnumber = randint(1,100)
    attemps = 0

    win = False

    print("Adivina un número entre el 1 y el 100")

    while (not win and attemps < 10):
        playernumber = input("Numero: ")

        while playernumber == '':
            playernumber = input("Numero: ")

        playernumber = int(playernumber)

        if playernumber == rnumber:
            win = True
        elif playernumber < rnumber:
            print("El número buscado es mayor")
        else:
            print("El número buscado es menor")

        attemps += 1
        print("Intentos restantes: " + str(10-attemps))

    if attemps == 10:
        print("LOSER")
    else:
        print("WINNER")

exercise1()
