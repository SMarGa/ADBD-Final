from flask import Blueprint,jsonify , request

from db import  get_db_connection

route_bp = Blueprint('route', __name__)

@route_bp.route('/', methods=["GET"])
def getRoutes():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener ruta por ID
        cur.execute('SELECT * FROM Ruta;')
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado ninguna ruta"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500


@route_bp.route('/<int:id>', methods=["GET"])
def getRouteById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener ruta por ID
        cur.execute('SELECT * FROM Ruta WHERE ID_Ruta = %s;', (id,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una ruta con el ID {id}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500


@route_bp.route('/', methods=["POST"])
def createRoute():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron todos los campos necesarios
        if "Duracion" not in data or "N_paradas" not in data:
            return jsonify({"error": "Todos los campos son requeridos"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar nueva ruta en la base de datos
        cur.execute('INSERT INTO Ruta (Duracion, N_paradas) VALUES (%s, %s) RETURNING ID_Ruta;',
                    (data["Duracion"], data["N_paradas"]))
        new_route_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Ruta creada exitosamente", "ID_Ruta": new_route_id}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@route_bp.route('/<int:id>', methods=["PATCH"])
def updateRouteById(id):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la ruta existe antes de intentar actualizarla
        cur.execute('SELECT * FROM Ruta WHERE ID_Ruta = %s;', (id,))
        existing_route = cur.fetchall()

        if not existing_route:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una ruta con el ID {id}"}), 404

        # Construir la consulta de actualización
        update_query = 'UPDATE Ruta SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_Ruta = %s;'
        values.append(id)

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Ruta con ID {id} actualizada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@route_bp.route('/<int:id>', methods=["DELETE"])
def deleteRouteById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la ruta existe antes de intentar eliminarla
        cur.execute('SELECT * FROM Ruta WHERE ID_Ruta = %s;', (id,))
        existing_route = cur.fetchall()

        if not existing_route:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una ruta con el ID {id}"}), 404

        # Eliminar la ruta de la base de datos
        cur.execute('DELETE FROM Ruta WHERE ID_Ruta = %s;', (id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Ruta con ID {id} eliminada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500