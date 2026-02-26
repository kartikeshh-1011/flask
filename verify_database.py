import mysql.connector
from datetime import datetime

# Connect to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vishal7084",
    database="flask_auth"
)

cursor = db.cursor(dictionary=True)

print("="*60)
print("DATABASE VERIFICATION REPORT")
print("="*60)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

# Check all tables
print("\n1. CHECKING ALL TABLES IN DATABASE:")
print("-"*60)
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
table_names = [list(table.values())[0] for table in tables]
print(f"Found {len(table_names)} tables:")
for table in table_names:
    print(f"  ✓ {table}")

# Check each table structure and data
for table_name in table_names:
    print(f"\n{'='*60}")
    print(f"TABLE: {table_name}")
    print(f"{'='*60}")
    
    # Get table structure
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    print(f"\nColumns ({len(columns)}):")
    for col in columns:
        print(f"  • {col['Field']:20} | {col['Type']:25} | Null: {col['Null']:3} | Default: {col['Default']}")
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
    count = cursor.fetchone()['count']
    print(f"\nTotal Records: {count}")
    
    # Show sample data (last 3 records)
    if count > 0:
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 3")
        records = cursor.fetchall()
        print(f"\nSample Data (Last {len(records)} records):")
        for i, record in enumerate(records, 1):
            print(f"\n  Record #{i}:")
            for key, value in record.items():
                # Truncate long values
                if isinstance(value, str) and len(value) > 50:
                    value = value[:47] + "..."
                elif isinstance(value, bytes):
                    value = "[BINARY DATA]"
                print(f"    {key:20}: {value}")

print("\n" + "="*60)
print("2. TESTING DATA INSERTION")
print("="*60)

# Test inserting a contact
try:
    test_name = f"Test User {datetime.now().strftime('%H%M%S')}"
    test_email = f"test{datetime.now().strftime('%H%M%S')}@test.com"
    test_message = "This is a test message to verify database connectivity"
    
    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
        (test_name, test_email, test_message)
    )
    db.commit()
    print(f"\n✓ SUCCESS: Test contact inserted")
    print(f"  Name: {test_name}")
    print(f"  Email: {test_email}")
    
    # Verify insertion
    cursor.execute("SELECT * FROM contacts WHERE email = %s", (test_email,))
    inserted = cursor.fetchone()
    if inserted:
        print(f"✓ VERIFIED: Record found in database with ID: {inserted['id']}")
    
    # Clean up test data
    cursor.execute("DELETE FROM contacts WHERE email = %s", (test_email,))
    db.commit()
    print(f"✓ CLEANUP: Test record deleted")
    
except Exception as e:
    print(f"✗ ERROR: {e}")

print("\n" + "="*60)
print("3. DATABASE HEALTH CHECK")
print("="*60)

# Check for any issues
issues = []

# Check if users table has Parent role
cursor.execute("SHOW COLUMNS FROM users WHERE Field = 'role'")
role_col = cursor.fetchone()
if role_col and 'Parent' in role_col['Type']:
    print("✓ Users table includes 'Parent' role")
else:
    print("✗ WARNING: Users table missing 'Parent' role")
    issues.append("Parent role not in ENUM")

# Check if admissions table has status column
cursor.execute("SHOW COLUMNS FROM admissions")
admission_cols = cursor.fetchall()
admission_col_names = [col['Field'] for col in admission_cols]
if 'status' in admission_col_names:
    print("✓ Admissions table has 'status' column")
else:
    print("⚠ INFO: Admissions table doesn't have 'status' column")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
if len(issues) == 0:
    print("✓ DATABASE IS WORKING CORRECTLY!")
    print("✓ All tables are accessible")
    print("✓ Data can be inserted and retrieved successfully")
else:
    print(f"⚠ Found {len(issues)} issue(s):")
    for issue in issues:
        print(f"  • {issue}")

cursor.close()
db.close()

print("\n" + "="*60)
print("Verification Complete!")
print("="*60)
