import pandas as pd
import psycopg2

connection = psycopg2.connect(database="master", user="postgres", password="0000")
cursor = connection.cursor()
cursor.execute("SELECT * FROM employees")
employee_data = pd.DataFrame(cursor.fetchall(), columns=['id', 'name', 'surname'])
connection.close()

print(employee_data)

employee_performance = pd.read_excel('reports\performance\Employee Performance.xlsx').rename(columns={'ID': 'id', 'SCORE': 'score'})

print()
print(employee_performance)

report_df = pd.merge(employee_data, employee_performance, on='id')
report_df.sort_values(by=['score'], ascending=False, inplace=True)

print()
print(report_df)
