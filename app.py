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

@app.route("/ultimaspelis")
def ultimas_peliculas():
         with open("peliculas.json", encoding="utf-8") as file:
            peliculas = json.load(file) 
            ultimas_10_peliculas = peliculas[-10:]
            return jsonify(ultimas_10_peliculas)




#Si estamos en el archivo main de nuestra aplicacion, la ejecutamos
#Activamos la depuracion
if __name__== "__main__":
    app.run(debug=True)