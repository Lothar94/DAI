#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mandelbrot import *
import random

x1 = int(input("Introduce la dupla de coordenada x1: "))
x2 = int(input("Introduce la dupla de coordenada x2: "))

y1 = int(input("Introduce la dupla de coordenada y1: "))
y2 = int(input("Introduce la dupla de coordenada y2: "))

width = int(input("Introduce el ancho de representación: "))
times = int(input("Introduce el números de iteraciones: "))

shufflepalette = input("Aleatorizar orden de la paleta de colores (yes|no): ")

palette = [(88,140,115), (242,227,148), (242,174,114), (217,100,89), (140,70,70)]

if shufflepalette == "yes":
    random.shuffle(palette)

renderizaMandelbrotBonito(x1, x2, y1, y2, width, times, "mandelbrot.png", palette, len(palette))
