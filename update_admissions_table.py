"""
Database migration script to add status field to admissions table
This allows tracking of Active and Cancelled admissions
"""
import mysql.connector

def update_admissions_table():
    try:
        # Connect to database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal7084",
            database="flask_auth"
        )
        
        cursor = db.cursor()
        
        print("=" * 80)
        print("APEX LEARNING HUB - Admissions Table Update")
        print("=" * 80)
        print()
        
        # Check if status column already exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = 'flask_auth' 
            AND TABLE_NAME = 'admissions' 
            AND COLUMN_NAME = 'status'
        """)
        
        column_exists = cursor.fetchone()[0]
        
        if column_exists:
            print("⚠ Status column already exists in admissions table.")
            print("No changes needed.")
        else:
            # Add status column
            print("📝 Adding 'status' column to admissions table...")
            
            alter_query = """
            ALTER TABLE admissions 
            ADD COLUMN status ENUM('Active', 'Cancelled') 
            DEFAULT 'Active' 
            NOT NULL 
            AFTER created_at
            """
            
            cursor.execute(alter_query)
            db.commit()
            
            print("✓ Status column added successfully!")
            
            # Add index for performance
            print("📝 Adding index on status column...")
            
            index_query = """
            ALTER TABLE admissions 
            ADD INDEX idx_status (status)
            """
            
            cursor.execute(index_query)
            db.commit()
            
            print("✓ Index added successfully!")
            
            # Update all existing records to 'Active'
            print("📝 Updating existing records to 'Active' status...")
            
            update_query = """
            UPDATE admissions 
            SET status = 'Active' 
            WHERE status IS NULL
            """
            
            cursor.execute(update_query)
            db.commit()
            
            affected_rows = cursor.rowcount
            print(f"✓ Updated {affected_rows} existing record(s) to 'Active' status")
        
        # Show updated table structure
        cursor.execute("DESCRIBE admissions")
        columns = cursor.fetchall()
        
        print("\n📋 Updated Table Structure:")
        print("-" * 80)
        for col in columns:
            print(f"  {col[0]:<25} {col[1]:<30} {col[2]:<10}")
        print("-" * 80)
        
        cursor.close()
        db.close()
        
        print("\n✅ Database migration completed successfully!")
        print("The admissions table now supports status tracking (Active/Cancelled).")
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        print("\nPlease make sure:")
        print("  1. MySQL server is running")
        print("  2. Database 'flask_auth' exists")
        print("  3. Username and password are correct")
        print("  4. Admissions table exists")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_admissions_table()
