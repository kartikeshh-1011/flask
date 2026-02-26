import mysql.connector
from app import get_db_connection

def create_tables():
    try:
        print("Connecting to database...")
        db = get_db_connection()
        cursor = db.cursor()
        
        print("Reading SQL script...")
        with open('create_class_tables.sql', 'r') as f:
            sql_script = f.read()
            
        print("Executing table creation...")
        # Split by semicolon to execute statements individually
        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    print(f"Executed statement starting: {statement.strip()[:20]}...")
                except mysql.connector.Error as err:
                    print(f"Error executing statement: {err}")
        
        db.commit()
        print("Tables created successfully.")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_tables()
