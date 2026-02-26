import mysql.connector
import os

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

def test_admin_queries():
    try:
        db = get_db_connection()
        if not db:
            print("Failed to connect to DB")
            return
            
        cursor = db.cursor(dictionary=True)
        
        # Test 1: Admissions Count
        print("Testing Admissions Count...")
        tables = ['admissions_v', 'admissions_vi', 'admissions_vii', 'admissions_viii', 
                  'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii']
        total_admissions = 0
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                total_admissions += cursor.fetchone()['count']
            except Exception as e:
                print(f"Error querying {table}: {e}")
                
        print(f"Total Admissions: {total_admissions}")

        # Test 2: Teachers Count
        print("\nTesting Teachers Count...")
        cursor.execute("SELECT COUNT(*) as count FROM teacher_admissions")
        print(f"Total Teachers: {cursor.fetchone()['count']}")

        # Test 3: Students List
        print("\nTesting Students List...")
        union_query = " UNION ALL ".join([f"SELECT student_name, email, class_enroll, created_at FROM {table}" for table in tables])
        union_query += " ORDER BY created_at DESC LIMIT 10"
        cursor.execute(union_query)
        students = cursor.fetchall()
        print(f"Fetched {len(students)} students")

        # Test 4: Teachers List
        print("\nTesting Teachers List...")
        cursor.execute("""
            SELECT full_name, email, employee_id, department, phone 
            FROM teacher_admissions 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        teachers = cursor.fetchall()
        print(f"Fetched {len(teachers)} teachers")

        # Test 5: All Teachers (for dropdown)
        print("\nTesting All Teachers...")
        cursor.execute("""
            SELECT full_name, email, employee_id, department, phone 
            FROM teacher_admissions 
            ORDER BY full_name ASC
        """)
        all_teachers = cursor.fetchall()
        print(f"Fetched {len(all_teachers)} all_teachers")

        # Test 6: Class Teachers Assignments
        print("\nTesting Class Teachers Assignments...")
        cursor.execute("""
            SELECT ct.*, t.full_name as teacher_name 
            FROM class_teachers ct 
            JOIN teacher_admissions t ON ct.teacher_email = t.email
            ORDER BY ct.class_name, ct.section
        """)
        class_teachers_assignments = cursor.fetchall()
        print(f"Fetched {len(class_teachers_assignments)} class teacher assignments")

        # Test 7: Subject Teachers Assignments
        print("\nTesting Subject Teachers Assignments...")
        cursor.execute("""
            SELECT st.*, t.full_name as teacher_name 
            FROM subject_teachers st 
            JOIN teacher_admissions t ON st.teacher_email = t.email
            ORDER BY st.class_name, st.subject_name
        """)
        subject_teachers_assignments = cursor.fetchall()
        print(f"Fetched {len(subject_teachers_assignments)} subject teacher assignments")

        cursor.close()
        db.close()
        print("\nALL TESTS PASSED")

    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")

if __name__ == "__main__":
    test_admin_queries()
