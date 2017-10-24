#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

string = input("Introduce una cadena de texto: ")
select_exercise = int(input("Número de 1 a 3: "))
while select_exercise > 3 or select_exercise < 1:
    select_exercise = int(input("Número invalido introduce uno del 1 a 3: "))

def exercise1(string):
    pattern = re.compile(r"\b(\w+)\b\s[A-Z]")
    return pattern.findall(string)

def exercise2(string):
    pattern = re.compile(r"\b[\w._-]+@[\w]+\.[\w]+\b")
    return pattern.findall(string)

def exercise3(string):
    pattern = re.compile(r"[1-9]{4}(\s-)[1-9]{4}\1[1-9]{4}\1[1-9]{4}")
    return pattern.findall(string)

options = {1:exercise1, 2:exercise2, 3:exercise3}
print(options[select_exercise](string))
