from contextlib import contextmanager
from typing import List, Tuple
# from psycopg2.extras import execute_values
# from models.test_poll import PollTest
# rom models.test_option import OptionTest

Poll = Tuple[int, str, str]
Option = Tuple[int, str, int]
Vote = Tuple[str, int]
PollResults = Tuple[int, str, int, float]

CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""
CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options
(id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER);"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, option_id INTEGER);"""

INSERT_POLL_RETURN_ID = """INSERT INTO polls 
(title, owner_username) VALUES (%s, %s) RETURNING id;"""
SELECT_ALL_POLLS = "SELECT * FROM polls;"
SELECT_POLL = "SELECT * FROM polls WHERE id=%s;"
SELECT_LATEST_POLL = """SELECT * FROM polls 
WHERE polls.id = (SELECT id FROM polls ORDER BY id DESC LIMIT 1);"""
SELECT_POLL_OPTIONS = "SELECT * FROM options WHERE poll_id = %s;"

INSERT_OPTION = "INSERT INTO options (option_text, poll_id) VALUES %s RETURNING id;"
SELECT_OPTION = "SELECT * FROM options WHERE id = %s;"

SELECT_VOTES_FOR_OPTION = "SELECT * FROM votes WHERE option_id = %s"
INSERT_VOTE = "INSERT INTO votes (username, option_id) VALUES (%s, %s);"


# SELECT_RANDOM_VOTE = "SELECT * FROM votes WHERE option_id=%s ORDER BY RANDOM() LIMIT 1;"

# GET_POLL_VOTE_RESULTS = """
# SELECT
#     options.id,
#     options.option_text,
#     COUNT(votes.option_id) AS count,
#     COUNT(votes.option_id)/SUM(COUNT(votes.option_id)) OVER() * 100.0 AS percentage
# FROM options
# LEFT JOIN votes ON votes.option_id = options.id
# WHERE options.poll_id = %s
# GROUP BY options.id
# """  # window function <- after WHERE, GROUP BY, AGGREGATION


# -- check / create tables when connected to database --

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_POLLS)
        cursor.execute(CREATE_OPTIONS)
        cursor.execute(CREATE_VOTES)


# -- polls --


def create_poll(connection, title, owner):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_POLL_RETURN_ID, (title, owner))
        poll_id = cursor.fetchone()[0]  # first col of first row
        return poll_id


def get_polls(connection) -> List[Poll]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_POLLS)
        return cursor.fetchall()


def get_poll(connection, poll_id) -> Poll:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL, (poll_id,))
        return cursor.fetchone()


def get_latest_poll(connection) -> Poll:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_LATEST_POLL)
        return cursor.fetchone()


def get_poll_options(connection, poll_id) -> Option:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL_OPTIONS, (poll_id,))
        return cursor.fetchall()


# -- options --


def add_option(connection, option_text: str, poll_id: int) -> Option:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_OPTION, (option_text, poll_id))
        return cursor.fetchone()


def get_option(connection, option_id: int) -> Option:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_OPTION, (option_id,))
        return cursor.fetchone()


# -- votes --

def get_votes_for_option(connection, option_id: int) -> List[Vote]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_VOTES_FOR_OPTION, (option_id,))
        return cursor.fetchall()


def add_poll_vote(connection, username: str, option_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_VOTE, (username, option_id))

# def get_random_poll_vote(connection, option_id: int) -> Vote:
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_RANDOM_VOTE, (option_id, ))
#             return cursor.fetchone()
