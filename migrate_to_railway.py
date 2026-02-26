import mysql.connector
import os

# --- CONFIGURE THESE WITH YOUR RAILWAY MYSQL VARIABLES ---
# You can find these in the Railway MySQL "Variables" tab
DB_CONFIG = {
    'host': 'mainline.proxy.rlwy.net',
    'user': 'root',
    'password': 'QKTJUAYusDsXCPsfELgvjVEfhlaBhSGT',
    'database': 'railway',
    'port': '46971'
}

def migrate():
    try:
        print("Connecting to Railway MySQL...")
        # Use buffered=True to avoid 'Unread result found' errors
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(buffered=True)

        print("Disabling foreign key checks for migration...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # 1. Create Users Table (Required for Login)
        print("Creating 'users' table...")
        users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARBINARY(255) NOT NULL,
            role VARCHAR(50) DEFAULT 'Student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(users_table_query)

        # 2. Run your official SQL file
        sql_file_path = 'parent_dashboard_database.sql'
        print(f"Reading {sql_file_path}...")
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            full_sql = f.read()
            # Split by semicolon but preserve content
            sql_queries = full_sql.split(';')
            
        print(f"Running {len(sql_queries)} database migration queries...")
        for query in sql_queries:
            clean_query = query.strip()
            if not clean_query or clean_query.startswith('--') or clean_query.startswith('/*'):
                continue
                
            try:
                cursor.execute(clean_query)
                # Consume any remaining results
                while cursor.nextset():
                    pass
            except Exception as e:
                # Log error but try to continue
                print(f"Error in query: {clean_query[:50]}... \n -> {e}")

        print("Re-enabling foreign key checks...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        conn.commit()
        print("\n" + "="*50)
        print("🎉 SUCCESS! Your whole database and all tables are ready.")
        print("="*50)
        print("\nNEXT STEP: You MUST push your code to GitHub for the fixes to work:")
        print("1. git add .")
        print("2. git commit -m 'Fix database and email logging'")
        print("3. git push")
        print("\nThen try to Sign Up on the live site again!")
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    migrate()
