import mysql.connector

connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        database="zombiator",
        user="root",
        password="Bu@1234#Li",
        autocommit=True
    )
countries = []
sql1 = "SELECT country FROM airport"
cursor = connection.cursor()
cursor.execute(sql1)
result1 = cursor.fetchall()
countries = result1

def get_dict_distance(current_location):
    dict_distance = {}
    dict_airport_coordinate = get_dict_airportcoordinate_by_country(countries)
    for country in dict_airport_coordinate:
        distance = calculate_distance(current_location,country)
        dict_distance[country] = distance
    return dict_distance
dict_distance = get_dict_distance("Finland")
print(dict_distance)