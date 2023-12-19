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