"""
Comprehensive Database Verification Script
This script checks if the database is working correctly and storing data properly
"""

import mysql.connector
from datetime import datetime
import bcrypt

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vishal7084',
    'database': 'flask_auth'
}

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_connection():
    """Test database connection"""
    print_header("1. DATABASE CONNECTION TEST")
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        print("✓ Successfully connected to MySQL database")
        print(f"  Database: {DB_CONFIG['database']}")
        print(f"  Host: {DB_CONFIG['host']}")
        db.close()
        return True
    except mysql.connector.Error as err:
        print(f"✗ Connection failed: {err}")
        return False

def check_tables():
    """Check if all required tables exist"""
    print_header("2. TABLE STRUCTURE CHECK")
    
    required_tables = ['users', 'contacts', 'feedback', 'complaints', 'admissions', 'results']
    
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        print(f"Found {len(existing_tables)} tables in database:")
        
        all_present = True
        for table in required_tables:
            if table in existing_tables:
                print(f"  ✓ {table}")
            else:
                print(f"  ✗ {table} - MISSING!")
                all_present = False
        
        cursor.close()
        db.close()
        
        return all_present
    except Exception as e:
        print(f"✗ Error checking tables: {e}")
        return False

def check_table_structure():
    """Check structure of each table"""
    print_header("3. TABLE COLUMN VERIFICATION")
    
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        # Check users table
        print("\n📋 USERS Table:")
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        # Check if 'role' column exists and has correct ENUM values
        cursor.execute("SHOW COLUMNS FROM users LIKE 'role'")
        role_column = cursor.fetchone()
        if role_column:
            print(f"  ✓ Role column exists: {role_column[1]}")
        else:
            print("  ✗ Role column MISSING!")
        
        # Check admissions table
        print("\n📋 ADMISSIONS Table:")
        cursor.execute("DESCRIBE admissions")
        columns = cursor.fetchall()
        print(f"  Total columns: {len(columns)}")
        
        # Check if status column exists
        cursor.execute("SHOW COLUMNS FROM admissions LIKE 'status'")
        status_column = cursor.fetchone()
        if status_column:
            print(f"  ✓ Status column exists: {status_column[1]}")
        else:
            print("  ⚠ Status column not found (may need to be added)")
        
        # Check results table
        print("\n📋 RESULTS Table:")
        cursor.execute("DESCRIBE results")
        columns = cursor.fetchall()
        print(f"  Total columns: {len(columns)}")
        
        cursor.close()
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error checking table structure: {e}")
        return False

def check_data_counts():
    """Check how much data is stored in each table"""
    print_header("4. DATA COUNT VERIFICATION")
    
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary=True)
        
        tables = ['users', 'contacts', 'feedback', 'complaints', 'admissions', 'results']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            count = cursor.fetchone()['count']
            print(f"  {table:15} : {count:5} records")
        
        cursor.close()
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error counting data: {e}")
        return False

def check_users_data():
    """Display sample users data"""
    print_header("5. USERS TABLE DATA SAMPLE")
    
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC LIMIT 5")
        users = cursor.fetchall()
        
        if users:
            print(f"\n  Recent {len(users)} users:")
            for user in users:
                print(f"  - ID: {user['id']}, Username: {user['username']}, Role: {user['role']}, Email: {user['email']}")
        else:
            print("  ⚠ No users found in database")
        
        # Check role distribution
        cursor.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role")
        role_counts = cursor.fetchall()
        
        print("\n  Role Distribution:")
        for role in role_counts:
            print(f"  - {role['role']}: {role['count']} users")
        
        cursor.close()
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error checking users: {e}")
        return False

def check_admissions_data():
    """Display sample admissions data"""
    print_header("6. ADMISSIONS TABLE DATA SAMPLE")
    
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT id, student_name, email, class_enroll, created_at FROM admissions ORDER BY created_at DESC LIMIT 5")
        admissions = cursor.fetchall()
        
        if admissions:
            print(f"\n  Recent {len(admissions)} admissions:")
            for adm in admissions:
                print(f"  - ID: {adm['id']}, Student: {adm['student_name']}, Class: {adm['class_enroll']}")
        else:
            print("  ⚠ No admissions found in database")
        
        cursor.close()
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error checking admissions: {e}")
        return False

def test_insert_and_retrieve():
    """Test inserting and retrieving data"""
    print_header("7. INSERT/RETRIEVE TEST")
    
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary=True)
        
        # Test contact form insert
        test_name = f"Test User {datetime.now().strftime('%H%M%S')}"
        test_email = f"test{datetime.now().strftime('%H%M%S')}@example.com"
        test_message = "This is a test message for database verification"
        
        print(f"\n  Testing INSERT into contacts table...")
        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (test_name, test_email, test_message)
        )
        db.commit()
        insert_id = cursor.lastrowid
        print(f"  ✓ Successfully inserted record with ID: {insert_id}")
        
        # Retrieve the inserted data
        print(f"\n  Testing SELECT from contacts table...")
        cursor.execute("SELECT * FROM contacts WHERE id = %s", (insert_id,))
        result = cursor.fetchone()
        
        if result and result['name'] == test_name:
            print(f"  ✓ Successfully retrieved record")
            print(f"    Name: {result['name']}")
            print(f"    Email: {result['email']}")
            print(f"    Message: {result['message']}")
        else:
            print(f"  ✗ Failed to retrieve inserted record")
        
        # Clean up test data
        cursor.execute("DELETE FROM contacts WHERE id = %s", (insert_id,))
        db.commit()
        print(f"\n  ✓ Test data cleaned up")
        
        cursor.close()
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error in insert/retrieve test: {e}")
        return False

def check_password_hashing():
    """Verify password hashing is working"""
    print_header("8. PASSWORD HASHING TEST")
    
    try:
        test_password = "TestPassword123"
        
        # Hash the password
        hashed = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt(rounds=4))
        print(f"  ✓ Password hashing successful")
        print(f"    Original: {test_password}")
        print(f"    Hashed length: {len(hashed)} bytes")
        
        # Verify the password
        is_valid = bcrypt.checkpw(test_password.encode('utf-8'), hashed)
        if is_valid:
            print(f"  ✓ Password verification successful")
        else:
            print(f"  ✗ Password verification failed")
        
        return is_valid
        
    except Exception as e:
        print(f"✗ Error in password hashing test: {e}")
        return False

def check_indexes():
    """Check if indexes are properly created"""
    print_header("9. INDEX VERIFICATION")
    
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        # Check indexes on users table
        print("\n  USERS table indexes:")
        cursor.execute("SHOW INDEX FROM users")
        indexes = cursor.fetchall()
        for idx in indexes:
            print(f"  - {idx[2]} on column {idx[4]}")
        
        cursor.close()
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error checking indexes: {e}")
        return False

def main():
    """Run all verification tests"""
    print("\n" + "🔍 DATABASE VERIFICATION SCRIPT".center(70, "="))
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Run all tests
    results.append(("Connection Test", test_connection()))
    results.append(("Table Check", check_tables()))
    results.append(("Table Structure", check_table_structure()))
    results.append(("Data Counts", check_data_counts()))
    results.append(("Users Data", check_users_data()))
    results.append(("Admissions Data", check_admissions_data()))
    results.append(("Insert/Retrieve Test", test_insert_and_retrieve()))
    results.append(("Password Hashing", check_password_hashing()))
    results.append(("Index Check", check_indexes()))
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {test_name:25} : {status}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🎉 ALL TESTS PASSED! Database is working correctly.")
    else:
        print(f"\n  ⚠ {total - passed} test(s) failed. Please review the errors above.")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
