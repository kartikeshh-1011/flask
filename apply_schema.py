import mysql.connector
from app import get_db_connection

def apply_schema():
    try:
        print("Connecting to database...")
        db = get_db_connection()
        cursor = db.cursor()
        
        print("Reading SQL script...")
        with open('update_teacher_schema.sql', 'r') as f:
            sql_script = f.read()
            
        print("Executing schema update...")
        # Split by semicolon in case of multiple statements, though here it's one
        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                except mysql.connector.Error as err:
                    # Ignore "Duplicate column name" error if columns already exist
                    if err.errno == 1060:
                        print(f"Column already exists, skipping: {err}")
                    else:
                        raise err
        
        db.commit()
        print("Schema update committed successfully.")
        
        cursor.close()
        db.close()
        print("Done.")
        
    except Exception as e:
        print(f"Error applying schema: {e}")

if __name__ == "__main__":
    apply_schema()
