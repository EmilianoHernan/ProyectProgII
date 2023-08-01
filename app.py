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

@app.route("/listaPelis")
def listaPelis():
    with open("peliculas.json", encoding="utf-8") as file:
        lista_de_peliculas = json.load(file)
    return render_template("listaPelis.html", peliculas=lista_de_peliculas)


#BORRAR PELICULAS
# Ruta para borrar una película
@app.route("/borrar", methods=["GET", "POST"])
def borrar():
    with open("peliculas.json", encoding="utf-8") as file:
        listaPeliculas = json.load(file)

    if request.method == "POST":
        nombrePelicula = request.form["peli"]


        peliculaEncontrada = None
        for pelicula in listaPeliculas:
            if pelicula["nombre"] == nombrePelicula:
                peliculaEncontrada = pelicula
                break

        #mensaje de error
        if peliculaEncontrada == None:
            mensaje_error = "La película no existe."
            return render_template("borrar.html", error=mensaje_error)
        
        # Viendo los comentarios
        if peliculaEncontrada.get("comentarios"):
            mensaje_error = "No se puede eliminar la película, tiene comentarios de usuarios."
            return render_template("error.html", error=mensaje_error)

        # Elimino la pelicula
        listaPeliculas.remove(peliculaEncontrada)

        with open("peliculas.json", "w", encoding="utf-8") as file:
            json.dump(listaPeliculas, file)

        mensaje_exito = "La película ha sido eliminada con éxito."
        return render_template("exito.html", mensaje_exito=mensaje_exito)

    return render_template("borrar.html")













#AÑADIR PELICULA AL CATALOGO
@app.route("/agregar", methods=["POST", "GET"])
def agregar():
     if request.method == "POST":
          nombre= request.form["nombre"]
          anio= request.form["anio"]
          director= request.form["director"]
          genero= request.form["genero"]
          sinopsis= request.form["sinopsis"]
          imagen= request.form["imagen"]
          comentario= request.form["comentario"]

          nuevaPeli={
               "nombre": nombre,
               "anio": anio,
               "director": director,
               "genero": genero,
               "sinopsis": sinopsis,
               "imagen": imagen,
               "comentarios": {} if not comentario else {1: comentario}
          }

        #Agregando la nueva pelicula al json
          with open("peliculas.json", encoding="utf-8") as file:
               listaPelis= json.load(file)

          listaPelis.append(nuevaPeli)

          with open("peliculas.json", "w", encoding="utf-8") as file:
               json.dump(listaPelis, file)

          return redirect(url_for("listaPelis"))


     return render_template("agregar.html")

@app.route("/error")
def error():
     return render_template("error.html")


@app.route("/editar")
def editar():
     return render_template("editar.html")


#Si estamos en el archivo main de nuestra aplicacion, la ejecutamos
#Activamos la depuracion
if __name__== "__main__":
    app.run(debug=True)