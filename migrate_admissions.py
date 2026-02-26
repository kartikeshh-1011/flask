import mysql.connector
from app import get_db_connection

def migrate_admissions():
    
    # Map class names to table names
    class_map = {
        'V': 'admissions_v', '5': 'admissions_v',
        'VI': 'admissions_vi', '6': 'admissions_vi',
        'VII': 'admissions_vii', '7': 'admissions_vii',
        'VIII': 'admissions_viii', '8': 'admissions_viii',
        'IX': 'admissions_ix', '9': 'admissions_ix',
        'X': 'admissions_x', '10': 'admissions_x',
        'XI': 'admissions_xi', '11': 'admissions_xi',
        'XII': 'admissions_xii', '12': 'admissions_xii'
    }

    try:
        print("Connecting to database...")
        db = get_db_connection()
        source_cursor = db.cursor(dictionary=True)
        dest_cursor = db.cursor()
        
        # Get all students from legacy admissions table
        print("Fetching existing admissions...")
        source_cursor.execute("SELECT * FROM admissions")
        students = source_cursor.fetchall()
        
        print(f"Found {len(students)} students to migrate.")
        
        migrated_count = 0
        skipped_count = 0
        
        for student in students:
            class_enroll = student['class_enroll']
            target_table = class_map.get(class_enroll)
            
            if not target_table:
                print(f"Skipping student {student['student_name']} (ID: {student['id']}) - Invalid class: {class_enroll}")
                skipped_count += 1
                continue
                
            print(f"Migrating {student['student_name']} (Class {class_enroll}) to {target_table}...")
            
            # Check if already exists in target (by email)
            dest_cursor.execute(f"SELECT id FROM {target_table} WHERE email = %s", (student['email'],))
            if dest_cursor.fetchone():
                print(f"Student already exists in {target_table}, skipping.")
                skipped_count += 1
                continue

            # Insert into target table
            dest_cursor.execute(f"""
                INSERT INTO {target_table} (
                    student_name, date_of_birth, email, contact_number, 
                    class_enroll, gender, guardian_name, guardian_contact, 
                    guardian_occupation, guardian_address, previous_board, 
                    previous_school, percentage_obtained, enrolled_board, 
                    enrolled_school, program_enrolled, subjects, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                student['student_name'], student['date_of_birth'], student['email'], student['contact_number'],
                student['class_enroll'], student['gender'], student['guardian_name'], student['guardian_contact'],
                student['guardian_occupation'], student['guardian_address'], student['previous_board'],
                student['previous_school'], student['percentage_obtained'], student['enrolled_board'],
                student['enrolled_school'], student['program_enrolled'], student['subjects'], student['created_at']
            ))
            
            migrated_count += 1
        
        db.commit()
        
        print(f"Migration completed.")
        print(f"Migrated: {migrated_count}")
        print(f"Skipped: {skipped_count}")
        
        source_cursor.close()
        dest_cursor.close()
        db.close()
        
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate_admissions()
