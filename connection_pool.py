# Loading create_connection() over and over --> expensive
# Later need connection pooling process

import os
from contextlib import contextmanager
# import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

# Creating new PostgreSQL connections can be an expensive operation.
# psycopg2 offers a few pure Python classes implementing connection pooling directly in the client application.

# def create_connection():
#     return psycopg2.connect(os.environ.DATABASE_URI)
import Finaldatabase

DATABASE_PROMPT = "Enter the DATABASE_URL value or leave empty to load from .env file: "

database_uri = input(DATABASE_PROMPT)
if not database_uri:
    load_dotenv()
    database_uri = os.environ["DATABASE_URI"]

# Create a single-threaded pool
pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_uri)  # dsn pass onto psycopg2.connect({**kwargs})


@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)
