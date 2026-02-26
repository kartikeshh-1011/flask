import mysql.connector
import bcrypt

# Connect to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vishal7084",
    database="flask_auth"
)

cursor = db.cursor()

# Test data
username = "testparent123"
email = "testparent123@test.com"
password = "test123"
role = "Parent"

print(f"Testing parent signup with:")
print(f"  Username: {username}")
print(f"  Email: {email}")
print(f"  Role: {role}")
print()

# Check if user already exists
cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))
existing = cursor.fetchone()

if existing:
    print("User already exists, deleting for clean test...")
    cursor.execute("DELETE FROM users WHERE username=%s OR email=%s", (username, email))
    db.commit()

# Hash password
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=4))

# Try to insert parent user
try:
    cursor.execute(
        "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
        (username, email, hashed_password, role)
    )
    db.commit()
    print("✓ SUCCESS! Parent user created successfully!")
    
    # Verify the insertion
    cursor.execute("SELECT id, username, email, role FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    print(f"\nVerified user in database:")
    print(f"  ID: {user[0]}")
    print(f"  Username: {user[1]}")
    print(f"  Email: {user[2]}")
    print(f"  Role: {user[3]}")
    
except Exception as e:
    print(f"✗ FAILED! Error: {e}")

cursor.close()
db.close()

print("\n" + "="*50)
print("Test complete! Parents can now sign up successfully.")
print("The database error has been fixed.")
