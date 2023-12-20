

from flask import Flask , request, jsonify

from employee import employee_bp 
from cell import cell_bp
from instalation import instalation_bp
from route import route_bp
from machine import machine_bp
from waste import waste_bp
from visit import visit_bp
from vehicle import vehicle_bp

from visit_vehicle import visit_vehicle_bp
from guide_visit import guide_visit_bp
from tech_instalation import tec_inst_bp
from trans_vehicle import trans_vehicle_bp

from public import public_bp

from db import  get_db_connection


app = Flask(__name__)

# Las siguientes rutas estan ordenadas de manera piramidal donde 
# los miembros pertenecientes a escalones superiores tienen acceso
# a los inferiores de manera que los cargos directivos también pueden
# acceder a las rutas destinadas tanto a empleados como clientes.

# Rutas destinadas a los cargos superiores del CAT

app.register_blueprint(employee_bp, url_prefix='/empleado')
app.register_blueprint(cell_bp, url_prefix='/celda')
app.register_blueprint(instalation_bp, url_prefix='/instalacion')

# Rutas destinadas a empleados

app.register_blueprint(route_bp, url_prefix='/ruta')
app.register_blueprint(machine_bp, url_prefix='/maquina')

app.register_blueprint(waste_bp, url_prefix='/residuo')

app.register_blueprint(vehicle_bp, url_prefix='/vehiculos')
app.register_blueprint(visit_bp, url_prefix='/visita')
app.register_blueprint(visit_vehicle_bp, url_prefix='/visita_vehiculo')
app.register_blueprint(guide_visit_bp, url_prefix='/guia_visita')
app.register_blueprint(tec_inst_bp, url_prefix='/tec_inst')
app.register_blueprint(trans_vehicle_bp, url_prefix='/trans_veh')

# Rutas destinadas a clientes 

app.register_blueprint(public_bp, url_prefix='/public')



@app.route('/', methods=['GET'])
def welcome():
  
    return jsonify("This is a api for the accesing data from the databases of the CAT!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)