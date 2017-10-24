#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

def generate(n):
    length = 2*n
    text = ""

    for i in range(length):
        randomNumber = randint(0,1)
        if randomNumber == 0:
            text = text + "["
        else:
            text = text + "]"

    return text

def balanced(text):
    stack = []
    balanced = False

    for i in range(len(text)):
        if text[i] == "[":
            stack.append("[")
        else:
            if len(stack) == 0:
                return False
            else:
                top = stack.pop()

        if len(stack) == 0:
            balanced = True

    return balanced

print(balanced("[]][[]"))
