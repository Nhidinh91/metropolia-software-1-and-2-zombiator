import dbconnection

sql = "SELECT * FROM airport"

cursor = dbconnection.db_connection()
cursor.execute(sql)
result = cursor.fetchall()

print(result)

