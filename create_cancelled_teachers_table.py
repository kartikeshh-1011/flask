import mysql.connector

# Database connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vishal7084",
        database="flask_auth"
    )
    cursor = conn.cursor()
    
    # Create cancelled_teachers table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cancelled_teachers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        
        -- Original teacher ID (for reference)
        original_teacher_id INT,
        
        -- Personal Information
        full_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        date_of_birth DATE,
        gender VARCHAR(10),
        blood_group VARCHAR(5),
        address TEXT,
        
        -- Professional Information
        employee_id VARCHAR(50) NOT NULL,
        designation VARCHAR(100),
        department VARCHAR(100),
        highest_qualification VARCHAR(100),
        specialization VARCHAR(100),
        experience INT,
        joining_date DATE,
        
        -- Emergency Contact
        emergency_contact_name VARCHAR(255),
        emergency_contact_phone VARCHAR(20),
        emergency_contact_relation VARCHAR(50),
        
        -- Metadata
        original_created_at TIMESTAMP NULL,
        cancelled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        cancellation_reason TEXT,
        
        INDEX idx_email (email),
        INDEX idx_employee_id (employee_id),
        INDEX idx_cancelled_at (cancelled_at),
        INDEX idx_original_teacher_id (original_teacher_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    
    cursor.execute(create_table_query)
    conn.commit()
    
    print("✅ Table 'cancelled_teachers' created successfully!")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
