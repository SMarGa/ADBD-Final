import os
import psycopg2

from flask import Flask , request, jsonify

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
        database="myhome",
        # user=os.environ['DB_USERNAME'],
		user="postgres",
		# password=os.environ['DB_PASSWORD']
        password="1234")
    return conn

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return "This is a API for accesing data from the database of CAT!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)