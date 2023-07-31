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
        usuarioIngresado = None
        contraseniaIngresada = None
        if request.method == 'POST':
            usuarioIngresado = request.form["nombre"]
            contraseniaIngresada = request.form["contrasenia"]

        #Abro mi archivo json y lo paso a un objeto de python en la variable users_registrados
            with open("usuarios.json", encoding="utf-8") as file:
                  registrados =json.load(file)

            #verifico si el usuario existe o no
            usuario_encontrado = False
            for usuario in registrados:
                  if usuario["nombre"] == usuarioIngresado and usuario["contrasenia"] == contraseniaIngresada:      
                        session ["nombre"] = usuarioIngresado
                        usuario_encontrado= True
                        break
              ####CORREGIR MENSAJE DE ERROR
            if usuario_encontrado:
                 return redirect(url_for('main'))
            mensajeError = "El usuario o contraseña son incorrectas"
            return render_template("error.html", error=mensajeError)
        
        return render_template("ingreso.html")


@app.route("/main")
def main():
    if "nombre" in session:
        return render_template("main.html")
    else:
        return redirect(url_for("login"))

@app.route("/ingreso")
def ingreso():
      return render_template("ingreso.html")


@app.route("/ultimaspelis")
def ultimas_peliculas():
         with open("peliculas.json", encoding="utf-8") as file:
            peliculas = json.load(file) 
            ultimas_10_peliculas = peliculas[-10:]
            return jsonify(ultimas_10_peliculas)

#REGISTRAR UN USUARIO
@app.route("/registro", methods=["POST", "GET"])
def registro():
    if request.method == "POST":
        nuevoUsuario = {
            "nombre": request.form["nombre"],
            "contrasenia": request.form["contrasenia"]
        }

        try:
            with open("usuarios.json", encoding="utf-8", mode="r+") as file:
                usuariosRegistrados = json.load(file)
        except FileNotFoundError:
            usuariosRegistrados = []

        # Verifico si el usuario esta registrado
        for usuario in usuariosRegistrados:
            if usuario["nombre"] == nuevoUsuario["nombre"]:
                mensajeError = "El usuario ya esta siendo utilizado"
                return render_template("error.html", error=mensajeError)

        # Agrego al usuario nuevo
        usuariosRegistrados.append(nuevoUsuario)

        with open("usuarios.json", encoding="utf-8", mode="w") as file:
            json.dump(usuariosRegistrados, file)

        return redirect(url_for('login'))

    return render_template("registro.html")






#BORRAR PELICULAS
@app.route("/borrar")
def borrar():
     return render_template("borrar.html") 

#AÑADIR PELICULA AL CATALOGO
@app.route("/agregar")
def agregar():
     return render_template("agregar.html")

@app.route("/error")
def error():
     return render_template("error.html")






#Si estamos en el archivo main de nuestra aplicacion, la ejecutamos
#Activamos la depuracion
if __name__== "__main__":
    app.run(debug=True)