#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import *

from mandelbrot import *
from io import BytesIO
from datetime import datetime
from svg_randomizer import random_svg

import base64
import random
import shelve
import re
import os

app = Flask(__name__)
app.secret_key = "Lothar-is-my-name"

#-----------------------------------------------------------
# Función: AddLink(link)
# Argumentos: link - Cadena de texto con un enlace a web
# Salida: void
# Descripción: Gestiona a través de sesiones los últimos sitios visitados por el
# usuario.
#-----------------------------------------------------------
def AddLink(link):
    if "last_visited" not in session:
        session["last_visited"] = []
        print(session["last_visited"])
    session["last_visited"].append(link)
    if len(session["last_visited"]) > 10:
        session["last_visited"].pop(0)
    session.modified = True

#-----------------------------------------------------------
# Función: load_cache()
# Argumentos: void
# Salida: cache - Lista de archivos que están en cache
# Descripción: Gestiona la cache de archivos del directorio /dynamic que contiene
# las imágenes generadas de forma dinamica por la función mandelbrot. Además se encarga
# de eliminar las imágenes con más de un dia de antigüedad.
#-----------------------------------------------------------
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

#-----------------------------------------------------------
# Función: parse_palette(string)
# Argumentos: string - Cadena de texto
# Salida: palette - Lista de tuplas RGB
# Descripción: Gestiona la entrada en string de una paleta de colores RGB, aplicando
# una expresión regular para obtener cada uno de los números y tomándolos de tres
# en tres.
#-----------------------------------------------------------
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

#-----------------------------------------------------------
# Función: hello()
# Argumentos: void
# Salida: "Hello World!"
# Descripción: Hola mundo inicial
#-----------------------------------------------------------
@app.route("/Hello")
def hello():
    AddLink("/Hello")
    return "Hello World!"

#-----------------------------------------------------------
# Función: index()
# Argumentos: void
# Salida: render_template - Renderizado del template seleccionado
# Descripción: Gestor del enlace raíz.
#-----------------------------------------------------------
@app.route("/")
def index():
    AddLink("/")
    if "username" in session and "password" in session:
        return render_template("index.html", username = session["username"], historial = session["last_visited"])
    else:
        return render_template("index.html", historial = session["last_visited"])

#-----------------------------------------------------------
# Función: login()
# Argumentos: void
# Salida: redirect - Rediriección al directorio raiz
# Descripción: Gestiona los formularios de login, comprueba que el usuario introducido
# esté en la bd y que el password introducido coincida con el de la bd. Si esto es así
# se crea la sesión para ese usuario.
#-----------------------------------------------------------
@app.route("/login", methods = ["POST"])
def login():
    db = shelve.open("users.dat")
    username = request.form.get("username")
    password = request.form.get("password")

    if username in db and db[username]["password"] == password:
        session["username"] = username
        session["password"] = password

    db.close()
    return redirect("/")

#-----------------------------------------------------------
# Función: singup()
# Argumentos: void
# Salida: redirect - Rediriección al directorio raiz
# Descripción: Gestiona los formularios de registro, permite crear un nuevo usuario
# a menos que ya exista en la base de datos.
#-----------------------------------------------------------
@app.route("/singup", methods = ["POST"])
def singup():
    db = shelve.open("users.dat")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if username in db:
        db.close()
        return render_template("1.html", historial = session["last_visited"])

    session["username"] = username
    session["password"] = password
    db[username] = {"username": username, "email": email, "password": password}
    db.close()
    return redirect("/")

#-----------------------------------------------------------
# Función: logout()
# Argumentos: void
# Salida: redirect - Rediriección al directorio raiz
# Descripción: Gestiona el boton de logout, elimina la sesión actual.
#-----------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#-----------------------------------------------------------
# Función: show_user_info()
# Argumentos: void
# Salida: redirect - Rediriección al directorio raiz, render_template - Template info_user.html
# Descripción: Gestiona el template que se encarga de mostrar la información del usuario
# en el caso de que este tenga una sesión activa si no, se redirige al usuario al directorio raiz.
#-----------------------------------------------------------
@app.route("/user_info")
def show_user_info():
    if "username" in session:
        AddLink("/user_info")
        db = shelve.open("users.dat")
        email = db[session["username"]]["email"]
        return render_template("user_info.html", username = session["username"], password = session["password"], email = email , historial = session["last_visited"])
    else:
        return redirect("/")

#-----------------------------------------------------------
# Función: edit_user_info()
# Argumentos: void
# Salida: redirect - Rediriección al directorio /user_info
# Descripción: Gestiona el formulario de edición de información de usuarios.
#-----------------------------------------------------------
@app.route("/edit_info", methods=["POST"])
def edit_user_info():
    if "username" in session:
        db = shelve.open("users.dat", writeback=True)

        username = session["username"]

        email = request.form.get("email")
        password = request.form.get("password")

        db[username]["email"] = email
        db[username]["password"] = password

        session["password"] = password

        db.close()

        return redirect("/user_info")
    else:
        return redirect("/")

#-----------------------------------------------------------
# Función: about()
# Argumentos: void
# Salida: render_template - Renderiza el template /about
# Descripción: Muestra la información de las prácticas
#-----------------------------------------------------------
@app.route("/about")
def about():
    AddLink("/about")
    if "username" in session:
        return render_template("about.html", username = session["username"], historial = session["last_visited"])
    else:
        return render_template("about.html", historial = session["last_visited"])

#-----------------------------------------------------------
# Función: show_user_get()
# Argumentos: void
# Salida: redirect - Redirección a /user/<username>
# Descripción: Gestiona peticiones get para acceder a la web de los usuarios mediante formularios.
#-----------------------------------------------------------
@app.route("/user_get", methods = ["GET"])
def show_user_get():
    result = request.args.get('username')
    return redirect("/user/"+result)

#-----------------------------------------------------------
# Función: show_user()
# Argumentos: username - Cadena de texto
# Salida: render_template - Renderiza el template /user/<username>
# Descripción: Genera un template con el nombre de usuario dado por argumento.
#-----------------------------------------------------------
@app.route("/user/<username>")
def show_user(username):
    AddLink("/user/"+username)
    if "username" in session:
        return render_template("user.html", user = username, username = session["username"], historial = session["last_visited"])
    else:
        return render_template("user.html", user = username, historial = session["last_visited"])

#-----------------------------------------------------------
# Función: render_mandelbrot()
# Argumentos: void
# Salida: render_template - Renderiza el template /mandelbrot
# Descripción: A partir de coordenadas dadas por un formulario se crea un template con
# el resultado de la ejecución de la función mandelbrot(), además comprueba si la imagen
# ha sido solicitada previamente en cuyo caso la recupera directamente, si no la recalcula.
#-----------------------------------------------------------
@app.route("/mandelbrot", methods = ["GET"])
def render_mandelbrot():
    AddLink(request.url)
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

    if "username" in session:
        return render_template("binaryImg.html", img = img, username = session["username"], historial = session["last_visited"])
    else:
        return render_template("binaryImg.html", img = img, historial = session["last_visited"])

#-----------------------------------------------------------
# Función: render_random_svg()
# Argumentos: void
# Salida: render_template - Renderiza el template /svg
# Descripción: Gestiona el template randsvg que muestra imagenes aleatorias vectorizadas.
#-----------------------------------------------------------
@app.route("/svg")
def render_random_svg():
    AddLink("/svg")
    if "username" in session:
        return render_template("randsvg.html", img = random_svg(), username = session["username"], historial = session["last_visited"])
    else:
        return render_template("randsvg.html", img = random_svg(), historial = session["last_visited"])

#-----------------------------------------------------------
# Función: not_found()
# Argumentos: void
# Salida: render_template - Renderiza el template /404
# Descripción: Error 404
#-----------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", historial = session["last_visited"]), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
