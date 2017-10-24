#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def random_color():
    return random.sample(["blue", "cyan", "white", "black", "red", "green", "orange"],1)[0]

def random_rectangle():
    return """<rect x="{}" y="{}" height="{}" width="{}" fill="{}"/>""".format(
        random.randint(0,500),
        random.randint(0,500),
        random.randint(0,500),
        random.randint(0,500),
        random_color()
    )

def random_line():
    return """<line x1="{}" y1="{}" x2="{}" y2="{}" fill="{}"/>""".format(
        random.randint(0,500),
        random.randint(0,500),
        random.randint(0,500),
        random.randint(0,500),
        random_color()
    )

def random_ellipse():
    return """<ellipse cx="{}" cy="{}" rx="{}" ry="{}" fill="{}"/>""".format(
        random.randint(0,500),
        random.randint(0,500),
        random.randint(0,500),
        random.randint(0,500),
        random_color()
    )

def random_svg():
    svg = "<svg width=\"500\" height=\"500\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">"
    items = random.randint(1,150)

    typesOfItems = [random_rectangle, random_line, random_ellipse]

    for i in range(items):
        svg += random.sample(typesOfItems,1)[0]()

    svg += "</svg>"

    return svg
