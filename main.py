from flask import Flask, request, session, jsonify, redirect, url_for, render_template

import controllers.index as indx

import os

app = Flask(__name__, template_folder='templates', static_url_path="/static")
app.secret_key = os.getenv("KEY")

@app.route('/', methods=["GET", "POST"])
def index():
    return indx.inicio(request)

@app.route('/salir', methods=["GET"])
def salir():
    return indx.salir()

@app.route('/principal', methods=["GET", "POST"])
def principal():
    productos = obtener_productos()  
    return render_template('principal.html', productos=productos)

@app.route('/usuarios/<int:id>', methods=["GET"])
def usuario(id):
    return indx.ver_usuario(id)

@app.route('/save_usuario', methods=["POST"])
def save_usuario():
    return indx.save_user(request)

@app.route('/edit_usuario', methods=["POST"])
def edit_usuario():
    return indx.edit_user(request)

@app.route('/del_usuario', methods=["POST"])
def del_usuario():
    return indx.del_user(request)

@app.route('/carrito', methods=["GET"])
def ver_carrito():
    return indx.ver_carrito()

@app.route('/agregar_al_carrito/<int:producto_id>', methods=["POST"])
def agregar_al_carrito(producto_id):
    return indx.agregar_al_carrito(producto_id)

@app.route('/some_route')
def some_route():
    val_session(session)
    return jsonify({"message": "Sesión válida"})

@app.route('/productos', methods=["GET"])
def mostrar_productos():
    productos = obtener_productos()  # Asegúrate de que esta función retorne una lista de productos
    return render_template('productos.html', productos=productos)

if __name__ == '__main__':
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"), debug=True)