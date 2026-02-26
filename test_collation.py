import mysql.connector

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal7084",
            database="flask_auth"
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def test_joins():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("Testing Class Teacher Join...")
        try:
            cursor.execute("""
                SELECT ct.*, t.full_name as teacher_name 
                FROM class_teachers ct 
                JOIN teacher_admissions t ON ct.teacher_email = t.email
                LIMIT 1
            """)
            result = cursor.fetchall() # Consume result
            print("Class Teacher Join OK")
        except Exception as e:
            print(f"Class Teacher Join ERROR: {e}")

        print("\nTesting Subject Teacher Join...")
        try:
            cursor.execute("""
                SELECT st.*, t.full_name as teacher_name 
                FROM subject_teachers st 
                JOIN teacher_admissions t ON st.teacher_email = t.email
                LIMIT 1
            """)
            result = cursor.fetchall() # Consume result
            print("Subject Teacher Join OK")
        except Exception as e:
            print(f"Subject Teacher Join ERROR: {e}")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_joins()
