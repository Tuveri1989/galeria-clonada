from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

DOCUMENTOS = ["doc", "docx"]

EXTENSIONES = ["png", "jpg", "jpeg"]
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './static/archivos'

def archivo_permitido(nombre):
    return "." in nombre and nombre.rsplit(".", 1)[1] in EXTENSIONES
    
@app.route("/")
@app.route("/upload", methods=["POST"])
def uploader():
    texto = "Seleccione una imagen para cargar"
    if request.method == 'POST':
        f  = request.files['archivo']
        if f.filename == "":
            texto = "Hay que seleccionar un archivo."
        else:
            if archivo_permitido(f.filename):
                archivo = secure_filename(f.filename)
                f.save(os.path.join(app.config["UPLOAD_FOLDER"], archivo))
                texto = "Imagen cargada."
            else:
                texto = "No ha seleccionado un archivo de imagen."
    archivos = []
    for archivo in os.scandir(app.config["UPLOAD_FOLDER"]):
        archivos.append(archivo.name)
    return render_template("formulario.html", lista=archivos, t=texto)

@app.route("/foto/<nombre>")
def cargafoto(nombre):
    for archivo in os.scandir(app.config["UPLOAD_FOLDER"]):
        if archivo.name == nombre:
            return send_from_directory(app.config["UPLOAD_FOLDER"], nombre)
    return "<h1>Lo siento, la imagen " + nombre + \
        " no se ha encontrado.</h1><br><a href='/'>Volver</a>"
        
        
@app.errorhandler(404)
def ruta_no_valida(e):
    return "<h3>Lo siento, no encuentro la página.<br>" \
        "Puede <a href='/'>regresar</a> a la página principal</h3>"

if __name__ == '__main__':
    app.run(debug=True)