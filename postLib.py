import pandas as pd
import psycopg2 as pg
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 17:06:23 2021

@author: SUNGJOON
"""

class PostgresDataClass():
    def __init__(self, host, database, user, password):
        self.host = host
        self.user = user
        self.database = database
        self.password = password
        self.type_dict = {'timestamp without time zone': 'timestamp[]',
                          'character varying': 'text[]',
                          'integer': 'int4[]',
                          'date': 'date[]',
                          'real': 'real[]',
                          'bigint': 'bigint[]',
                          'double precision': 'double precision[]',
                          'text': 'text[]'}

    def connect(self):
        conn = pg.connect(host=self.host,
                          database=self.database,
                          user=self.user,
                          password=self.password)
        return conn

    def get_cursor(self, conn):
        cur = conn.cursor()
        return cur

    def get_table_schema(self, address, db_name, schema_name, table_name):
        conn = pg.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cur = conn.cursor()
        cur.execute("""select create_sql from table_information.table_schema
                        where address=%s
                        and db_name =%s
                        and schema_name =%s
                        and table_name =%s""", (address, db_name, schema_name, table_name))
        result = cur.fetchall()
        cur.close()
        conn.close()

        return result[0][0]

    ##select return list
    def select_list(self, sql, param=()):
        with self.connect() as conn:
            with self.get_cursor(conn) as cur:
                cur.execute(sql, param)
                return cur.fetchall()

    ##select return dataframe
    def select_dataframe(self, sql, param=()):
        with self.connect() as conn:
            with self.get_cursor(conn) as cur:
                cur.execute(sql, param)
                colnames = [desc[0] for desc in cur.description]
                df = pd.DataFrame(cur.fetchall())
                df.columns = colnames
                return df

    ##query execute
    def execute(self, sql, param=()):
        with self.connect() as conn:
            with self.get_cursor(conn) as cur:
                try:
                    cur.execute(sql, param)
                    conn.commit()

                except Exception as e:
                    print('%s %s' % (e.__class.__name__, str(e)))

    def set_source_list(self, data):
        self.source_list = data

    def insert_list(self, data, schema_table_name, size=100000):
        it = iter(data)
        win = []
        length = len(data)
        record_sum = 0
        with self.connect() as conn:
            with self.get_cursor(conn) as cur:
                while True:
                    try:
                        for e in range(0, size):
                            win.append(next(it))

                    except Exception:
                        None

                    if len(win) == 0:
                        break
                    record_sum += len(win)
                    print("%5s:%-20s [%s/%s]" % ('Insert', schema_table_name, record_sum, length))

                    #                    with timer(name="duraction"):
                    self.set_source_list(win)
                    self.migration(cur, schema_table_name)
                    win = []
                    conn.commit()

    def migration(self, cur, schema_table_name):
        schema, table_name = schema_table_name.split('.')
        table_info = self.select_dataframe(""" SELECT column_name, ordinal_position,is_nullable, data_type
                                               FROM information_schema.columns WHERE table_schema = lower(%s)
                                               AND table_name = lower(%s) order by ordinal_position""",
                                           (schema, table_name))
        index = 0
        for column_name in table_info['column_name']:
            exec(column_name + '=[x[{index}] for x in self.source_list]'.format(index=index))

            index += 1
        columns = ','.join(table_info['column_name'])

        unnest_columns = []
        for i in range(0, len(table_info)):
            unnest_columns.append(
                'unnest(%({})s::{})'.format(table_info['column_name'][i], self.type_dict[table_info['data_type'][i]]))

        insert_sql = """INSERT INTO {schema_table_name}({columns}) SELECT {unnest_columns} ON CONFLICT DO NOTHING""".format(
            schema_table_name=schema_table_name, columns=columns, unnest_columns=','.join(unnest_columns))

        params = locals()
        cur.execute(insert_sql, params)


