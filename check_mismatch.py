import mysql.connector

def check_data_mismatch():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='flask_auth',
            user='root',
            password='vishal7084'
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Get all users with Teacher role
        print("=== USERS TABLE (Teachers) ===")
        cursor.execute("SELECT id, username, email, role FROM users WHERE role = 'Teacher'")
        users = cursor.fetchall()
        
        for user in users:
            print(f"\nUser ID: {user['id']}")
            print(f"Username: {user['username']}")
            print(f"Email: {user['email']}")
            print(f"Role: {user['role']}")
            
            # Check if this email exists in teacher_admissions
            cursor.execute("SELECT * FROM teacher_admissions WHERE email = %s", (user['email'],))
            teacher_data = cursor.fetchone()
            
            if teacher_data:
                print(f"✓ Teacher admission found:")
                print(f"  Full Name: {teacher_data['full_name']}")
                print(f"  Phone: {teacher_data['phone']}")
                print(f"  Designation: {teacher_data['designation']}")
            else:
                print(f"✗ NO teacher admission data found for this email")
        
        print("\n\n=== ALL TEACHER ADMISSIONS ===")
        cursor.execute("SELECT id, full_name, email, phone, designation, department FROM teacher_admissions")
        all_teachers = cursor.fetchall()
        
        for t in all_teachers:
            print(f"\nID: {t['id']}")
            print(f"Name: {t['full_name']}")
            print(f"Email: {t['email']}")
            print(f"Phone: {t['phone']}")
            print(f"Designation: {t['designation']}")
            print(f"Department: {t['department']}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_data_mismatch()
