#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import *

from mandelbrot import *
import random
from io import BytesIO
import base64
from datetime import datetime
from svg_randomizer import random_svg

import re
import os

app = Flask(__name__)

def load_cache():
    cache = list(os.listdir("./dynamic"))
    cache.remove(".DS_Store")

    today = datetime.today()

    for f in cache:
        d = datetime.fromtimestamp(os.path.getmtime("./dynamic/"+f)).day
        print(str(abs(today.day-d)))
        if abs(today.day-d) >= 1:
            os.remove("./dynamic/"+f)
            cache.remove(f)

    return cache

def parse_palette(string):
    palette = []
    pattern = re.compile(r"([0-9]+)")
    results = pattern.findall(string)

    aux = []
    for i in range(len(results)):
        if (i+1)%3 == 0:
            aux.append(int(results[i]))
            palette.append(tuple(aux))
            aux = []
        else:
            aux.append(int(results[i]))

    return palette


@app.route("/Hello")
def hello():
    return "Hello World!"

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/user_get", methods = ["GET"])
def show_user_get():
    result = request.args.get('username')
    return show_user(result)

@app.route("/user/<username>")
def show_user(username):
    return render_template("user.html", username = username)

@app.route("/mandelbrot", methods = ["GET"])
def render_mandelbrot():
    x1 = int(request.args.get('x1'))
    x2 = int(request.args.get('x2'))
    y1 = int(request.args.get('y1'))
    y2 = int(request.args.get('y2'))
    initial_palette = request.args.get('palette')

    cache = load_cache()

    palette = parse_palette(initial_palette)
    random.shuffle(palette)

    file_name = "mandel"+str(x1)+str(x2)+str(y1)+str(y2)+initial_palette+".png".replace(" ","")

    if file_name not in cache:
        output = BytesIO()
        renderizaMandelbrotBonito(x1, x2, y1, y2, 300, 100, output, "./dynamic/"+file_name, palette, len(palette))
        img = base64.b64encode(output.getvalue()).decode("ascii")
        output.close()
    else:
        with open("./dynamic/"+file_name, "rb") as f:
            img = base64.b64encode(f.read()).decode("ascii")

    return render_template("binaryImg.html", img = img)

@app.route("/svg")
def render_random_svg():
    return render_template("randsvg.html", img = random_svg(), code=escape(open("svg_randomizer.py", "r").read()))

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
