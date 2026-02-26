import mysql.connector

try:
    print("Attempting to connect to the database...")
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vishal7084",
        database="flask_auth"
    )
    
    if db.is_connected():
        print("SUCCESS: Connected to database 'flask_auth'")
        
        cursor = db.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database: ", record[0])
        
        # Check if users table exists
        cursor.execute("SHOW TABLES LIKE 'users'")
        result = cursor.fetchone()
        if result:
            print("Table 'users' exists.")
        else:
            print("WARNING: Table 'users' does not exist!")
            
        cursor.close()
        db.close()
        print("MySQL connection is closed")

except mysql.connector.Error as err:
    print(f"ERROR: Could not connect to database. {err}")
except Exception as e:
    print(f"ERROR: An unexpected error occurred: {e}")
