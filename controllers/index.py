from flask import render_template, jsonify, session, request
from datetime import datetime
from controllers.ctl_validaciones import Validaciones as val
from bson.objectid import ObjectId
from database.mongodb import MongoDb
import controllers.ctl_history as hist

db = MongoDb().db()

meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
         "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
semanas = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]

# Función de inicio, se mostrará la página principal con la fecha actual
def inicio():
    fecha = datetime.now()
    arreglo = {"dia": fecha.day, "anio": fecha.year,
               "mes": meses[fecha.month-1], "semana": semanas[fecha.weekday()]}
    return render_template('/views/index.html', fecha=arreglo)

# Función para eliminar una foto del sistema, solo si el usuario está autenticado
def del_foto(request):
    if request.method == 'POST':
        try:
            # Verificamos si la sesión es válida (usuario autenticado)
            if val.validar_session(session):

                # Extraemos los parámetros necesarios desde la solicitud
                id = val.val_vacio("id", "", request)
                tipo = val.val_vacio("tipo", "", request)

                # Buscamos si el recurso (tipo de producto) existe en la base de datos
                existe = db[tipo].find_one({"_id": ObjectId(id)})

                if existe:
                    if existe["url_foto"] != "":
                        # Si existe la foto, la eliminamos del sistema de archivos
                        path = "static/" + tipo + "/" + existe["url_foto"]
                        val.del_archivo(path)

                        # Actualizamos el registro en la base de datos, quitando la URL de la foto
                        db[tipo].update_one({"_id": ObjectId(id)}, {"$set": {"url_foto": ""}})

                        return jsonify({"message": "Imagen Eliminada Correctamente"}), 200
                    else:
                        return jsonify({"message": "No hay imagen asociada a este recurso"}), 404
                else:
                    return jsonify({"message": "El Recurso No existe"}), 404

            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            # En caso de error, se guarda el historial de la acción con detalles
            hist.guardar_historial(
                "ERROR", "ELIMINAR", 'Error al eliminar la imagen de tipo "' + tipo + '" con ID "' + id + '" - "' + str(e) + '"')
            return jsonify({"message": "Error al eliminar la imagen"}), 500
    else:
        return jsonify({"message": "Petición Incorrecta"}), 405
