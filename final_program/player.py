import dbconnection as db


def is_player_existed(player_name):
    sql = "SELECT id, name FROM player WHERE name = %s"
    values = (player_name,)

    cursor = db.db_connection()
    cursor.execute(sql, values)
    if cursor.rowcount > 0:
        return True

    return False


def get_player_info(player_name):
    sql = "SELECT id, name FROM player WHERE name = %s"
    values = (player_name,)

    cursor = db.db_connection()
    cursor.execute(sql, values)

    player_info = cursor.fetchone()

    if player_info:
        return player_info
    else:
        return None


def add_player(name, location):
    sql = "INSERT INTO player (name, location) VALUES (%s, %s)"
    values = (name, location)

    cursor = db.db_connection()
    cursor.execute(sql, values)


def update_player(name, new_location):
    sql = "UPDATE player SET location = %s WHERE name = %s"
    values = (new_location, name)

    cursor = db.db_connection()
    cursor.execute(sql, values)
