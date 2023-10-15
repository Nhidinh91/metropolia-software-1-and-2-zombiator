import dbconnection as db


# This function is used to check if the player is existed in the database
def is_player_existed(player_name):
    sql = "SELECT id, name FROM player"

    connection, cursor = db.db_connection()

    player_exist = False
    if cursor is not None:
        cursor.execute(sql)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            for row in result:
                if row[1] == player_name:
                    player_exist = True
                    break

    cursor.close()
    connection.close()

    return player_exist


# This function is used to get the player info from the database
def get_player_info(player_name):
    sql = "SELECT id, name FROM player"

    connection, cursor = db.db_connection()

    player_info = None
    if cursor is not None:
        cursor.execute(sql)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            for row in result:
                if row[1] == player_name:
                    player_info = (row[0], row[1])

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
def update_player(player_id, new_location):
    sql = "UPDATE player SET location = %s WHERE id = %s"
    values = (new_location, player_id)

    connection, cursor = db.db_connection()
    if cursor is not None:
        cursor.execute(sql, values)

    cursor.close()
    connection.close()
