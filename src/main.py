import pandas as pd
import psycopg2
from fpdf import FPDF
from datetime import datetime
from pathlib import Path

# Connect to the database and retrieve employee data.
password = "0000"
connection = psycopg2.connect(database="master", user="postgres", password=password)
cursor = connection.cursor()
cursor.execute("SELECT * FROM employees")
employee_data = pd.DataFrame(cursor.fetchall(), columns=['id', 'name', 'surname']).set_index('id')
connection.close()

print(employee_data)

# Get employee performance data from Excel document.
employee_performance = pd.read_excel("reports\performance\employee-performance.xlsx").rename(columns={'ID': 'id', 'SCORE': 'score'}).set_index('id')

print()
print(employee_performance)

# Form a report dataframe combining employee data and performance.
report_df = pd.merge(employee_data, employee_performance, on='id')

# Sort the dataframe based on the performance score.
report_df.sort_values(by=['score'], ascending=False, inplace=True)

print()
print(report_df)

# Output the report to a .pdf file.
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)

pdf.cell(40, 10, "Employee Performance Report")
pdf.ln(20)

pdf.set_font('Arial', '', 12)

row_height = 10
for i, (_, row) in enumerate(report_df.iterrows()):
    pdf.cell(40, row_height, f"\t{i + 1}. {row['name']} {row['surname']}: {row['score']}")
    pdf.ln(row_height)

path = Path(fr"reports\full\report-{datetime.now().strftime('%d-%m-%Y')}.pdf").absolute()
pdf.output(path, "F")
