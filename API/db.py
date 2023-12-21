import psycopg2

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
        database="postgres",
        # user=os.environ['DB_USERNAME'],
		user="postgres",
		# password=os.environ['DB_PASSWORD']
        password="1234")
    return conn