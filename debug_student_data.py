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

def find_student_in_all_tables(email, cursor):
    tables = ['admissions_v', 'admissions_vi', 'admissions_vii', 'admissions_viii', 
              'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM {table} WHERE email = %s", (email,))
            student = cursor.fetchone()
            if student:
                return student
        except Exception as e:
            print(f"Error searching {table}: {e}")
            continue
    return None

def debug_student(email):
    print(f"Debugging student: {email}")
    try:
        db = get_db_connection()
        if not db:
            print("DB Connection failed")
            return
            
        cursor = db.cursor(dictionary=True)
        
        # 1. Search for student
        print("Searching for student record...")
        student_data = find_student_in_all_tables(email, cursor)
        
        if student_data:
            print("Student FOUND:")
            print(student_data)
            
            class_enroll = student_data.get('class_enroll')
            print(f"Class Enroll: {class_enroll}")
            
            # 2. Check Class Teacher
            print("\nChecking Class Teacher...")
            try:
                cursor.execute("""
                    SELECT t.*, ct.section 
                    FROM class_teachers ct
                    JOIN teacher_admissions t ON ct.teacher_email = t.email
                    WHERE ct.class_name = %s
                """, (class_enroll,))
                class_teacher = cursor.fetchone()
                print("Class Teacher Found:" if class_teacher else "Class Teacher NOT Found")
                if class_teacher: print(class_teacher)
            except Exception as e:
                print(f"Class Teacher Query Error: {e}")

            # 3. Check Subject Teachers
            print("\nChecking Subject Teachers...")
            try:
                cursor.execute("""
                    SELECT st.subject_name, t.* 
                    FROM subject_teachers st
                    JOIN teacher_admissions t ON st.teacher_email = t.email
                    WHERE st.class_name = %s
                """, (class_enroll,))
                subject_teachers = cursor.fetchall()
                print(f"Subject Teachers Found: {len(subject_teachers)}")
                for st in subject_teachers:
                    print(st)
            except Exception as e:
                print(f"Subject Teacher Query Error: {e}")
                
        else:
            print("Student NOT FOUND in any admissions table")
            
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"General Error: {e}")

if __name__ == "__main__":
    debug_student('vaishnavi@gmail.com')
