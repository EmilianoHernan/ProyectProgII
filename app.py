from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

#Enrutamientos, Ruta raiz "/"
@app.route('/') 
def index():
    return render_template('index.html')

@app.route("/login")
def login():
        return render_template("ingreso.html")

@app.rout("/ultimaspelis")
def ultimas_peliculas():
     return peliculas.json





#Si estamos en el archivo main de nuestra aplicacion, la ejecutamos
#Activamos la depuracion
if __name__== "__main__":
    app.run(debug=True)