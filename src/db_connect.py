import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="edi_clinicaltrials",
        user="ediuser",
        password="12345"
    )
    return conn

if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cur.fetchall()
    print("Tables in the database:", tables)
    cur.close()
    conn.close()
