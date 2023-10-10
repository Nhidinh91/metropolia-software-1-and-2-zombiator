import dbconnection as db


# This function returns a dictionary with the country as key and the coordinate as value
def get_dict_airportcoordinate_fromcountry():
    dict_airport_coordinate = {}
    sql = "SELECT country, latitude_deg, longitude_deg FROM airport"

    connection, cursor = db.db_connection()

    if cursor is not None:
        cursor.execute(sql)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            for row in result:
                coordinate = (row[1], row[2])
                dict_airport_coordinate[row[0]] = coordinate

        cursor.close()
        connection.close()

    return dict_airport_coordinate
