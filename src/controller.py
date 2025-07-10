from flask import Flask, request, jsonify
from data_handler import DataHandler
import atexit

from models.usuario import Usuario
from models.asignacion import Asignacion
from models.tarea import Tarea, StateError

app = Flask(__name__)
data_handler = DataHandler()

class TaskController:
    def __init__(self, data_handler):
        self.data_handler = data_handler

@app.route("/usuarios/mialias=<alias>", methods=["GET"])
def get_usuario_por_alias(alias):
    print(f"alias: {alias}!!!")
    return {}

@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    data: dict = request.get_json()
    if not data:
        return jsonify({"Error": "No se pudo encontrar el JSON"}), 400
    alias = data.get("alias")
    nombre = data.get("nombre")
    if not alias or not nombre:
        return jsonify({"Error": "Parametros faltantes, JSON invalido"}), 400
    usuario = Usuario(alias, nombre)
    data_handler.users.append(usuario)
    return data, 200

@app.route("/tasks", methods=["POST"])
def crear_task():
    data: dict = request.get_json()
    if not data:
        return jsonify({"Error": "No se pudo encontrar el JSON"}), 400
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    usuario_alias = data.get("usuario")
    rol = data.get("rol")
    if not nombre or not descripcion or not usuario_alias or not rol:
        return jsonify({"Error": "Parametros faltantes, JSON invalido"}), 400
    
    # get usuario
    usuario = data_handler.get_user_by_alias(usuario_alias)
    if usuario is None:
        return jsonify({"Error": "El usuario no existe!"}), 404

    # crear task
    id = data_handler.create_task_id()
    task = Tarea(id, nombre, descripcion)

    # crear asignacion
    asignacion = Asignacion(usuario, rol)
    task.adicionar_asignacion(asignacion)

    data_handler.tasks.append(task)
    return data, 200

@app.route("/tasks/<id>", methods=["POST"])
def task_cambiar_estado(id: str):
    data: dict = request.get_json()
    if not data:
        return jsonify({"Error": "No se pudo encontrar el JSON"}), 400
    estado = data.get("estado")
    if not estado:
        return jsonify({"Error": "Parametros faltantes, JSON invalido"}), 400

    task = data_handler.get_task_by_id(id)
    if task is None:
        return jsonify({"Error": "La tarea no existe!"}), 404
    
    try:
        task.cambiar_estado(estado)
        return data, 200 
    except TypeError:
        return jsonify({"Error": f"Parametro '{estado}' invalido"}), 400
    except StateError as e:
        return jsonify({"Error": str(e)}), 422

@app.route("/tasks/<id>/users", methods=["POST"])
def task_adicionar_o_remover_usuario(id: str):
    data: dict = request.get_json()
    if not data:
        return jsonify({"Error": "No se pudo encontrar el JSON"}), 400
    usuario_alias = data.get("usuario")
    rol = data.get("rol")
    accion = data.get("accion")
    if not usuario_alias or not rol or not accion:
        return jsonify({"Error": "Parametros faltantes, JSON invalido"}), 400

    task = data_handler.get_task_by_id(id)
    if task is None:
        return jsonify({"Error": "La tarea no existe!"}), 404

    if accion not in ["adicionar", "remover"]:
        return jsonify({"Error": f"Parametro '{accion}' invalido"}), 400
    if accion == "adicionar":
        usuario = data_handler.get_user_by_alias(usuario_alias)
        if usuario is None:
            return jsonify({"Error": "El usuario no existe!"}), 404
        asignacion = Asignacion(usuario, rol)
        task.adicionar_asignacion(asignacion)
        return data, 200
    else:
        task.remover_asignacion(usuario_alias)
        return data, 200

@app.route("/tasks/<id>/dependencies", methods=["POST"])
def task_adicionar_o_remover_dependencia(id: str):
    data: dict = request.get_json()
    if not data:
        return jsonify({"Error": "No se pudo encontrar el JSON"}), 400
    dependency_id = data.get("dependencytaskid")
    accion = data.get("accion")
    if not dependency_id or not accion:
        return jsonify({"Error": "Parametros faltantes, JSON invalido"}), 400

    task = data_handler.get_task_by_id(id)
    if task is None:
        return jsonify({"Error": "La tarea no existe!"}), 404

    if accion not in ["adicionar", "remover"]:
        return jsonify({"Error": f"Parametro '{accion}' invalido"}), 400
    if accion == "adicionar":
        dependency = data_handler.get_task_by_id(dependency_id)
        if dependency is None:
            return jsonify({"Error": "La dependencia no existe!"}), 404
        task.adicionar_dependencia(dependency)
        return data, 200
    else:
        task.remover_dependencia(dependency_id)
        return data, 200

atexit.register(data_handler.save_data)

if __name__ == '__main__':
    data_handler.load_data()
    app.run(debug=True)