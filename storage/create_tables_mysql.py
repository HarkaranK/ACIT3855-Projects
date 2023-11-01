import mysql.connector
db_conn = mysql.connector.connect(host="lab6-servicebased.eastus.cloudapp.azure.com", user="user",
password="#4Havel", database="macro_weight_tracker")

db_cursor = db_conn.cursor()

create_adding_weight_table = ('''
    CREATE TABLE weight_logging
    (
        id INT AUTO_INCREMENT PRIMARY KEY,
        weight DECIMAL NOT NULL,
        note TEXT,
        trace_id VARCHAR(36) NOT NULL,
        date_created VARCHAR(100) NOT NULL
    )
''')

create_adding_macro_table = ('''
    CREATE TABLE macro_logging
    (
        id INT AUTO_INCREMENT PRIMARY KEY,
        protein DECIMAL,
        carbohydrate DECIMAL,
        fats DECIMAL,
        vitamin_A DECIMAL,
        vitamin_B DECIMAL,
        vitamin_C DECIMAL,
        vitamin_D DECIMAL,
        vitamin_E DECIMAL,
        vitamin_K DECIMAL,
        calcium DECIMAL,
        sodium DECIMAL,
        iron DECIMAL,
        potassium DECIMAL,
        magnesium DECIMAL,
        zinc DECIMAL,
        omega_3 DECIMAL,
        omega_6 DECIMAL,
        trace_id VARCHAR(36) NOT NULL,
        date_created VARCHAR(100) NOT NULL
    )
''')

db_cursor.execute(create_adding_weight_table)
db_cursor.execute(create_adding_macro_table)

db_conn.commit()
db_conn.close()