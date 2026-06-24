import psycopg2

def seed():
    conn = psycopg2.connect(dbname="nc_plus_one", host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    drop_table(conn)
    create_table(conn)
    insert_data(conn)
    conn.commit()
    conn.close()
    
def drop_table(conn):
    conn = psycopg2.connect(dbname="nc_plus_one", host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    sql_drop_tables = "DROP TABLE IF EXISTS events, rsvps, users, venues CASCADE"
    cursor.execute(sql_drop_tables)
    cursor.close()


def create_table():
    cursor = conn.cursor()
    sql_create_table = "CREATE TABLE events, rsvps, users, venues"
    cursor.execute(sql_create_table)
    pass

def insert_data():
    conn = psycopg2.connect(dbname=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    pass

if __name__ == "__main__":
    seed()



