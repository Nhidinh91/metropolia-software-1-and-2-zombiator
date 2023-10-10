import dbconnection as db


# This function is used to check if the player is existed in the database
def is_player_existed(player_name):
    sql = "SELECT id, name FROM player WHERE name = %s"
    values = (player_name,)

    connection, cursor = db.db_connection()

    player_exist = False
    if cursor is not None:
        cursor.execute(sql, values)
        result = cursor.fetchone()

        if result:
            player_exist = True

    cursor.close()
    connection.close()

    return player_exist


# This function is used to get the player info from the database
def get_player_info(player_name):
    sql = "SELECT id, name FROM player WHERE name = %s"
    values = (player_name,)

    connection, cursor = db.db_connection()

    player_info = None
    if cursor is not None:
        cursor.execute(sql, values)
        result = cursor.fetchone()

        if result:
            player_info = result

    cursor.close()
    connection.close()

    return player_info


# This function is used to add the player to the database
def add_player(name, location):
    sql = "INSERT INTO player (name, location) VALUES (%s, %s)"
    values = (name, location)

    connection, cursor = db.db_connection()

    if cursor is not None:
        cursor.execute(sql, values)

    cursor.close()
    connection.close()


# This function is used to update the player location in the database
def update_player(name, new_location):
    sql = "UPDATE player SET location = %s WHERE name = %s"
    values = (new_location, name)

    connection, cursor = db.db_connection()
    if cursor is not None:
        cursor.execute(sql, values)

    cursor.close()
    connection.close()
