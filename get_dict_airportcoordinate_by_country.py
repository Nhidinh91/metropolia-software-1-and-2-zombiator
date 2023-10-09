import mysql.connector

connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        database="zombiator",
        user="root",
        password="Bu@1234#Li",
        autocommit=True
    )

def get_dict_airportcoordinate_by_country():
    dict_airport_coordinate = {}
    sql = "SELECT country, latitude_deg, longitude_deg FROM airport"

    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            coordinate = (row[1], row[2])
            dict_airport_coordinate[row[0]] = coordinate
    return dict_airport_coordinate





