import psycopg2

conn = psycopg2.connect("dbname=matcha user=vagrant");
cur = conn.cursor()
print conn
print cur
cur.execute("CREATE TABLE test2 (id serial PRIMARY KEY, num integer, data varchar);")
conn.commit()
print 'success'