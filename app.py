
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

            with open("usuarios.json", encoding="utf-8") as file:
                  registrados =json.load(file)

            #verifico si el usuario existe o no
            usuario_encontrado = False
            for usuario in registrados:
                  if usuario["nombre"] == usuarioIngresado and usuario["contrasenia"] == contraseniaIngresada:      
                        session ["nombre"] = usuarioIngresado
                        usuario_encontrado= True
                        break  
            if usuario_encontrado:
                 return redirect(url_for('main'))
            mensajeError = "El usuario o contraseña son incorrectas"
            return render_template("error_ingreso.html", error=mensajeError)
        
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

#Enrutador de las ultimas 10 peliculas
@app.route("/ultimaspelis", methods=["GET"])
def ultimas_peliculas():
         with open("peliculas.json", encoding="utf-8") as file:
            peliculas = json.load(file) 
            ultimas10Peliculas = peliculas[-10:]
            return jsonify(ultimas10Peliculas)



#REGISTRAR UN USUARIO
@app.route("/registro", methods=["POST", "GET"])
def registro():
    if request.method == "POST":
        nuevoUsuario = {
            "nombre": request.form["nombre"],
            "contrasenia": request.form["contrasenia"]
        }
        # Bloque de excepcion de usuario
        try:
            with open("usuarios.json", encoding="utf-8", mode="r+") as file:
                usuariosRegistrados = json.load(file)
        except FileNotFoundError:
                usuariosRegistrados = []

        # Verifico si el usuario esta registrado
        for usuario in usuariosRegistrados:
            if usuario["nombre"] == nuevoUsuario["nombre"]:
                mensajeError = "El usuario ya esta siendo utilizado"
                return render_template("error", error=mensajeError)

        # Agrego al usuario nuevo
        usuariosRegistrados.append(nuevoUsuario)

        with open("usuarios.json", encoding="utf-8", mode="w") as file:
            json.dump(usuariosRegistrados, file)

        return redirect(url_for('login'))

    return render_template("registro.html")




#BORRAR PELICULAS

@app.route("/borrar", methods=["GET", "POST"])
def borrar():
    with open("peliculas.json", encoding="utf-8") as file:
        listaPeliculas = json.load(file)

    if request.method == "POST":
        nombrePelicula = request.form["peli"]

        #buscamos la pelicula
        peliculaEncontrada = None
        for pelicula in listaPeliculas:
            if pelicula["nombre"] == nombrePelicula:
                peliculaEncontrada = pelicula
                break

        #si no la encontramos
        if peliculaEncontrada == None:
            mensaje_error = "La película no existe."
            return render_template("borrar.html", error=mensaje_error)
        
        # si Si la encontramos
        if peliculaEncontrada.get("comentarios"):
            mensaje_error = "No se puede eliminar la película, tiene comentarios de usuarios."
            return render_template("error_borrar.html", error=mensaje_error)


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



#Editar una pelicla
def obtenerNombrePelicula(nombrePelicula):
    with open("peliculas.json", encoding="utf-8") as file:
        listaPeliculas = json.load(file)
    for pelicula in listaPeliculas:
        if pelicula["nombre"] == nombrePelicula:
            return pelicula
    return None

def actualizarPelicula(pelicula_actualizada):
    with open("peliculas.json", encoding="utf-8") as file:
        listaPeliculas = json.load(file)
    for pelicula in listaPeliculas:
        if pelicula["nombre"] == pelicula_actualizada["nombre"]:
            pelicula.update(pelicula_actualizada)
            break
    with open("peliculas.json", "w", encoding="utf-8") as file:
        json.dump(listaPeliculas, file)

@app.route("/editar", methods=["GET", "POST"])
def editar():
    if request.method == "POST":
        nombrePelicula = request.form["pelicula"]
        infoEditada = {
            "nombre": nombrePelicula,
            "anio": request.form["anio"],
            "director": request.form["director"],
            "genero": request.form["genero"],
            "sinopsis": request.form["sinopsis"],
            "imagen": request.form["imagen"],
            "comentarios": obtenerNombrePelicula(nombrePelicula)["comentarios"]
        }

        actualizarPelicula(infoEditada)

        return redirect(url_for("infoPelis"))

    return render_template("editar.html")


#Buscar una pelicula
@app.route("/buscaPelis", methods=["GET", "POST"])
def buscaPelis():
    if request.method== "POST":
        busco_pelis = request.form ["busco_pelis"].lower()
        with open("peliculas.json", encoding="utf-8")as file:
            listaPelis= json.load(file)

        peliculasEncontradas= [pelicula for pelicula in listaPelis if busco_pelis in pelicula["nombre"].lower()]

        if not peliculasEncontradas:
            mensajeError = "No se encontraron peliculas que coincidan con la búsqueda."
            return render_template("error.html", error=mensajeError)
        
        return render_template("buscaPelis.html", peliculas=peliculasEncontradas, query=busco_pelis)
    return render_template("buscaPelis.html", peliculas=None, busco_pelis=None)



#Buscar un director
@app.route("/buscaDirect", methods=["GET", "POST"])
def buscaDirect():
    if request.method == "POST":
        busco_direct= request.form ["busco_direct"].lower()
        with open ("peliculas.json", encoding="utf-8") as file:
            listaPelis= json.load(file)

        peliculasEncontradas= [pelicula for pelicula in listaPelis if busco_direct in pelicula ["director"].lower()]

        if not peliculasEncontradas:
            mensajeError = "No se encontraron directores que coincidan con la búsqueda."
            return render_template("error_directores.html", error=mensajeError)
    
        return render_template("buscaDirect.html", peliculas=peliculasEncontradas, query=busco_direct)
    
    return render_template("buscaDirect.html", peliculas=None, busco_direct=None)

        


#Endpoints
@app.route("/directores")
def directores():
    with open("peliculas.json", encoding="utf-8") as file:
        listaPelis= json.load(file)
    #Que no repita directores que aparecen mas de una vez
    directoresUnicos= list(set(pelicula["director"]for pelicula in listaPelis))
    return jsonify(directoresUnicos)

@app.route("/generos")
def generos():
    with open("peliculas.json", encoding="utf-8") as file:
        listaPelis= json.load(file)
    generosUnicos= list(set(generos["genero"]for generos in listaPelis))
    return jsonify(generosUnicos)

@app.route("/imagenes")
def imagenes():
    with open ("peliculas.json", encoding="utf-8") as file:
        listaPelis=json.load(file)

    peliculasImagen= [pelicula for pelicula in listaPelis if pelicula.get("imagen")]
    return jsonify(peliculasImagen)

@app.route("/listaPelis")
def listaPelis():
    with open("peliculas.json", encoding="utf-8") as file:
        lista_de_peliculas = json.load(file)
    return render_template("listaPelis.html", peliculas=lista_de_peliculas)




@app.route("/infoPelis")
def infoPelis():
    with open("peliculas.json", encoding="utf-8") as file:
        lista_de_peliculas = json.load(file)

    page = request.args.get("page", type=int, default=1)
    items_per_page = 5

    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page

    paginated_peliculas = lista_de_peliculas[start_idx:end_idx]

    total_pages = (len(lista_de_peliculas) + items_per_page - 1) // items_per_page

    return render_template("infoPelis.html", peliculas=paginated_peliculas, page=page, total_pages=total_pages)

@app.route("/error")
def error():
     return render_template("error.html")



#Si estamos en el archivo main de nuestra aplicacion, la ejecutamos
#Activamos la depuracion
if __name__== "__main__":
    app.run(debug=True)