import mysql.connector

# Test database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vishal7084",
        database="flask_auth"
    )
    print("✓ Database connection successful!")
    
    cursor = db.cursor()
    
    # Check if database exists
    cursor.execute("SHOW DATABASES LIKE 'flask_auth'")
    if cursor.fetchone():
        print("✓ Database 'flask_auth' exists")
    else:
        print("✗ Database 'flask_auth' does NOT exist")
        
    # Check tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\n✓ Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]}")
        
    # Check users table structure
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    print("\n✓ Users table structure:")
    for col in columns:
        print(f"  - {col[0]} ({col[1]})")
        
    cursor.close()
    db.close()
    print("\n✓ All database checks passed!")
    
except mysql.connector.Error as err:
    print(f"✗ Database error: {err}")
except Exception as e:
    print(f"✗ Error: {e}")
