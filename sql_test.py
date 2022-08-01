import sqlite3
from sqlite3 import Error
import datetime

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to "+path+" successful.")
        return connection
    except Error as e:
        print(f"The error '{e}' occured")
    
    return connection

def execute_query(connection, query):
    c = connection.cursor()
    try:
        c.execute(query)
        connection.commit()
        print("Query executed successfully.")
    except Error as e:
        print(f"The error '{e}' occured")

create_table = """
CREATE TABLE Trade_Log_3 (
    Action varchar(255),
    Datetime varchar(255),
    Shares float(255,2),
    Value float(255,2),
    Total_Shares float(255,2),
    Total_Value float(255,2),
    ND_PL float(255,4)
);
"""

add_row_string = """
INSERT INTO Trade_Log_3
VALUES ({0})
"""

def execute_get_table(connection):
    c = connection.cursor()
    try:
        c.execute("SELECT * FROM Trade_Log_3")
        data = c.fetchall()
        print("Get table executed successfully.")
        for row in data:
            print(row)
        return data
    except Error as e:
        print(f"The error '{e}' occured")

def add_row(connection, date, action, row):
    c = connection.cursor()
    try:
        row_data = "'"+date.strftime('%Y-%m-%d %H:%M:%S')+"','"+action+"'"
        for i in row:
            row_data = row_data+","+str(i)
        c.execute(add_row_string.format(row_data))
        print("Add row executed successfully.")
    except Error as e:
        print(f"The error '{e}' occured")

connection = create_connection(r'data.db')
print(connection)
#execute_query(connection, create_table)
add_row(connection, datetime.datetime(2022,7,18,21,6,23,341),'Sell', [0.1 ,789.89,4.5,90179.65,0.1245])
z = execute_get_table(connection)
print(z)

