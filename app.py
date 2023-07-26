from flask import Flask, render_template

app = Flask(__name__)

#Enrutamientos, Ruta raiz "/"
@app.route('/') 
def index():
    return render_template('index.html')

#Si estamos en el archivo main de nuestra aplicacion, la ejecutamos
#Activamos la depuracion
if __name__== "__main__":
    app.run(debug=True)