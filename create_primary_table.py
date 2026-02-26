import mysql.connector

conn = mysql.connector.connect(
    host='localhost', user='root', password='vishal7084', database='flask_auth'
)
cursor = conn.cursor()

cursor.execute("DELETE FROM admissions_primary WHERE class_enroll IN ('Play Group', 'Nursery', 'LKG', 'UKG')")
conn.commit()
print(f'Deleted {cursor.rowcount} row(s) with removed class values.')

cursor.close()
conn.close()
