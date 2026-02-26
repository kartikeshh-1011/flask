import mysql.connector

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="vishal7084",
        database="flask_auth"
    )

# Create teacher_admissions table
def create_teacher_admissions_table():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teacher_admissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                date_of_birth DATE NOT NULL,
                gender VARCHAR(20) NOT NULL,
                blood_group VARCHAR(10),
                address TEXT NOT NULL,
                
                employee_id VARCHAR(50) NOT NULL UNIQUE,
                designation VARCHAR(100) NOT NULL,
                department VARCHAR(100) NOT NULL,
                joining_date DATE NOT NULL,
                experience INT NOT NULL,
                specialization VARCHAR(255),
                
                highest_qualification VARCHAR(100) NOT NULL,
                university VARCHAR(255) NOT NULL,
                graduation_year INT NOT NULL,
                certifications TEXT,
                
                emergency_contact_name VARCHAR(255) NOT NULL,
                emergency_contact_phone VARCHAR(20) NOT NULL,
                emergency_contact_relation VARCHAR(100) NOT NULL,

                
                photo_path VARCHAR(255),

                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                
                INDEX idx_email (email),
                INDEX idx_employee_id (employee_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        db.commit()
        print("✓ teacher_admissions table created successfully!")
        
        cursor.close()
        db.close()
        
    except mysql.connector.Error as err:
        print(f"✗ Error creating table: {err}")

if __name__ == "__main__":
    print("Creating teacher_admissions table...")
    create_teacher_admissions_table()
    print("Done!")
