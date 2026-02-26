import mysql.connector

def create_aux_tables():
    config = {
        "host": "localhost",
        "user": "root",
        "password": "vishal7084",
        "database": "flask_auth"
    }
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # 1. Contacts Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Contacts table checked/created")
        
        # 2. Feedback Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                feedback TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Feedback table checked/created")
        
        # 3. Complaints Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                contact VARCHAR(20) NOT NULL,
                description TEXT NOT NULL,
                status VARCHAR(20) DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Complaints table checked/created")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ All auxiliary tables setup complete.")
        
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

if __name__ == "__main__":
    create_aux_tables()
