from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key='LaCoMuNAOSOS'

#Enrutamientos, Ruta raiz "/"
@app.route('/') 
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
        usuarioIngresado = None # Asignandole valor predeterminado a la variable, sino rompe el codigo
        #Abro mi archivo json y lo paso a un objeto de python en la variable users_registrados
        with open("usuarios.json", encoding="utf-8") as file:
              registrados =json.load(file)
            
        if request.method == "POST" :
              usuarioIngresado = request.form["nombre"]
              contraseniaIngresada = request.form["contrasenia"]

        #verifico si el usuario existe o no
        for usuario in registrados:
              if usuario["nombre"] == usuarioIngresado and usuario["contrasenia"] == contraseniaIngresada:      
                session ["nombre"] = usuarioIngresado
                return redirect (url_for("main"))
        else:
              mensajeError = "Usuario o contraseña incorrectas, vuelve a intentarlo"
              return render_template ('ingreso.html', error = mensajeError)


@app.route("/main")
def main():
    if "nombre" in session:
        return render_template("main.html")
    else:
        return redirect(url_for("login"))

@app.route("/ingreso")
def ingresar():
      return render_template("ingreso.html")


@app.route("/ultimaspelis")
def ultimas_peliculas():
         with open("peliculas.json", encoding="utf-8") as file:
            peliculas = json.load(file) 
            ultimas_10_peliculas = peliculas[-10:]
            return jsonify(ultimas_10_peliculas)

@app.route("/registro")
def registro():
      return render_template("registro.html")       




#Si estamos en el archivo main de nuestra aplicacion, la ejecutamos
#Activamos la depuracion
if __name__== "__main__":
    app.run(debug=True)