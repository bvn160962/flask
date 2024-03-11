import psycopg2
from psycopg2.extras import NamedTupleCursor

PG_HOST = 'localhost'
PG_PORT = '54321'
PG_DATABASE = 'postgres'
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'


def get_entries():
    sql = "select *, to_char(date, 'YYYY-MM-DD') as d from ts_entries"
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(sql)
        entries = curs.fetchall()

    return entries

try:
    # connect to Data Base
    conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DATABASE, user=PG_USER, password=PG_PASSWORD)
    print(f'Connected to database: <{PG_DATABASE}> on <{PG_HOST}>')

except Exception as ex:
    print(f'Can`t establish connection to database {ex}: host={PG_HOST}, port={PG_PORT}, dbname={PG_DATABASE}, user={PG_USER}')

print(f'select: {get_entries()}')

