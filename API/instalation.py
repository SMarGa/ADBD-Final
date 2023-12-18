from flask import Blueprint,jsonify , request

from db import  get_db_connection

instalation_bp = Blueprint('instalation', __name__)


@instalation_bp.route('/', methods=["GET"])
def getAllInstallations():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener todas las instalaciones
        cur.execute('SELECT * FROM Instalacion;')
        data = cur.fetchall()

        cur.close()
        conn.close()

        if( len(data) == 0):
            return jsonify("No se ha encontrado instalaciones"),404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

@instalation_bp.route('/<int:id>', methods=["GET"])
def getInstallationByID(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener todas las instalaciones
        cur.execute('SELECT * FROM Instalacion WHERE ID_I = %s;', (id,))
        data = cur.fetchall()

        cur.close()
        conn.close()


        if not data:
            return jsonify({"error": f"No se ha encontrado una celda con el ID {id}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
@instalation_bp.route('/', methods=["POST"])
def createInstallation():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron todos los campos necesarios
        if "Tipo" not in data or "Nombre" not in data or "Capacidad" not in data or "Estado_operativo" not in data:
            return jsonify({"error": "Todos los campos son requeridos"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar nueva instalación en la base de datos
        cur.execute('INSERT INTO Instalacion (Tipo, Nombre, Capacidad, Estado_operativo) VALUES (CAST(%s AS tipo_residuo[]), %s, %s, %s) RETURNING ID_I;',
                    (data["Tipo"], data["Nombre"], data["Capacidad"], data["Estado_operativo"]))

        # Obtener la fila resultante
        result = cur.fetchone()

        if result is not None:
            new_installation_id = result[0]
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"message": "Instalación creada exitosamente", "ID_I": new_installation_id}), 201
        else:
            cur.close()
            conn.close()
            return jsonify({"error": "No se ha devuelto ninguna fila después de la inserción"}), 500

    except Exception as err:
        print(err)
        return jsonify({"error": str(err)}), 500

    

@instalation_bp.route('/<int:id>', methods=["DELETE"])
def deleteInstallationById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la instalación existe antes de eliminarla
        cur.execute('SELECT * FROM Instalacion WHERE ID_I = %s;', (id,))
        data = cur.fetchall()

        if not data:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una instalación con el ID {id}"}), 404

        # Eliminar la instalación por su ID
        cur.execute('DELETE FROM Instalacion WHERE ID_I = %s;', (id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify(f"Instalación con ID {id} eliminada exitosamente")

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@instalation_bp.route('/<int:id>', methods=["PATCH"])
def updateInstallationById(id):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la instalación existe antes de intentar actualizarla
        cur.execute('SELECT * FROM Instalacion WHERE ID_I = %s;', (id,))
        existing_installation = cur.fetchall()

        if not existing_installation:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una instalación con el ID {id}"}), 404

        # Construir la consulta de actualización
        update_query = 'UPDATE Instalacion SET '
        values = []

        for key, value in data.items():
            # Realizar CAST si la columna es del tipo_residuo
            if key == 'Tipo':
                update_query += f'{key} = CAST(%s AS tipo_residuo[]), '
            else:
                update_query += f'{key} = %s, '

            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_I = %s;'
        values.append(id)

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Instalación con ID {id} actualizada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500
