import mysql.connector
from datetime import datetime
import bcrypt

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vishal7084',
    'database': 'flask_auth'
}

print("="*70)
print("DATABASE VERIFICATION REPORT")
print("="*70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Test 1: Connection
print("1. CONNECTION TEST")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    print("   [PASS] Successfully connected to database")
    db.close()
except Exception as e:
    print(f"   [FAIL] Connection error: {e}")
    exit(1)

# Test 2: Tables
print("\n2. TABLE CHECK")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"   Found {len(tables)} tables:")
    for table in tables:
        print(f"   - {table}")
    cursor.close()
    db.close()
except Exception as e:
    print(f"   [FAIL] {e}")

# Test 3: Data counts
print("\n3. DATA COUNTS")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    
    for table in ['users', 'contacts', 'feedback', 'complaints', 'admissions', 'results']:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        count = cursor.fetchone()['count']
        print(f"   {table:15} : {count:5} records")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"   [FAIL] {e}")

# Test 4: Users table
print("\n4. USERS TABLE")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT id, username, email, role FROM users LIMIT 5")
    users = cursor.fetchall()
    
    if users:
        print(f"   Sample users ({len(users)}):")
        for user in users:
            print(f"   - {user['username']} ({user['role']}) - {user['email']}")
    else:
        print("   No users found")
    
    cursor.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role")
    roles = cursor.fetchall()
    print("\n   Role distribution:")
    for role in roles:
        print(f"   - {role['role']}: {role['count']}")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"   [FAIL] {e}")

# Test 5: Admissions table
print("\n5. ADMISSIONS TABLE")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT student_name, class_enroll, email FROM admissions LIMIT 5")
    admissions = cursor.fetchall()
    
    if admissions:
        print(f"   Sample admissions ({len(admissions)}):")
        for adm in admissions:
            print(f"   - {adm['student_name']} (Class: {adm['class_enroll']})")
    else:
        print("   No admissions found")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"   [FAIL] {e}")

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
        print("   [PASS] Insert and retrieve successful")
    else:
        print("   [FAIL] Could not retrieve inserted data")
    
    cursor.execute("DELETE FROM contacts WHERE id = %s", (insert_id,))
    db.commit()
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"   [FAIL] {e}")

# Test 7: Password hashing
print("\n7. PASSWORD HASHING TEST")
try:
    test_pwd = "TestPassword123"
    hashed = bcrypt.hashpw(test_pwd.encode('utf-8'), bcrypt.gensalt(rounds=4))
    is_valid = bcrypt.checkpw(test_pwd.encode('utf-8'), hashed)
    
    if is_valid:
        print("   [PASS] Password hashing and verification working")
    else:
        print("   [FAIL] Password verification failed")
except Exception as e:
    print(f"   [FAIL] {e}")

# Test 8: Check for status column in admissions
print("\n8. ADMISSIONS TABLE STRUCTURE")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    
    cursor.execute("SHOW COLUMNS FROM admissions LIKE 'status'")
    status_col = cursor.fetchone()
    
    if status_col:
        print(f"   [INFO] Status column exists: {status_col[1]}")
    else:
        print("   [WARNING] Status column not found - may need to add it")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"   [FAIL] {e}")

print("\n" + "="*70)
print("VERIFICATION COMPLETE")
print("="*70)
