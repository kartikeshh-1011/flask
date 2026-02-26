import mysql.connector
import sys

def check_database():
    print("================ DATABASE VERIFICATION ================")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal7084",
            database="flask_auth"
        )
        cursor = conn.cursor()
        
        # 1. List Tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"Found {len(tables)} tables: {', '.join(tables)}")
        
        required_tables = [
            'users', 'teacher_admissions', 'admissions', 
            'cancelled_admissions', 'cancelled_teachers',
            'students', 'parents', 'teachers',
            'results', 'contacts', 'feedback', 'complaints'
        ]
        
        missing = [t for t in required_tables if t not in tables]
        
        if missing:
            print(f"❌ MISSING TABLES: {', '.join(missing)}")
        else:
            print("✅ All core tables are present.")

        # 2. Check Table Counts
        print("\n--- Row Counts ---")
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table}: {count} rows")
            except Exception as e:
                print(f"{table}: Error counting - {e}")

        # 3. Check specific user 'tea1'
        print("\n--- User Check ('tea1') ---")
        cursor.execute("SELECT * FROM users WHERE username = 'tea1' OR username = 'hhh'") # 'hhh' was in screenshot
        users = cursor.fetchall()
        if users:
            for u in users:
                print(f"Found user: ID={u[0]}, Username={u[1]}, Email={u[2]}, Role={u[4]}")
                
                # Check if this user has admission data
                if u[4] == 'Teacher':
                    cursor.execute(f"SELECT * FROM teacher_admissions WHERE email = '{u[2]}'")
                    tea_data = cursor.fetchone()
                    print(f"  -> Admission Record: {'✅ Found' if tea_data else '❌ Not Found (Should redirect to admission form)'}")
        else:
            print("❌ User 'tea1' or 'hhh' not found in users table.")

        conn.close()
        print("\n================ VERIFICATION COMPLETE ================")
        
    except mysql.connector.Error as err:
        print(f"❌ DATABASE CONNECTION ERROR: {err}")

if __name__ == "__main__":
    check_database()
