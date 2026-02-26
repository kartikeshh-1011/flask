import mysql.connector

# Connect to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vishal7084",
    database="flask_auth"
)

cursor = db.cursor()

# Check current table structure
print("Current users table structure:")
cursor.execute("DESCRIBE users")
for row in cursor.fetchall():
    print(row)

print("\n" + "="*50 + "\n")

# Check if role column is ENUM
cursor.execute("SHOW COLUMNS FROM users WHERE Field = 'role'")
role_info = cursor.fetchone()
print(f"Role column info: {role_info}")

cursor.close()
db.close()
