import pandas as pd
import psycopg2

connection = psycopg2.connect(database="master", user="postgres", password="0000")
cursor = connection.cursor()
cursor.execute("SELECT * FROM employees")
employee_data = pd.DataFrame(cursor.fetchall(), columns=['id', 'name', 'surname'])
connection.close()

print(employee_data)
