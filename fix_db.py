import mysql.connector

# Connect to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vishal7084",
    database="flask_auth"
)

cursor = db.cursor()

print("Updating users table to add 'Parent' to role ENUM...")

# Modify the role column to include 'Parent'
cursor.execute("""
    ALTER TABLE users 
    MODIFY COLUMN role ENUM('Teacher', 'Admin', 'Student', 'Parent') 
    DEFAULT 'Student'
""")

db.commit()

print("✓ Successfully updated role column!")

# Verify the change
cursor.execute("SHOW COLUMNS FROM users WHERE Field = 'role'")
role_info = cursor.fetchone()
print(f"\nUpdated role column info: {role_info}")

cursor.close()
db.close()

print("\n✓ Database schema updated successfully!")
print("Parents can now sign up without errors.")
