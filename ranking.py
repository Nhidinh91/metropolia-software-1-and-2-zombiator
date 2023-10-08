import dbconnection as db


def add_ranking(player_id, score):
    sql = "INSERT INTO ranking (player_id, score) VALUES (%s, %s)"
    values = (player_id, score)

    cursor = db.db_connection()
    cursor.execute(sql, values)


def update_player_score(player_id, new_score):
    sql = "UPDATE ranking SET score = %s WHERE player_id = %s"
    values = (new_score, player_id)

    cursor = db.db_connection()
    cursor.execute(sql, values)


def get_all_player_ranking():
    sql = "SELECT player.name, ranking.score FROM ranking JOIN player ON ranking.player_id = player.id ORDER BY ranking.score DESC"

    cursor = db.db_connection()
    cursor.execute(sql)

    # Fetch all rows as a list of tuples
    rankings = cursor.fetchall()

    return rankings


def get_ranking_info(player_id):
    sql = "SELECT * FROM ranking WHERE player_id = %s"
    values = (player_id,)

    cursor = db.db_connection()
    cursor.execute(sql, values)

    ranking_info = cursor.fetchone()

    if ranking_info:
        return ranking_info
    else:
        return None
