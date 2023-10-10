import dbconnection as db

def get_dict_airportcoordinate_fromcountry():
    dict_airport_coordinate = {}
    sql = "SELECT country, latitude_deg, longitude_deg FROM airport"

    cursor = db.db_connection()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            coordinate = (row[1], row[2])
            dict_airport_coordinate[row[0]] = coordinate

    return dict_airport_coordinate
