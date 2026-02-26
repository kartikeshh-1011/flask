import mysql.connector
from mysql.connector import Error

def check_teacher_data():
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host='localhost',
            database='flask_auth',
            user='root',
            password='vishal7084'
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # Check if table exists
            cursor.execute("SHOW TABLES LIKE 'teacher_admissions'")
            table_exists = cursor.fetchone()
            print(f"Table exists: {table_exists}")
            
            # Get all teacher records
            cursor.execute("SELECT * FROM teacher_admissions ORDER BY created_at DESC")
            teachers = cursor.fetchall()
            
            print(f"\nTotal teachers in database: {len(teachers)}")
            
            for i, teacher in enumerate(teachers, 1):
                print(f"\n--- Teacher {i} ---")
                print(f"ID: {teacher.get('id')}")
                print(f"Full Name: {teacher.get('full_name')}")
                print(f"Email: {teacher.get('email')}")
                print(f"Phone: {teacher.get('phone')}")
                print(f"Designation: {teacher.get('designation')}")
                print(f"Department: {teacher.get('department')}")
                print(f"Employee ID: {teacher.get('employee_id')}")
                print(f"Qualification: {teacher.get('highest_qualification')}")
                print(f"Created at: {teacher.get('created_at')}")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_teacher_data()
