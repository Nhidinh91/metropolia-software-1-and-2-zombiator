import dbconnection as db


# This function is used to add user ranking to the database
def add_ranking(player_id, score):
    sql = "INSERT INTO ranking (player_id, score) VALUES (%s, %s)"
    values = (player_id, score)

    connection, cursor = db.db_connection()
    if cursor is not None:
        cursor.execute(sql, values)

    cursor.close()
    connection.close()


# This function is used to update the player score in the database
def update_player_score(player_id, new_score):
    sql = "UPDATE ranking SET score = %s WHERE player_id = %s"
    values = (new_score, player_id)

    connection, cursor = db.db_connection()

    if cursor is not None:
        cursor.execute(sql, values)

    cursor.close()
    connection.close()

# This function is used to get all player ranking from the database
def get_all_player_ranking():
    sql = "SELECT player.id, player.name, ranking.score FROM ranking JOIN player ON ranking.player_id = player.id ORDER BY ranking.score DESC"

    connection, cursor = db.db_connection()

    rankings = None
    if cursor is not None:
        cursor.execute(sql)

        # Fetch all rows as a list of tuples
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            rankings = result

    cursor.close()
    connection.close()

    return rankings

# This function is used to get the player ranking from the database
def get_ranking_info(player_id):
    sql = "SELECT * FROM ranking WHERE player_id = %s"
    values = (player_id,)

    connection, cursor = db.db_connection()

    ranking_info = None
    if cursor is not None:
        cursor.execute(sql, values)

        result = cursor.fetchone()

        if result:
            ranking_info = result

    cursor.close()
    connection.close()

    return ranking_info
