import mysql.connector

cnx = mysql.connector.connect(user='root',password='admin',
                              host='127.0.0.1',
                              database='test')

cursor = cnx.cursor()
cursor.execute("SHOW TABLES;")
print(cursor.fetchall())
cnx.close()
