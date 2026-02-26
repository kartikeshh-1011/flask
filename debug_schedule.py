import mysql.connector
import json

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vishal7084',
    'database': 'flask_auth'
}

def check_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Check a specific student's class (from the screenshot)
        student_email = 'kartikesh@gmail.com'
        
        # We need to find which table they are in.
        # Based on previous knowledge, we check admissions_x for 'kartikesh' or just search all?
        # Let's search all known class tables or just check the logic 
        # But for debugging, I'll just check if I can find him.
        
        tables = [
            'admissions_v', 'admissions_vi', 'admissions_vii', 'admissions_viii',
            'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii'
        ]
        
        student_class = None
        for table in tables:
            try:
                cursor.execute(f"SELECT class_enroll FROM {table} WHERE email = %s", (student_email,))
                result = cursor.fetchone()
                if result:
                    student_class = result['class_enroll']
                    print(f"Student found in {table}, Class: '{student_class}'")
                    break
            except Exception as e:
                pass
                
        if not student_class:
            print("Student not found in any class table.")

        # Check schedules
        print("\nSchedules content:")
        cursor.execute("SELECT * FROM schedules")
        schedules = cursor.fetchall()
        for s in schedules:
            print(f"Teacher: {s['teacher_email']}, Class: '{s['class_name']}', Time: {s['start_time']}-{s['end_time']}")

        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_data()
