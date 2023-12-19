from flask import Blueprint,jsonify , request

from db import  get_db_connection

waste_bp = Blueprint('waste', __name__)


@waste_bp.route('/', methods=["GET"])
def getWaste():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener residuos
        cur.execute('SELECT * FROM Residuo;')
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado ningun residuo" }), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500



@waste_bp.route('/<int:id>', methods=["GET"])
def getWasteById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener residuo por ID
        cur.execute('SELECT * FROM Residuo WHERE ID_R = %s;', (id,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado un residuo con el ID {id}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500


@waste_bp.route('/', methods=["POST"])
def createWaste():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron todos los campos necesarios
        if "Tipo" not in data or "Cantidad" not in data or "Origen" not in data or "Fecha_de_recepcion" not in data:
            return jsonify({"error": "Todos los campos son requeridos"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si ID_C existe
        id_c = data.get("ID_C")
        if id_c is not None:
            cur.execute('SELECT * FROM Celda WHERE ID_C = %s;', (id_c,))
            if not cur.fetchone():
                conn.close()
                return jsonify({"error": f"No se ha encontrado una celda con el ID_C {id_c}"}), 404

        # Verificar si ID_I existe
        id_i = data.get("ID_I")
        if id_i is not None:
            cur.execute('SELECT * FROM Instalacion WHERE ID_I = %s;', (id_i,))
            if not cur.fetchone():
                conn.close()
                return jsonify({"error": f"No se ha encontrado una instalación con el ID_I {id_i}"}), 404

        # Insertar nuevo residuo en la base de datos
        cur.execute('INSERT INTO Residuo (Tipo, Cantidad, Origen, Fecha_de_recepcion, ID_C, ID_I) VALUES (%s, %s, %s, %s, %s, %s) RETURNING ID_R;',
                    (data["Tipo"], data["Cantidad"], data["Origen"], data["Fecha_de_recepcion"], id_c, id_i))
        new_waste_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Residuo creado exitosamente", "ID_R": new_waste_id}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    


@waste_bp.route('/<int:id>', methods=["DELETE"])
def deleteWasteById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si el residuo existe antes de intentar eliminarlo
        cur.execute('SELECT * FROM Residuo WHERE ID_R = %s;', (id,))
        existing_waste = cur.fetchall()

        if not existing_waste:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado un residuo con el ID {id}"}), 404

        # Eliminar el residuo de la base de datos
        cur.execute('DELETE FROM Residuo WHERE ID_R = %s;', (id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Residuo con ID {id} eliminado exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@waste_bp.route('/<int:id>', methods=["PATCH"])
def updateWasteById(id):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si el residuo existe antes de intentar actualizarlo
        cur.execute('SELECT * FROM Residuo WHERE ID_R = %s;', (id,))
        existing_waste = cur.fetchall()

        if not existing_waste:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado un residuo con el ID {id}"}), 404
        
        
        # Verificar si se está cambiando el ID_C y si el nuevo ID_C existe
        new_id_c = data.get("ID_C", existing_waste[5])  # Si no se proporciona un nuevo ID_C, mantener el existente
        if new_id_c != existing_waste[5]:
            cur.execute('SELECT * FROM Celda WHERE ID_C = %s;', (new_id_c,))
            if not cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({"error": f"No se ha encontrado una celda con el ID_C {new_id_c}"}), 404

        # Verificar si se está cambiando el ID_I y si el nuevo ID_I existe
        new_id_i = data.get("ID_I", existing_waste[6])  # Si no se proporciona un nuevo ID_I, mantener el existente
        if new_id_i != existing_waste[6]:
            cur.execute('SELECT * FROM Instalacion WHERE ID_I = %s;', (new_id_i,))
            if not cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({"error": f"No se ha encontrado una instalación con el ID_I {new_id_i}"}), 404

      

        # Construir la consulta de actualización
        update_query = 'UPDATE Residuo SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_R = %s;'
        values.append(id)

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Residuo con ID {id} actualizado exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500