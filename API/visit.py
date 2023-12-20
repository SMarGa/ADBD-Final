from flask import Blueprint,jsonify , request

from db import  get_db_connection

visit_bp = Blueprint('visit', __name__)


@visit_bp.route('/', methods=["GET"])
def getVisits():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener visita por ID
        cur.execute('SELECT * FROM Visita;')
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado ningnuna visita"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@visit_bp.route('/<int:id>', methods=["GET"])
def getVisitById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener visita por ID
        cur.execute('SELECT * FROM Visita WHERE ID_Visit = %s;', (id,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        if not data:
            return jsonify({"error": f"No se ha encontrado una visita con el ID_Visit {id}"}), 404

        return jsonify(data)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@visit_bp.route('/', methods=["POST"])
def createVisit():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron todos los campos necesarios
        if "Duracion" not in data or "N_visitantes" not in data:
            return jsonify({"error": "La duración y el número de visitantes son campos requeridos"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar nueva visita en la base de datos
        cur.execute('INSERT INTO Visita (Duracion, N_visitantes) VALUES (%s, %s) RETURNING ID_Visit;',
                    (data["Duracion"], data["N_visitantes"]))
        new_visit_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Visita creada exitosamente", "ID_Visit": new_visit_id}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@visit_bp.route('/<int:id>', methods=["PATCH"])
def updateVisitById(id):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la visita existe antes de intentar actualizarla
        cur.execute('SELECT * FROM Visita WHERE ID_Visit = %s;', (id,))
        existing_visit = cur.fetchone()

        if not existing_visit:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una visita con el ID_Visit {id}"}), 404

        # Construir la consulta de actualización
        update_query = 'UPDATE Visita SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_Visit = %s;'
        values.append(id)

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Visita con ID_Visit {id} actualizada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@visit_bp.route('/<int:id>', methods=["DELETE"])
def deleteVisitById(id):
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si la visita existe antes de intentar eliminarla
        cur.execute('SELECT * FROM Visita WHERE ID_Visit = %s;', (id,))
        existing_visit = cur.fetchone()

        if not existing_visit:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado una visita con el ID_Visit {id}"}), 404

        # Eliminar la visita de la base de datos
        cur.execute('DELETE FROM Visita WHERE ID_Visit = %s;', (id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Visita con ID_Visit {id} eliminada exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500