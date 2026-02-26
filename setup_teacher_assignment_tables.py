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

def create_tables():
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()

    # Create class_teachers table
    try:
        cursor.execute("DROP TABLE IF EXISTS class_teachers")
        cursor.execute("""
        CREATE TABLE class_teachers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            class_name VARCHAR(10) NOT NULL,
            section VARCHAR(5) DEFAULT 'A',
            teacher_email VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY unique_class_teacher (class_name, section)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """)
        print("Table 'class_teachers' recreated with utf8mb4_unicode_ci collation.")
    except mysql.connector.Error as err:
        print(f"Error creating class_teachers table: {err}")

    # Create subject_teachers table
    try:
        cursor.execute("DROP TABLE IF EXISTS subject_teachers")
        cursor.execute("""
        CREATE TABLE subject_teachers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            class_name VARCHAR(10) NOT NULL,
            section VARCHAR(5) DEFAULT 'A',
            subject_name VARCHAR(50) NOT NULL,
            teacher_email VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY unique_subject_teacher (class_name, section, subject_name)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """)
        print("Table 'subject_teachers' recreated with utf8mb4_unicode_ci collation.")
    except mysql.connector.Error as err:
        print(f"Error creating subject_teachers table: {err}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
