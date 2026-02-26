import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vishal7084',
    'database': 'flask_auth'
}

def create_table():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        with open('syllabus_table.sql', 'r') as f:
            sql_script = f.read()
            
        # Split by semicolon and execute each command
        commands = sql_script.split(';')
        for command in commands:
            if command.strip():
                cursor.execute(command)
                
        conn.commit()
        print("Syllabus table created successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_table()
