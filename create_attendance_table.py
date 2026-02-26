import mysql.connector

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal7084",
            database="flask_auth",
            use_pure=True
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def create_attendance_table():
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        
        # Create attendance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_email VARCHAR(255) NOT NULL,
                student_name VARCHAR(255),
                class_name VARCHAR(50) NOT NULL,
                date DATE NOT NULL,
                status ENUM('Present', 'Absent', 'Late') NOT NULL,
                marked_by VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_attendance (student_email, date)
            )
        """)
        
        print("Attendance table created successfully (or already exists).")
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating table: {e}")

if __name__ == "__main__":
    create_attendance_table()
