import mysql.connector

db_conn = mysql.connector.connect(host="lab6-servicebased.eastus.cloudapp.azure.com", user="user",
password="#4Havel", database="macro_weight_tracker")

db_cursor = db_conn.cursor()

db_cursor.execute('''
DROP TABLE weight_logging, macro_logging
''')
db_conn.commit()
db_conn.close()