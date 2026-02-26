import mysql.connector

def check_collation():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal7084",
            database="flask_auth"
        )
        cursor = conn.cursor(dictionary=True)
        
        print("--- Collation Check ---")
        
        cursor.execute("SHOW FULL COLUMNS FROM teacher_admissions WHERE Field='email'")
        row = cursor.fetchone()
        print(f"teacher_admissions.email: {row['Collation']}")
        
        cursor.execute("SHOW FULL COLUMNS FROM class_teachers WHERE Field='teacher_email'")
        row = cursor.fetchone()
        print(f"class_teachers.teacher_email: {row['Collation']}")
        
        conn.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    check_collation()
