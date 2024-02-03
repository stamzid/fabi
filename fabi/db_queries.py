#!/usr/bin/env python3

from psycopg2 import sql


crawl_public_information_schema = sql.SQL("""SELECT table_name, column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_schema='public';""")
crawl_all_information_schema = sql.SQL("""SELECT table_name, column_name, data_type, is_nullable, column_default FROM information_schema.columns;""")

get_public_table_names = sql.SQL("""SELECT table_name from information_schema.tables WHERE table_schema = 'public';""")
get_all_table_names = sql.SQL("""SELECT table_name from information_schema.tables;""")

get_table_schema = sql.SQL("""SELECT table_name, column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position""")


public_queries = {
    "crawl": crawl_public_information_schema,
    "tables": get_public_table_names
}

all_queries = {
    "crawl": crawl_all_information_schema,
    "tables": get_all_table_names
}
