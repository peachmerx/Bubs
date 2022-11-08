import os

DB_URL = os.environ.get('DATABASE_URL', 'dbname=bubs')

import psycopg2

def sql_select(db_query, params=[]):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute(db_query,params)
    results = cur.fetchall()

    cur.close()
    conn.close()
    
    return results