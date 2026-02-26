import mysql.connector
import os

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vishal7084',
    'database': 'flask_auth'
}

def create_table():
    try:
        # Read the SQL file
        with open('schedules_table.sql', 'r') as f:
            sql_commands = f.read()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Split commands by semicolon and execute
        commands = sql_commands.split(';')
        for command in commands:
            if command.strip():
                try:
                    cursor.execute(command)
                    print(f"Executed: {command[:50]}...")
                except mysql.connector.Error as err:
                    print(f"Error executing command: {err}")

        conn.commit()
        cursor.close()
        conn.close()
        print("Schedules table created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    create_table()
