import psycopg2

def sql_select(db_query, params=[]):
    conn = psycopg2.connect('dbname=bubs')
    cur = conn.cursor()

    cur.execute(db_query,params)
    results = cur.fetchall()

    cur.close()
    conn.close()
    
    return results