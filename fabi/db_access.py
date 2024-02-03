#!/usr/bin/env python3

import os
import psycopg2
import traceback
from psycopg2 import pool
from psycopg2.extras import DictCursor

from contextlib import contextmanager
from fabi.utils.logging_utils import service_logger


## Since this information is public, adding the credentials on repo, otherwise we will put them in secure environment variables
DB_HOST = os.getenv("DB_HOST", "interview-sandbox.c7myq48g2e87.us-east-1.rds.amazonaws.com")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_USER = os.getenv("DB_USER", "interviewee")
DB_PASS = os.getenv("DB_PASS", "fabi.aiiscool")
DB_NAME = os.getenv("DB_NAME", "toy_example")

connection_pool = None

def format_list_query(query: str, records: list):
    formatted_query = query.format(
        sql.SQL(', ').join(sql.Literal(str(item)) for item in records)
    )

    return formatted_query


def get_connection_pool():
    global connection_pool
    if connection_pool is None:
        connection_pool = pool.ThreadedConnectionPool(
            minconn=int(os.getenv("MINIMUM_DB_CONNECTIONS", 16)),
            maxconn=int(os.getenv("MAXIMUM_DB_CONNECTIONS", 256)),
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
    return connection_pool


@contextmanager
def get_db_connection():
    connection = get_connection_pool().getconn()
    try:
        yield connection
    finally:
        get_connection_pool().putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            yield cursor
            if commit:
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()


def execute_read_query(query, record):
    count = 0
    data = []
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, record)
            count = cursor.rowcount
            data = [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        service_logger.error(e)
    return count, data


def execute_read_without_condition(query):
    count = 0
    data = []
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            count = cursor.rowcount
            data = [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        traceback.print_exc()
        service_logger.error(e)
    return count, data


def execute_read_query_with_list(query_template, params):
    """
    Executes a read query with a list of parameters for an IN clause.

    :param query_template: SQL query template with a placeholder for list parameters.
                           Example: "SELECT * FROM table WHERE column IN ({})"
    :param params: List of parameters to be included in the IN clause.
    :return: Tuple of (row count, list of data dictionaries)
    """
    count = 0
    data = []
    try:
        with get_db_cursor() as cursor:
            literals = [sql.Literal(param) for param in params]
            formatted_query = sql.SQL(query_template).format(sql.SQL(', ').join(literals))
            cursor.execute(formatted_query)
            count = cursor.rowcount
            data = [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        service_logger.error(e)
        traceback.print_exc()

    return count, data
