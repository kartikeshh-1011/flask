"""
Database setup script for results table
Run this script to create the results table in your MySQL database
"""
import mysql.connector

def setup_results_table():
    try:
        # Connect to database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal7084",
            database="flask_auth"
        )
        
        cursor = db.cursor()
        
        # Create results table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            
            -- Student Information
            student_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            class VARCHAR(50) NOT NULL,
            
            -- Subject Marks
            hindi_grammar DECIMAL(5,2) DEFAULT NULL,
            english_grammar DECIMAL(5,2) DEFAULT NULL,
            marathi_grammar DECIMAL(5,2) DEFAULT NULL,
            maths DECIMAL(5,2) DEFAULT NULL,
            science DECIMAL(5,2) DEFAULT NULL,
            physics DECIMAL(5,2) DEFAULT NULL,
            chemistry DECIMAL(5,2) DEFAULT NULL,
            biology DECIMAL(5,2) DEFAULT NULL,
            sst DECIMAL(5,2) DEFAULT NULL,
            vedic_maths DECIMAL(5,2) DEFAULT NULL,
            art_craft DECIMAL(5,2) DEFAULT NULL,
            
            -- Calculated Fields
            total_marks DECIMAL(6,2) DEFAULT NULL,
            percentage DECIMAL(5,2) DEFAULT NULL,
            grade VARCHAR(10) DEFAULT NULL,
            
            -- Metadata
            updated_by VARCHAR(255) DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            -- Indexes
            INDEX idx_student_name (student_name),
            INDEX idx_email (email),
            INDEX idx_class (class),
            UNIQUE KEY unique_student (student_name, email, class)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        cursor.execute(create_table_query)
        db.commit()
        
        print("✓ Results table created successfully!")
        
        # Verify table exists
        cursor.execute("SHOW TABLES LIKE 'results'")
        result = cursor.fetchone()
        
        if result:
            print("✓ Table verification successful!")
            
            # Show table structure
            cursor.execute("DESCRIBE results")
            columns = cursor.fetchall()
            
            print("\n📋 Results Table Structure:")
            print("-" * 80)
            for col in columns:
                print(f"  {col[0]:<25} {col[1]:<20} {col[2]:<10}")
            print("-" * 80)
        
        cursor.close()
        db.close()
        
        print("\n✅ Database setup completed successfully!")
        print("Teachers can now update student results.")
        
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
    print("APEX LEARNING HUB - Results Table Setup")
    print("=" * 80)
    print()
    setup_results_table()
