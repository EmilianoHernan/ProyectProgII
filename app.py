from flask import Flask

app = Flask(__name__)

#Enrutamientos, Ruta raiz "/"
@app.route('/') 
def index():
    return "hola mundo!"

#Si estamos en el archivo main de nuestra aplicacion, la ejecutamos
#Activamos la depuracion
if __name__== "__main__":
    app.run(debug=True)