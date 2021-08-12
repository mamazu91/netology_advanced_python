import sqlite3

DB_NAME = "mamazinder.db"


def get_database_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_NAME)

    return connection


def create_users_table() -> None:
    create_table_query = '''CREATE TABLE IF NOT EXISTS users(id VARCHAR PRIMARY KEY);'''

    connection = get_database_connection()
    connection.execute(create_table_query)
    connection.close()


def create_matches_table() -> None:
    create_table_query = '''CREATE TABLE IF NOT EXISTS matches(
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
    );
    '''

    connection = get_database_connection()
    connection.execute(create_table_query)
    connection.close()
