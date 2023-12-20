from flask import Blueprint,jsonify , request

from db import  get_db_connection

employee_bp = Blueprint('employee', __name__)
# 

@employee_bp.route('/', methods = ["Get"])
def getEmp():
    try:
        # Estableciendo conección con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        # Obetener técnicos por id
        cur.execute('SELECT * FROM Empleado;')
        data = cur.fetchall()
        cur.close()
        conn.close()
        if( len(data) == 0):
            return jsonify("No se ha encontrado empleados"),404
        
        return jsonify(data)
    
    except Exception as err:
        return jsonify({"error" : str(err)}), 500 

@employee_bp.route('/', methods=["POST"])
def createEmployee():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Extraer datos del JSON
        nombre = data.get('nombre')
        n_telf = data.get('n_telf')
        turno = data.get('turno')
        ocupacion = data.get('ocupacion')

        # Validar que se proporcionaron todos los campos necesarios
        if not nombre or not n_telf or not turno or not ocupacion:
            return jsonify({"error": "Todos los campos son requeridos"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar nuevo empleado en la base de datos
        cur.execute('INSERT INTO Empleado (Nombre, N_telf, Turno, Ocupacion) VALUES (%s, %s, %s, %s) RETURNING ID_Emp;',
                    (nombre, n_telf, turno, ocupacion))
        new_employee_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Empleado creado exitosamente", "ID_Emp": new_employee_id}), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500   

@employee_bp.route('/<int:id>', methods=["PATCH"])
def updateEmployee(id):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionaron datos para actualizar
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si el empleado existe antes de intentar actualizarlo
        cur.execute('SELECT * FROM Empleado WHERE ID_Emp = %s;', (id,))
        existing_employee = cur.fetchall()

        if not existing_employee:
            cur.close()
            conn.close()
            return jsonify({"error": f"No se ha encontrado un empleado con el ID {id}"}), 404

        # Construir la consulta de actualización
        update_query = 'UPDATE Empleado SET '
        values = []

        for key, value in data.items():
            update_query += f'{key} = %s, '
            values.append(value)

        # Eliminar la coma extra al final y agregar la condición WHERE
        update_query = update_query.rstrip(', ') + f' WHERE ID_Emp = %s;'
        values.append(id)

        # Ejecutar la consulta de actualización
        cur.execute(update_query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"Empleado con ID {id} actualizado exitosamente"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500 


@employee_bp.route('/tecnicos', methods = ["Get"])
def getEmpTec():
    try:
        # Estableciendo conección con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        # Obetener técnicos por id
        cur.execute("SELECT * FROM Empleado WHERE Ocupacion = 'tecnico';")
        data = cur.fetchall()
        cur.close()
        conn.close()
        if( len(data) == 0):
            return jsonify("No se ha encontrado tecnicos"),404
        
        return jsonify(data)
    
    except Exception as err:
        return jsonify({"error" : str(err)}), 500 
    
@employee_bp.route('/guias', methods = ["Get"])
def getEmpGuide():
    try:
        # Estableciendo conección con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        # Obetener técnicos por id
        cur.execute("SELECT * FROM Empleado WHERE Ocupacion = 'guia';")
        data = cur.fetchall()
        cur.close()
        conn.close()
        if( len(data) == 0):
            return jsonify("No se ha encontrado guias"),404
        return jsonify(data)
    
    except Exception as err:
        return jsonify({"error" : str(err)}), 500 
    
@employee_bp.route('/transportistas', methods = ["Get"])
def getEmpTrans():
    try:
        # Estableciendo conección con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        # Obetener técnicos por id
        cur.execute("SELECT * FROM Empleado WHERE Ocupacion = 'transportista';")
        data = cur.fetchall()
        cur.close()
        conn.close()
        if( len(data) == 0):
            return jsonify("No se ha encontrado transportistas"),404
        return jsonify(data)
    
    except Exception as err:
        return jsonify({"error" : str(err)}), 500 



@employee_bp.route('/<int:id>', methods = ["Get"])
def getEmpById(id):
    try:
        # Estableciendo conección con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        # Obetener técnicos por id
        cur.execute('SELECT * FROM Empleado WHERE ID_Emp = %s;',(id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        if( len(data) == 0):
            return jsonify("No se ha encontrado un empleado con el id proporcionado"),404
        return jsonify(data)
    
    except Exception as err:
        return jsonify({"error" : str(err)}), 500 
    
@employee_bp.route('/<int:id>', methods=["DELETE"])
def deleteEmpById(id):
    try:
        # Estableciendo conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si el técnico existe antes de eliminarlo
        cur.execute('SELECT * FROM Empleado WHERE ID_Emp = %s;', (id,))
        data = cur.fetchall()

        if len(data) == 0:
            cur.close()
            conn.close()    
            return jsonify("No se ha encontrado un empleado con el id proporcionado"), 404

        # Eliminar el técnico por su ID
        cur.execute('DELETE FROM Empleado WHERE ID_Emp = %s;', (id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify(f"Empleado con ID {id} eliminado exitosamente")

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
  
