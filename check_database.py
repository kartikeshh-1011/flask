import mysql.connector
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vishal7084',
    'database': 'flask_auth'
}

print("DATABASE VERIFICATION REPORT")
print("=" * 60)

# Test 1: Connection
print("\n1. CONNECTION TEST")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    print("   PASS - Successfully connected to database")
    db.close()
except Exception as e:
    print(f"   FAIL - {e}")
    exit(1)

# Test 2: Tables
print("\n2. TABLE CHECK")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"   Found {len(tables)} tables: {', '.join(tables)}")
    cursor.close()
    db.close()
except Exception as e:
    print(f"   FAIL - {e}")

# Test 3: Data counts
print("\n3. DATA COUNTS")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    
    tables_to_check = ['users', 'contacts', 'feedback', 'complaints', 'admissions', 'results']
    for table in tables_to_check:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        count = cursor.fetchone()['count']
        print(f"   {table:15} : {count} records")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"   FAIL - {e}")

# Test 4: Users sample
print("\n4. USERS TABLE SAMPLE")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT username, role, email FROM users LIMIT 3")
    users = cursor.fetchall()
    
    if users:
        for user in users:
            print(f"   - {user['username']} ({user['role']}) - {user['email']}")
    else:
        print("   No users found")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"   FAIL - {e}")

# Test 5: Check status column
print("\n5. ADMISSIONS TABLE STRUCTURE")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    
    cursor.execute("SHOW COLUMNS FROM admissions LIKE 'status'")
    result = cursor.fetchone()
    
    if result:
        print(f"   Status column EXISTS: {result[1]}")
    else:
        print("   Status column NOT FOUND - needs to be added")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"   FAIL - {e}")

# Test 6: Insert/Retrieve
print("\n6. INSERT/RETRIEVE TEST")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    
    test_name = f"TestUser_{datetime.now().strftime('%H%M%S')}"
    test_email = f"test_{datetime.now().strftime('%H%M%S')}@test.com"
    
    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
        (test_name, test_email, "Test message")
    )
    db.commit()
    insert_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM contacts WHERE id = %s", (insert_id,))
    result = cursor.fetchone()
    
    if result and result['name'] == test_name:
        print("   PASS - Insert and retrieve successful")
        cursor.execute("DELETE FROM contacts WHERE id = %s", (insert_id,))
        db.commit()
    else:
        print("   FAIL - Could not retrieve inserted data")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"   FAIL - {e}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
