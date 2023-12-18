from flask import Blueprint,jsonify , request

from db import  get_db_connection

cell_bp = Blueprint('cell', __name__)
# 
# GET - Obtener todas las celdas
@cell_bp.route('/', methods=["GET"])
def getAllCells():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener todas las celdas
        cur.execute('SELECT * FROM Celda;')
        data = cur.fetchall()

        cur.close()
        conn.close()

        if( len(data) == 0):
            return jsonify("No se ha encontrado celdas"),404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@cell_bp.route('/<int:id>', methods=["GET"])
def getCellByID(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener todas las celdas
        cur.execute('SELECT * FROM Celda WHERE ID_C = %s;', (id,))
        data = cur.fetchall()

        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una celda con el ID {id}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

# POST - Crear una nueva celda
@cell_bp.route('/', methods=["POST"])
def createCell():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron todos los campos necesarios
        if "Nombre" not in data or "Capacidad" not in data or "Estado" not in data:
            return jsonify({"error": "Todos los campos son requeridos"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar nueva celda en la base de datos
        cur.execute('INSERT INTO Celda (Nombre, Capacidad, Estado) VALUES (%s, %s, %s) RETURNING ID_C;',
                    (data["Nombre"], data["Capacidad"], data["Estado"]))
        new_cell_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Celda creada exitosamente", "ID_C": new_cell_id}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500

# DELETE - Eliminar una celda por ID
@cell_bp.route('/<int:id>', methods=["DELETE"])
def deleteCellById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la celda existe antes de eliminarla
        cur.execute('SELECT * FROM Celda WHERE ID_C = %s;', (id,))
        data = cur.fetchall()

        if not data:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una celda con el ID {id}"}), 404

        # Eliminar la celda por su ID
        cur.execute('DELETE FROM Celda WHERE ID_C = %s;', (id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify(f"Celda con ID {id} eliminada exitosamente")

    except Exception as err:
        return jsonify({"error": str(err)}), 500

# PATCH - Actualizar información de una celda por ID
@cell_bp.route('/<int:id>', methods=["PATCH"])
def updateCellById(id):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la celda existe antes de intentar actualizarla
        cur.execute('SELECT * FROM Celda WHERE ID_C = %s;', (id,))
        existing_cell = cur.fetchall()

        if not existing_cell:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una celda con el ID {id}"}), 404

        # Construir la consulta de actualización
        update_query = 'UPDATE Celda SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_C = %s;'
        values.append(id)

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Celda con ID {id} actualizada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500