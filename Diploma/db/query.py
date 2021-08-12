from db import setup


def insert_user(user_id: str) -> None:
    insert_user_query = f'''INSERT INTO users(id) VALUES(?);'''

    connection = setup.get_database_connection()
    connection.execute(insert_user_query, (user_id,))
    connection.commit()
    connection.close()


def insert_match(match_id: str, user_id: str) -> None:
    insert_match_query = f'''INSERT INTO matches(id, user_id) VALUES(?,?);'''

    connection = setup.get_database_connection()
    connection.execute(insert_match_query, (match_id, user_id))
    connection.commit()
    connection.close()


def get_user(user_id: str) -> list:
    get_user_query = '''SELECT id FROM users WHERE id = ?;'''

    connection = setup.get_database_connection()
    cursor = connection.cursor()

    cursor.execute(get_user_query, (user_id,))
    user = cursor.fetchall()

    cursor.close()
    connection.close()

    return user


def get_matches(user_id: str) -> list:
    get_matches_query = '''SELECT id FROM matches WHERE user_id = ?;'''

    connection = setup.get_database_connection()
    cursor = connection.cursor()

    cursor.execute(get_matches_query, (user_id,))
    matches = [match_id[0] for match_id in cursor.fetchall()]

    cursor.close()
    connection.close()

    return matches
