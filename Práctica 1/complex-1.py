#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, './lib')

from random import randint
from graphics import *

def generateBlankTable(n,m):
    table = []
    for i in range(n):
        table.append([])
        for j in range(m):
            table[i].append(False)
    return table

def generateInitialState(table):
    n = randint(0,len(table)*len(table[0])-1)
    for k in range(n):
        i = randint(0,len(table)-1)
        j = randint(0,len(table[0])-1)
        table[i][j] = True

def generateInitialStateSpecified(table,n):
    for k in range(n):
        i = randint(0,len(table)-1)
        j = randint(0,len(table[0])-1)
        table[i][j] = True

def checkNeighboors(table,i,j):
    neighboorsAlive = 0
    if i > 0 and j > 0 and i < len(table)-1 and j < len(table[0])-1:
        for s in range(i-1,i+2):
            for t in range(j-1,j+2):
                if table[s][t] and (s != i or t != j):
                    neighboorsAlive += 1
    elif i == 0 and j > 0 and j < len(table[0])-1:
        for s in range(i,i+2):
            for t in range(j-1,j+2):
                if table[s][t] and (s != i or t != j):
                    neighboorsAlive += 1
    elif i == len(table)-1 and j > 0 and j < len(table[0])-1:
        for s in range(i-1,i+1):
            for t in range(j-1,j+2):
                if table[s][t] and (s != i or t != j):
                    neighboorsAlive += 1
    elif j == 0 and i > 0 and i < len(table[0])-1:
        for s in range(i-1,i+2):
            for t in range(j,j+2):
                if table[s][t] and (s != i or t != j):
                    neighboorsAlive += 1
    elif j == len(table[0])-1 and i > 0 and i < len(table[0])-1:
        for s in range(i-1,i+2):
            for t in range(j-1,j+1):
                if table[s][t] and (s != i or t != j):
                    neighboorsAlive += 1
    elif i == 0 and j == 0:
        for s in range(i,i+2):
            for t in range(j,j+2):
                if table[s][t] and (s != i or t != j):
                    neighboorsAlive += 1
    elif i == 0 and j == len(table[0])-1:
        for s in range(i,i+2):
            for t in range(j-1,j+1):
                if table[s][t] and (s != i or t != j):
                    neighboorsAlive += 1
    elif i == len(table)-1 and j == 0:
        for s in range(i-1,i+1):
            for t in range(j,j+2):
                if table[s][t] and (s != i or t != j):
                    neighboorsAlive += 1
    elif i == len(table)-1 and j == len(table[0])-1:
        for s in range(i-1,i+1):
            for t in range(j-1,j+1):
                if table[s][t] and (s != i or t != j):
                    neighboorsAlive += 1

    return neighboorsAlive

def drawInitialState(state, window, n, m):
    listOfPoints = []
    listOfRectangles = []
    s = 0
    for i in range(0, 400, int(400/n)):
        t = 0
        for j in range(0, 400, int(400/m)):
            rectangle = Rectangle(Point(i,j),Point(i+int(400/n),j+int(400/m)))
            if state[s][t]:
                #listOfPoints.append((Point(i,j),Point(i+int(400/n),j+int(400/m))))
                rectangle.setFill("black")
            else:
                rectangle.setFill("white")
            rectangle.draw(window)
            update(120)
            listOfRectangles.append(rectangle)
            t += 1
        s += 1

    return listOfRectangles

def drawState(state, window, n, m, listOfRectangles):
    x = 0
    for i in range(n):
        for j in range(m):
            listOfRectangles[x].undraw()
            if state[i][j]:
                listOfRectangles[x].setFill("black")
            else:
                listOfRectangles[x].setFill("white")
            listOfRectangles[x].draw(window)
            update(120)
            x += 1

def lifeGame(n,m,generations):
    window = GraphWin("Life Game", 400, 400, autoflush=False)
    state = generateBlankTable(n,m)
    generateInitialStateSpecified(state,200)
    listOfRectangles = drawInitialState(state, window,n,m)

    #for row in state:
    #    print(row)
    #print()

    for turns in range(generations):
        print("Turno: "+str(turns))
        new_state = list(state)
        for i in range(n):
            for j in range(m):
                k = checkNeighboors(state, i, j)
                #print(str(i)+" "+str(j)+" "+str(k))
                if not state[i][j] and k == 3:
                    new_state[i][j] = True
                elif state[i][j] and (k == 2 or k == 3):
                    new_state[i][j] = True
                else:
                    new_state[i][j] = False
        state = new_state
        drawState(state, window, n, m, listOfRectangles)

        #for row in state:
        #    print(row)
        #print()
    return window


window = lifeGame(40,40,int(input("Introduce número de iteraciones: ")))
window.getMouse()
window.close()
