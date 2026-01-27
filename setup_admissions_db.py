"""
Database setup script for admissions table
Run this script to create the admissions table in your MySQL database
"""
import mysql.connector

def setup_admissions_table():
    try:
        # Connect to database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal7084",
            database="flask_auth"
        )
        
        cursor = db.cursor()
        
        # Create admissions table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS admissions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            
            -- Student Information
            student_name VARCHAR(255) NOT NULL,
            date_of_birth DATE NOT NULL,
            email VARCHAR(255) NOT NULL,
            contact_number VARCHAR(20) NOT NULL,
            class_enroll VARCHAR(50) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            
            -- Guardian Information
            guardian_name VARCHAR(255) NOT NULL,
            guardian_contact VARCHAR(20) NOT NULL,
            guardian_occupation VARCHAR(100),
            guardian_address TEXT,
            
            -- Previous Board Details
            previous_board VARCHAR(50) NOT NULL,
            previous_school VARCHAR(255),
            percentage_obtained VARCHAR(10),
            
            -- Enrolled Board
            enrolled_board VARCHAR(50) NOT NULL,
            enrolled_school VARCHAR(255),
            
            -- Program & Subjects
            program_enrolled VARCHAR(100) NOT NULL,
            subjects TEXT,
            
            -- Metadata
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            INDEX idx_email (email),
            INDEX idx_student_name (student_name),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        cursor.execute(create_table_query)
        db.commit()
        
        print("✓ Admissions table created successfully!")
        
        # Verify table exists
        cursor.execute("SHOW TABLES LIKE 'admissions'")
        result = cursor.fetchone()
        
        if result:
            print("✓ Table verification successful!")
            
            # Show table structure
            cursor.execute("DESCRIBE admissions")
            columns = cursor.fetchall()
            
            print("\n📋 Table Structure:")
            print("-" * 80)
            for col in columns:
                print(f"  {col[0]:<25} {col[1]:<20} {col[2]:<10}")
            print("-" * 80)
        
        cursor.close()
        db.close()
        
        print("\n✅ Database setup completed successfully!")
        print("You can now use the admission form to submit applications.")
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        print("\nPlease make sure:")
        print("  1. MySQL server is running")
        print("  2. Database 'flask_auth' exists")
        print("  3. Username and password are correct")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("APEX LEARNING HUB - Admissions Table Setup")
    print("=" * 80)
    print()
    setup_admissions_table()
