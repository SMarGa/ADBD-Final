from flask import Blueprint,jsonify , request

from db import  get_db_connection

machine_bp = Blueprint('machine', __name__)




@machine_bp.route('/', methods=["GET"])
def getMachineById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener máquinas
        cur.execute('SELECT * FROM Maquinas;')
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado ninguna máquina"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500


@machine_bp.route('/<int:id>', methods=["GET"])
def getMachineById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener máquina por ID
        cur.execute('SELECT * FROM Maquinas WHERE ID_M = %s;', (id,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una máquina con el ID_M {id}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@machine_bp.route('/<int:id>', methods=["PATCH"])
def updateMachineById(id):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la máquina existe antes de intentar actualizarla
        cur.execute('SELECT * FROM Maquinas WHERE ID_M = %s;', (id,))
        existing_machine = cur.fetchall()

        if not existing_machine:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una máquina con el ID_M {id}"}), 404
        
        new_id_i = data.get("ID_I", existing_machine[4])  # Si no se proporciona un nuevo ID_I, mantener el existente
        if new_id_i != existing_machine[4]:
            cur.execute('SELECT * FROM Instalacion WHERE ID_I = %s;', (new_id_i,))
            if not cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({"error": f"No se ha encontrado una instalación con el ID_I {new_id_i}"}), 404



        # Construir la consulta de actualización
        update_query = 'UPDATE Maquinas SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_M = %s;'
        values.append(id)

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Máquina con ID_M {id} actualizada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@machine_bp.route('/<int:id>', methods=["DELETE"])
def deleteMachineById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la máquina existe antes de intentar eliminarla
        cur.execute('SELECT * FROM Maquinas WHERE ID_M = %s;', (id,))
        existing_machine = cur.fetchall()

        if not existing_machine:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una máquina con el ID_M {id}"}), 404

        # Eliminar la máquina de la base de datos
        cur.execute('DELETE FROM Maquinas WHERE ID_M = %s;', (id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Máquina con ID_M {id} eliminada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500